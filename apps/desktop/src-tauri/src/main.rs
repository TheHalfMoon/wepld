#![forbid(unsafe_code)]
use std::sync::Mutex;
use wepld_contracts::CancellationOutcome;
use wepld_contracts::Capability;
use wepld_contracts::HealthStatus;
use wepld_contracts::ResponseEnvelope;
use wepld_desktop::CoreClient;
use wepld_desktop::InboundEnvelope;

struct AppState {
    core: Mutex<Option<CoreClient>>,
}

#[tauri::command]
fn core_ready(state: tauri::State<'_, AppState>) -> Result<bool, String> {
    let mut guard = state
        .core
        .lock()
        .map_err(|_| String::from("core state unavailable"))?;
    let client = guard
        .as_mut()
        .ok_or_else(|| String::from("core unavailable"))?;
    let request_id = client
        .send_health()
        .map_err(|_| String::from("core request failed"))?;
    for _ in 0..=32 {
        match client.receive().map_err(|_| String::from("core response unavailable"))? {
            InboundEnvelope::Response(ResponseEnvelope::Health(fields))
                if fields.request_id == request_id =>
            {
                return Ok(client.is_ready());
            }
            InboundEnvelope::Event(_) => continue,
            InboundEnvelope::ProtocolError(_) => {
                return Err(String::from("core protocol error"));
            }
            InboundEnvelope::Response(_) => {
                return Err(String::from("unexpected readiness response"));
            }
        }
    }
    Err(String::from("core response event budget exceeded"))
}

#[tauri::command]
fn core_health(state: tauri::State<'_, AppState>) -> Result<String, String> {
    let mut guard = state
        .core
        .lock()
        .map_err(|_| String::from("core state unavailable"))?;
    let client = guard
        .as_mut()
        .ok_or_else(|| String::from("core unavailable"))?;
    let request_id = client
        .send_health()
        .map_err(|_| String::from("core request failed"))?;
    for _ in 0..=32 {
        match client.receive().map_err(|_| String::from("core response unavailable"))? {
            InboundEnvelope::Response(ResponseEnvelope::Health(fields))
                if fields.request_id == request_id =>
            {
                return Ok(String::from(match fields.payload.status {
                    HealthStatus::Healthy => "healthy",
                    HealthStatus::Degraded => "degraded",
                }));
            }
            InboundEnvelope::Event(_) => continue,
            InboundEnvelope::ProtocolError(_) => {
                return Err(String::from("core protocol error"));
            }
            InboundEnvelope::Response(_) => {
                return Err(String::from("unexpected health response"));
            }
        }
    }
    Err(String::from("core response event budget exceeded"))
}

#[tauri::command]
fn core_version(state: tauri::State<'_, AppState>) -> Result<String, String> {
    let mut guard = state
        .core
        .lock()
        .map_err(|_| String::from("core state unavailable"))?;
    let client = guard
        .as_mut()
        .ok_or_else(|| String::from("core unavailable"))?;
    let request_id = client
        .send_version()
        .map_err(|_| String::from("core request failed"))?;
    for _ in 0..=32 {
        match client.receive().map_err(|_| String::from("core response unavailable"))? {
            InboundEnvelope::Response(ResponseEnvelope::Version(fields))
                if fields.request_id == request_id =>
            {
                return Ok(format!(
                    "{} ({})",
                    fields.payload.core_version, fields.payload.build_id
                ));
            }
            InboundEnvelope::Event(_) => continue,
            InboundEnvelope::ProtocolError(_) => {
                return Err(String::from("core protocol error"));
            }
            InboundEnvelope::Response(_) => {
                return Err(String::from("unexpected version response"));
            }
        }
    }
    Err(String::from("core response event budget exceeded"))
}

#[tauri::command]
fn core_capabilities(state: tauri::State<'_, AppState>) -> Result<Vec<String>, String> {
    let mut guard = state
        .core
        .lock()
        .map_err(|_| String::from("core state unavailable"))?;
    let client = guard
        .as_mut()
        .ok_or_else(|| String::from("core unavailable"))?;
    let request_id = client
        .send_capabilities()
        .map_err(|_| String::from("core request failed"))?;
    for _ in 0..=32 {
        match client.receive().map_err(|_| String::from("core response unavailable"))? {
            InboundEnvelope::Response(ResponseEnvelope::Capabilities(fields))
                if fields.request_id == request_id =>
            {
                return Ok(fields
                    .payload
                    .capabilities
                    .into_vec()
                    .into_iter()
                    .map(|capability| {
                        String::from(match capability {
                            Capability::Health => "health",
                            Capability::Version => "version",
                            Capability::Capabilities => "capabilities",
                            Capability::HealthObservation => "health_observation",
                            Capability::Cancellation => "cancellation",
                        })
                    })
                    .collect());
            }
            InboundEnvelope::Event(_) => continue,
            InboundEnvelope::ProtocolError(_) => {
                return Err(String::from("core protocol error"));
            }
            InboundEnvelope::Response(_) => {
                return Err(String::from("unexpected capabilities response"));
            }
        }
    }
    Err(String::from("core response event budget exceeded"))
}

#[tauri::command]
fn core_observe_health(state: tauri::State<'_, AppState>) -> Result<u64, String> {
    let mut guard = state
        .core
        .lock()
        .map_err(|_| String::from("core state unavailable"))?;
    let client = guard
        .as_mut()
        .ok_or_else(|| String::from("core unavailable"))?;
    let request_id = client
        .send_observe_health()
        .map_err(|_| String::from("core request failed"))?;
    for _ in 0..=32 {
        match client.receive().map_err(|_| String::from("core response unavailable"))? {
            InboundEnvelope::Response(ResponseEnvelope::ObserveHealth(fields))
                if fields.request_id == request_id =>
            {
                return Ok(request_id);
            }
            InboundEnvelope::Event(_) => continue,
            InboundEnvelope::ProtocolError(_) => {
                return Err(String::from("core protocol error"));
            }
            InboundEnvelope::Response(_) => {
                return Err(String::from("unexpected observation response"));
            }
        }
    }
    Err(String::from("core response event budget exceeded"))
}

#[tauri::command]
fn core_cancel_observation(
    state: tauri::State<'_, AppState>,
    request_id: u64,
) -> Result<u64, String> {
    let mut guard = state
        .core
        .lock()
        .map_err(|_| String::from("core state unavailable"))?;
    let client = guard
        .as_mut()
        .ok_or_else(|| String::from("core unavailable"))?;
    let cancel_id = client
        .send_cancel(request_id)
        .map_err(|_| String::from("core request failed"))?;
    for _ in 0..=32 {
        match client.receive().map_err(|_| String::from("core response unavailable"))? {
            InboundEnvelope::Response(ResponseEnvelope::Cancel(fields))
                if fields.request_id == cancel_id =>
            {
                match fields.payload.outcome {
                    CancellationOutcome::Cancelled | CancellationOutcome::AlreadyTerminal => {
                        return Ok(cancel_id);
                    }
                    CancellationOutcome::UnknownTarget => {
                        return Err(String::from("unknown observation target"));
                    }
                }
            }
            InboundEnvelope::Event(_) => continue,
            InboundEnvelope::ProtocolError(_) => {
                return Err(String::from("core protocol error"));
            }
            InboundEnvelope::Response(_) => {
                return Err(String::from("unexpected cancellation response"));
            }
        }
    }
    Err(String::from("core response event budget exceeded"))
}

fn main() {
    let state = AppState {
        core: Mutex::new(CoreClient::start().ok()),
    };
    tauri::Builder::default()
        .manage(state)
        .invoke_handler(tauri::generate_handler![
            core_ready,
            core_health,
            core_version,
            core_capabilities,
            core_observe_health,
            core_cancel_observation
        ])
        .run(tauri::generate_context!())
        .expect("Tauri runtime failed");
}
