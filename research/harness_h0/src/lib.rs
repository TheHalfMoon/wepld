#![forbid(unsafe_code)]

//! Bounded research-only identity core for WePLD Harness H0-SCREEN.
//!
//! This crate does not execute screening work, call providers, run containers,
//! or integrate with the WePLD product runtime.

pub mod canonical;
pub mod identity;

pub use canonical::{
    CANONICAL_JSON_VERSION, CanonicalError, MANIFEST_HASH_FIELD,
    canonical_json_bytes, canonical_manifest_payload_bytes,
};
pub use identity::{
    IdentityDomain, IdentityError, Sha256Identity, TrialIdentityInput,
    identity_from_canonical, manifest_identity, trial_identity,
};
