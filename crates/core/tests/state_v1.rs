#![forbid(unsafe_code)]

use wepld_contracts::{
    CancelEnvelope, CancellationOutcome, CapabilitiesRequestPayload, Capability, CapabilityList,
    EventEnvelope, HealthRequestPayload, HealthStatus, ObserveHealthRequestPayload, Principal,
    ProtocolVersion, RequestEnvelope, RequestFields, ResponseEnvelope, VersionRequestPayload,
};
use wepld_core::{
    CoreProfile, HandshakeState, MAX_HEALTH_WATCHES, MAX_IN_FLIGHT_REQUESTS,
    MAX_TERMINAL_RESULTS, StateError,
};

const LAUNCH_ID: u64 = 41;

fn profile() -> CoreProfile {
    CoreProfile::new(
        "0.1.0-test",
        "build-test",
        CapabilityList::try_from(vec![
            Capability::Health,
            Capability::Version,
            Capability::Capabilities,
            Capability::HealthObservation,
            Capability::Cancellation,
        ])
        .expect("fixture capability list is bounded"),
    )
}

fn state() -> HandshakeState {
    HandshakeState::new(LAUNCH_ID, profile(), HealthStatus::Healthy)
}

fn health_request(launch_id: u64, request_id: u64) -> RequestEnvelope {
    RequestEnvelope::Health(RequestFields {
        protocol_version: ProtocolVersion::V1,
        principal: Principal::DesktopHost,
        launch_id,
        request_id,
        payload: HealthRequestPayload {},
    })
}

fn version_request(launch_id: u64, request_id: u64) -> RequestEnvelope {
    RequestEnvelope::Version(RequestFields {
        protocol_version: ProtocolVersion::V1,
        principal: Principal::DesktopHost,
        launch_id,
        request_id,
        payload: VersionRequestPayload {},
    })
}

fn capabilities_request(launch_id: u64, request_id: u64) -> RequestEnvelope {
    RequestEnvelope::Capabilities(RequestFields {
        protocol_version: ProtocolVersion::V1,
        principal: Principal::DesktopHost,
        launch_id,
        request_id,
        payload: CapabilitiesRequestPayload {},
    })
}

fn observe_request(launch_id: u64, request_id: u64) -> RequestEnvelope {
    RequestEnvelope::ObserveHealth(RequestFields {
        protocol_version: ProtocolVersion::V1,
        principal: Principal::DesktopHost,
        launch_id,
        request_id,
        payload: ObserveHealthRequestPayload {},
    })
}

fn cancellation(launch_id: u64, request_id: u64, target_request_id: u64) -> CancelEnvelope {
    CancelEnvelope {
        protocol_version: ProtocolVersion::V1,
        principal: Principal::DesktopHost,
        launch_id,
        request_id,
        target_request_id,
    }
}

fn cancel_outcome(response: ResponseEnvelope) -> CancellationOutcome {
    match response {
        ResponseEnvelope::Cancel(fields) => fields.payload.outcome,
        other => panic!("expected cancellation response, got {other:?}"),
    }
}

#[test]
fn health_version_and_capabilities_dispatch_with_exact_correlation() {
    let mut core = state();

    let health = core
        .accept_request(health_request(LAUNCH_ID, 1))
        .expect("health request must reserve");
    let health_response = core
        .dispatch_request(health)
        .expect("health request must dispatch");
    match health_response {
        ResponseEnvelope::Health(fields) => {
            assert_eq!(fields.launch_id, LAUNCH_ID);
            assert_eq!(fields.request_id, 1);
            assert_eq!(fields.payload.status, HealthStatus::Healthy);
        }
        other => panic!("expected health response, got {other:?}"),
    }

    let version = core
        .accept_request(version_request(LAUNCH_ID, 2))
        .expect("version request must reserve");
    let version_response = core
        .dispatch_request(version)
        .expect("version request must dispatch");
    match version_response {
        ResponseEnvelope::Version(fields) => {
            assert_eq!(fields.launch_id, LAUNCH_ID);
            assert_eq!(fields.request_id, 2);
            assert_eq!(fields.payload.core_version, "0.1.0-test");
            assert_eq!(fields.payload.build_id, "build-test");
        }
        other => panic!("expected version response, got {other:?}"),
    }

    let capabilities = core
        .accept_request(capabilities_request(LAUNCH_ID, 3))
        .expect("capability request must reserve");
    let capability_response = core
        .dispatch_request(capabilities)
        .expect("capability request must dispatch");
    match capability_response {
        ResponseEnvelope::Capabilities(fields) => {
            assert_eq!(fields.launch_id, LAUNCH_ID);
            assert_eq!(fields.request_id, 3);
            assert_eq!(fields.payload.capabilities.as_slice(), profile().capabilities().as_slice());
        }
        other => panic!("expected capability response, got {other:?}"),
    }

    assert_eq!(core.in_flight_count(), 0);
    assert_eq!(core.terminal_result_count(), 3);
    assert_eq!(core.highest_accepted_command_id(), Some(3));
}

#[test]
fn stale_launch_requests_and_cancellations_do_not_mutate_high_water() {
    let mut core = state();

    assert_eq!(
        core.accept_request(health_request(LAUNCH_ID + 1, 1)),
        Err(StateError::StaleLaunch {
            expected: LAUNCH_ID,
            received: LAUNCH_ID + 1,
        })
    );
    assert_eq!(core.highest_accepted_command_id(), None);

    assert_eq!(
        core.cancel(cancellation(LAUNCH_ID + 1, 1, 99)),
        Err(StateError::StaleLaunch {
            expected: LAUNCH_ID,
            received: LAUNCH_ID + 1,
        })
    );
    assert_eq!(core.highest_accepted_command_id(), None);
    assert_eq!(core.in_flight_count(), 0);
}

#[test]
fn command_ids_are_strictly_increasing_with_gaps_and_reuse_is_rejected() {
    let mut core = state();

    let first = core
        .accept_request(health_request(LAUNCH_ID, 10))
        .expect("first command must reserve");
    core.dispatch_request(first).expect("first command must dispatch");

    let second = core
        .accept_request(health_request(LAUNCH_ID, 12))
        .expect("larger command with a gap must reserve");
    core.dispatch_request(second).expect("second command must dispatch");

    assert_eq!(
        core.accept_request(health_request(LAUNCH_ID, 11)),
        Err(StateError::ReplayOrNonMonotonic {
            highest_accepted_command_id: 12,
            received: 11,
        })
    );
    assert_eq!(
        core.accept_request(health_request(LAUNCH_ID, 12)),
        Err(StateError::ReplayOrNonMonotonic {
            highest_accepted_command_id: 12,
            received: 12,
        })
    );
    assert_eq!(core.highest_accepted_command_id(), Some(12));
}

#[test]
fn maximum_command_id_never_wraps_or_reuses() {
    let mut core = state();

    let maximum = core
        .accept_request(health_request(LAUNCH_ID, u64::MAX))
        .expect("fresh maximum command id is valid once");
    core.dispatch_request(maximum)
        .expect("maximum command must dispatch");

    assert_eq!(
        core.accept_request(health_request(LAUNCH_ID, 0)),
        Err(StateError::ReplayOrNonMonotonic {
            highest_accepted_command_id: u64::MAX,
            received: 0,
        })
    );
    assert_eq!(core.highest_accepted_command_id(), Some(u64::MAX));
}

#[test]
fn in_flight_budget_rejects_without_consuming_command_id_and_can_retry() {
    let mut core = state();
    let mut pending = Vec::new();

    for request_id in 1..=MAX_IN_FLIGHT_REQUESTS as u64 {
        pending.push(
            core.accept_request(health_request(LAUNCH_ID, request_id))
                .expect("request within in-flight budget must reserve"),
        );
    }
    assert_eq!(core.in_flight_count(), MAX_IN_FLIGHT_REQUESTS);
    assert_eq!(
        core.accept_request(health_request(
            LAUNCH_ID,
            MAX_IN_FLIGHT_REQUESTS as u64 + 1,
        )),
        Err(StateError::InFlightBudgetExhausted {
            max: MAX_IN_FLIGHT_REQUESTS,
        })
    );
    assert_eq!(
        core.highest_accepted_command_id(),
        Some(MAX_IN_FLIGHT_REQUESTS as u64)
    );

    core.dispatch_request(pending.remove(0))
        .expect("freeing one reservation must succeed");
    let retried = core
        .accept_request(health_request(
            LAUNCH_ID,
            MAX_IN_FLIGHT_REQUESTS as u64 + 1,
        ))
        .expect("same rejected command id may retry after capacity is free");
    assert_eq!(retried.request_id(), MAX_IN_FLIGHT_REQUESTS as u64 + 1);
    assert_eq!(core.in_flight_count(), MAX_IN_FLIGHT_REQUESTS);
}

#[test]
fn health_watch_budget_counts_pending_and_active_watches() {
    let mut core = state();
    let mut pending = Vec::new();

    for request_id in 1..=MAX_HEALTH_WATCHES as u64 {
        pending.push(
            core.accept_request(observe_request(LAUNCH_ID, request_id))
                .expect("watch within budget must reserve"),
        );
    }
    assert_eq!(core.health_watch_count(), MAX_HEALTH_WATCHES);
    assert_eq!(
        core.accept_request(observe_request(LAUNCH_ID, MAX_HEALTH_WATCHES as u64 + 1)),
        Err(StateError::HealthWatchBudgetExhausted {
            max: MAX_HEALTH_WATCHES,
        })
    );
    assert_eq!(
        core.highest_accepted_command_id(),
        Some(MAX_HEALTH_WATCHES as u64)
    );

    core.dispatch_request(pending.remove(0))
        .expect("activating a reserved watch keeps the same budget occupancy");
    assert_eq!(core.health_watch_count(), MAX_HEALTH_WATCHES);
}

#[test]
fn replayed_observation_cannot_allocate_a_second_watch() {
    let mut core = state();
    let watch = core
        .accept_request(observe_request(LAUNCH_ID, 1))
        .expect("watch must reserve");
    core.dispatch_request(watch).expect("watch must activate");

    assert_eq!(core.health_watch_count(), 1);
    assert_eq!(
        core.accept_request(observe_request(LAUNCH_ID, 1)),
        Err(StateError::ReplayOrNonMonotonic {
            highest_accepted_command_id: 1,
            received: 1,
        })
    );
    assert_eq!(core.health_watch_count(), 1);
    assert_eq!(core.in_flight_count(), 1);
}

#[test]
fn cancellation_is_single_mutation_and_fresh_terminal_cancel_is_noop() {
    let mut core = state();
    let watch = core
        .accept_request(observe_request(LAUNCH_ID, 1))
        .expect("watch must reserve");
    core.dispatch_request(watch).expect("watch must activate");

    let first = core
        .cancel(cancellation(LAUNCH_ID, 2, 1))
        .expect("fresh cancellation must succeed");
    assert_eq!(cancel_outcome(first), CancellationOutcome::Cancelled);
    assert_eq!(core.health_watch_count(), 0);
    assert_eq!(core.in_flight_count(), 0);
    assert_eq!(core.terminal_result_count(), 1);

    let second = core
        .cancel(cancellation(LAUNCH_ID, 3, 1))
        .expect("fresh cancellation of terminal target is deterministic");
    assert_eq!(cancel_outcome(second), CancellationOutcome::AlreadyTerminal);
    assert_eq!(core.terminal_result_count(), 1);

    assert_eq!(
        core.cancel(cancellation(LAUNCH_ID, 3, 1)),
        Err(StateError::ReplayOrNonMonotonic {
            highest_accepted_command_id: 3,
            received: 3,
        })
    );
    assert_eq!(core.terminal_result_count(), 1);
    assert_eq!(core.highest_accepted_command_id(), Some(3));
}

#[test]
fn unknown_and_completed_cancellation_targets_are_distinct() {
    let mut unknown = state();
    let response = unknown
        .cancel(cancellation(LAUNCH_ID, 1, 900))
        .expect("fresh cancellation command is accepted");
    assert_eq!(cancel_outcome(response), CancellationOutcome::UnknownTarget);

    let mut completed = state();
    let request = completed
        .accept_request(health_request(LAUNCH_ID, 1))
        .expect("health request must reserve");
    completed
        .dispatch_request(request)
        .expect("health request must complete");
    let response = completed
        .cancel(cancellation(LAUNCH_ID, 2, 1))
        .expect("fresh terminal cancellation must succeed");
    assert_eq!(cancel_outcome(response), CancellationOutcome::AlreadyTerminal);
}

#[test]
fn terminal_cache_is_bounded_but_replay_floor_survives_eviction() {
    let mut core = state();

    for request_id in 1..=(MAX_TERMINAL_RESULTS as u64 + 1) {
        let request = core
            .accept_request(health_request(LAUNCH_ID, request_id))
            .expect("sequential request must reserve");
        core.dispatch_request(request)
            .expect("sequential request must complete");
    }
    assert_eq!(core.terminal_result_count(), MAX_TERMINAL_RESULTS);

    let cancel_id = MAX_TERMINAL_RESULTS as u64 + 2;
    let response = core
        .cancel(cancellation(LAUNCH_ID, cancel_id, 1))
        .expect("fresh cancellation command must be accepted");
    assert_eq!(cancel_outcome(response), CancellationOutcome::UnknownTarget);
    assert_eq!(core.terminal_result_count(), MAX_TERMINAL_RESULTS);

    assert_eq!(
        core.accept_request(health_request(LAUNCH_ID, 1)),
        Err(StateError::ReplayOrNonMonotonic {
            highest_accepted_command_id: cancel_id,
            received: 1,
        })
    );
}

#[test]
fn cancellation_before_dispatch_prevents_watch_activation() {
    let mut core = state();
    let pending = core
        .accept_request(observe_request(LAUNCH_ID, 1))
        .expect("watch must reserve");
    assert_eq!(core.health_watch_count(), 1);

    let response = core
        .cancel(cancellation(LAUNCH_ID, 2, 1))
        .expect("pending watch may be cancelled");
    assert_eq!(cancel_outcome(response), CancellationOutcome::Cancelled);
    assert_eq!(core.health_watch_count(), 0);

    assert_eq!(
        core.dispatch_request(pending),
        Err(StateError::PendingRequestNoLongerInFlight { request_id: 1 })
    );
    assert_eq!(core.health_watch_count(), 0);
    assert_eq!(core.in_flight_count(), 0);
}

#[test]
fn health_events_are_bounded_correlated_ordered_and_nonduplicating() {
    let mut core = state();

    for request_id in [2, 5] {
        let watch = core
            .accept_request(observe_request(LAUNCH_ID, request_id))
            .expect("watch must reserve");
        core.dispatch_request(watch).expect("watch must activate");
    }

    let degraded = core
        .update_health(HealthStatus::Degraded)
        .expect("health transition must emit bounded events");
    assert_eq!(degraded.len(), 2);
    assert!(degraded.len() <= MAX_HEALTH_WATCHES);

    for (event, expected_request_id) in degraded.iter().zip([2, 5]) {
        match event {
            EventEnvelope::ObserveHealth(fields) => {
                assert_eq!(fields.launch_id, LAUNCH_ID);
                assert_eq!(fields.request_id, expected_request_id);
                assert_eq!(fields.payload.sequence, 1);
                assert_eq!(fields.payload.status, HealthStatus::Degraded);
            }
        }
    }

    assert!(
        core.update_health(HealthStatus::Degraded)
            .expect("unchanged health is a no-op")
            .is_empty()
    );

    let healthy = core
        .update_health(HealthStatus::Healthy)
        .expect("second transition must emit next sequence");
    for event in healthy {
        match event {
            EventEnvelope::ObserveHealth(fields) => {
                assert_eq!(fields.payload.sequence, 2);
                assert_eq!(fields.payload.status, HealthStatus::Healthy);
            }
        }
    }
}
