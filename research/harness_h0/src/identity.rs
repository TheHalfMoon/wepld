//! Domain-separated SHA-256 identities and deterministic TrialIdentity.

use crate::canonical::{CanonicalError, canonical_json_bytes, canonical_manifest_payload_bytes};
use serde::{Serialize, Serializer};
use sha2::{Digest, Sha256};
use std::{error::Error, fmt};

const HASH_CONTEXT: &[u8] = b"wepld:h0:identity:v1\0";

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum IdentityDomain {
    ExperimentManifest,
    TaskManifest,
    ModelManifest,
    RecipeManifest,
    EnvironmentManifest,
    VerifierManifest,
    BudgetPolicy,
    EffectEnvelope,
    Trial,
}

impl IdentityDomain {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::ExperimentManifest => "experiment-manifest",
            Self::TaskManifest => "task-manifest",
            Self::ModelManifest => "model-manifest",
            Self::RecipeManifest => "recipe-manifest",
            Self::EnvironmentManifest => "environment-manifest",
            Self::VerifierManifest => "verifier-manifest",
            Self::BudgetPolicy => "budget-policy",
            Self::EffectEnvelope => "effect-envelope",
            Self::Trial => "trial",
        }
    }

    const fn is_manifest(self) -> bool {
        matches!(
            self,
            Self::ExperimentManifest
                | Self::TaskManifest
                | Self::ModelManifest
                | Self::RecipeManifest
                | Self::EnvironmentManifest
                | Self::VerifierManifest
        )
    }
}

#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct Sha256Identity([u8; 32]);

impl Sha256Identity {
    pub const fn from_bytes(bytes: [u8; 32]) -> Self {
        Self(bytes)
    }

    pub const fn as_bytes(&self) -> &[u8; 32] {
        &self.0
    }

    pub fn to_hex(self) -> String {
        const HEX: &[u8; 16] = b"0123456789abcdef";
        let mut out = String::with_capacity(64);
        for byte in self.0 {
            out.push(HEX[(byte >> 4) as usize] as char);
            out.push(HEX[(byte & 0x0f) as usize] as char);
        }
        out
    }

    pub fn from_hex(text: &str) -> Result<Self, DigestParseError> {
        if text.len() != 64 {
            return Err(DigestParseError::Length(text.len()));
        }
        let mut out = [0_u8; 32];
        let bytes = text.as_bytes();
        for (index, slot) in out.iter_mut().enumerate() {
            let at = index * 2;
            let high = hex_nibble(bytes[at]).ok_or(DigestParseError::NonLowercaseHex(at))?;
            let low = hex_nibble(bytes[at + 1]).ok_or(DigestParseError::NonLowercaseHex(at + 1))?;
            *slot = (high << 4) | low;
        }
        Ok(Self(out))
    }
}

impl fmt::Display for Sha256Identity {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(&self.to_hex())
    }
}

impl fmt::Debug for Sha256Identity {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_tuple("Sha256Identity")
            .field(&self.to_hex())
            .finish()
    }
}

impl Serialize for Sha256Identity {
    fn serialize<S: Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        serializer.serialize_str(&self.to_hex())
    }
}

fn hex_nibble(byte: u8) -> Option<u8> {
    match byte {
        b'0'..=b'9' => Some(byte - b'0'),
        b'a'..=b'f' => Some(byte - b'a' + 10),
        _ => None,
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum DigestParseError {
    Length(usize),
    NonLowercaseHex(usize),
}

impl fmt::Display for DigestParseError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Length(length) => write!(f, "SHA-256 hex length must be 64; actual={length}"),
            Self::NonLowercaseHex(index) => {
                write!(f, "SHA-256 must be lowercase hexadecimal; index={index}")
            }
        }
    }
}

impl Error for DigestParseError {}

#[derive(Debug)]
pub enum IdentityError {
    Canonical(CanonicalError),
    ExpectedManifestDomain(IdentityDomain),
}

impl fmt::Display for IdentityError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Canonical(error) => write!(f, "canonical identity input rejected: {error}"),
            Self::ExpectedManifestDomain(domain) => write!(
                f,
                "manifest identity requires manifest domain; actual={}",
                domain.as_str()
            ),
        }
    }
}

impl Error for IdentityError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            Self::Canonical(error) => Some(error),
            Self::ExpectedManifestDomain(_) => None,
        }
    }
}

impl From<CanonicalError> for IdentityError {
    fn from(value: CanonicalError) -> Self {
        Self::Canonical(value)
    }
}

pub fn hash_canonical_bytes(domain: IdentityDomain, bytes: &[u8]) -> Sha256Identity {
    let domain_bytes = domain.as_str().as_bytes();
    let mut hasher = Sha256::new();
    hasher.update(HASH_CONTEXT);
    hasher.update((domain_bytes.len() as u32).to_be_bytes());
    hasher.update(domain_bytes);
    hasher.update((bytes.len() as u64).to_be_bytes());
    hasher.update(bytes);
    Sha256Identity(hasher.finalize().into())
}

pub fn identity_from_canonical<T: Serialize + ?Sized>(
    domain: IdentityDomain,
    value: &T,
) -> Result<Sha256Identity, IdentityError> {
    Ok(hash_canonical_bytes(domain, &canonical_json_bytes(value)?))
}

pub fn manifest_identity<T: Serialize + ?Sized>(
    domain: IdentityDomain,
    hash_material: &T,
) -> Result<Sha256Identity, IdentityError> {
    if !domain.is_manifest() {
        return Err(IdentityError::ExpectedManifestDomain(domain));
    }
    Ok(hash_canonical_bytes(
        domain,
        &canonical_manifest_payload_bytes(hash_material)?,
    ))
}

/// Exactly the comparison-cell fields frozen by the H0 evidence contract.
/// Schedule position, timestamps, runner metadata, mutable labels, and outcomes
/// are absent and therefore cannot perturb TrialIdentity.
#[derive(Debug, Clone, Copy, Serialize)]
pub struct TrialIdentityInput {
    pub experiment_manifest_hash: Sha256Identity,
    pub task_manifest_hash: Sha256Identity,
    pub model_manifest_hash: Sha256Identity,
    pub recipe_manifest_hash: Sha256Identity,
    pub environment_manifest_hash: Sha256Identity,
    pub verifier_manifest_hash: Sha256Identity,
    pub attempt_number: u64,
    pub seed_if_supported: Option<u64>,
}

pub fn trial_identity(input: &TrialIdentityInput) -> Result<Sha256Identity, IdentityError> {
    identity_from_canonical(IdentityDomain::Trial, input)
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde::Serialize;

    fn digest(byte: u8) -> Sha256Identity {
        Sha256Identity::from_bytes([byte; 32])
    }

    fn sample_trial() -> TrialIdentityInput {
        TrialIdentityInput {
            experiment_manifest_hash: digest(1),
            task_manifest_hash: digest(2),
            model_manifest_hash: digest(3),
            recipe_manifest_hash: digest(4),
            environment_manifest_hash: digest(5),
            verifier_manifest_hash: digest(6),
            attempt_number: 1,
            seed_if_supported: Some(7),
        }
    }

    #[test]
    fn digest_hex_is_exact_lowercase() {
        let identity = digest(0xab);
        let hex = identity.to_hex();
        assert_eq!(hex, "ab".repeat(32));
        assert_eq!(Sha256Identity::from_hex(&hex).unwrap(), identity);
        assert!(Sha256Identity::from_hex(&hex.to_uppercase()).is_err());
    }

    #[derive(Serialize)]
    struct Demo<'a> {
        task_id: &'a str,
        revision: u64,
    }

    #[test]
    fn manifest_domains_are_separated_and_validated() {
        let demo = Demo {
            task_id: "task-1",
            revision: 1,
        };
        let task = manifest_identity(IdentityDomain::TaskManifest, &demo).unwrap();
        let model = manifest_identity(IdentityDomain::ModelManifest, &demo).unwrap();
        assert_ne!(task, model);
        assert!(matches!(
            manifest_identity(IdentityDomain::Trial, &demo).unwrap_err(),
            IdentityError::ExpectedManifestDomain(IdentityDomain::Trial)
        ));
        assert!(matches!(
            manifest_identity(
                IdentityDomain::TaskManifest,
                &serde_json::json!({"manifest_hash": task.to_hex()})
            )
            .unwrap_err(),
            IdentityError::Canonical(CanonicalError::ManifestHashFieldPresent)
        ));
    }

    #[test]
    fn trial_identity_is_deterministic_and_cell_bound() {
        let input = sample_trial();
        let first = trial_identity(&input).unwrap();
        assert_eq!(first, trial_identity(&input).unwrap());

        let mut changed = input;
        changed.recipe_manifest_hash = digest(9);
        assert_ne!(first, trial_identity(&changed).unwrap());

        let mut changed = input;
        changed.attempt_number = 2;
        assert_ne!(first, trial_identity(&changed).unwrap());

        let mut changed = input;
        changed.seed_if_supported = None;
        assert_ne!(first, trial_identity(&changed).unwrap());
    }

    #[test]
    fn framing_and_domains_prevent_aliases() {
        assert_ne!(
            hash_canonical_bytes(IdentityDomain::TaskManifest, b"ab"),
            hash_canonical_bytes(IdentityDomain::TaskManifest, b"a")
        );
        assert_ne!(
            hash_canonical_bytes(IdentityDomain::TaskManifest, b"ab"),
            hash_canonical_bytes(IdentityDomain::ModelManifest, b"ab")
        );
    }
}
