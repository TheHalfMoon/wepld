#![forbid(unsafe_code)]

pub mod state;

pub use state::{
    CoreProfile, HandshakeState, MAX_HEALTH_WATCHES, MAX_IN_FLIGHT_REQUESTS, MAX_TERMINAL_RESULTS,
    PendingRequest, StateError,
};
