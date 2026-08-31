#![forbid(unsafe_code)]

//! S2 local evidence store.
//!
//! The store persists immutable project generations under a WePLD-owned local
//! data root. A generation is written completely, validated, synced, and only
//! then published by atomically replacing a small `CURRENT` pointer. Readers
//! read `CURRENT` once and validate exactly that generation; records are never
//! combined across generations.
//!
//! Immutability is enforced rather than asserted. Writing the manifest closes a
//! generation, and every later record or manifest write targeting that
//! generation is rejected with [`StoreError::GenerationAlreadyClosed`]. Without
//! that rule a caller holding the correct project lock could rewrite a
//! published generation in place, which would turn an immutability guarantee
//! into a digest mismatch surfaced to an unlucky reader.
//!
//! Covered tasks: S2-E003, S2-E004, S2-E005, S2-E006, S2-E007, S2-E008,
//! S2-E009, S2-E010, S2-E011, S2-E012, S2-E017.
//!
//! # Authenticity boundary (S2-E017)
//!
//! Every integrity mechanism here is unkeyed: schema versions, SHA-256 content
//! digests, manifest reference checks, and bounded reads. Together they detect
//! corruption, truncation, torn writes, and incoherent generations. They do
//! **not** authenticate the store against an actor who already has writer access
//! to the complete store: such an actor can forge an internally self-consistent
//! generation. This limitation is reported by
//! [`StoreAuthenticity::UnauthenticatedStructuralCoherenceOnly`] and must not be
//! described as tamper evidence. Any authenticated trust anchor requires
//! separate planning and authority.
//!
//! # Effect boundary
//!
//! The store reads and writes only inside its own data root. It never deletes
//! files: superseded and interrupted artifacts remain as orphans for recovery
//! and are never promoted. It executes no process, performs no network effect,
//! and calls no version-control tooling.

use std::cell::Cell;
use std::error::Error;
use std::ffi::OsString;
use std::fmt;
use std::fs::{self, File, OpenOptions, TryLockError};
use std::io::{self, Read as _, Write as _};
use std::marker::PhantomData;
use std::path::{Component, MAIN_SEPARATOR_STR, Path, PathBuf};
use std::thread;
use std::time::{Duration, Instant, SystemTime, UNIX_EPOCH};

use sha2::{Digest as _, Sha256};
use wepld_contracts::{
    ContentDigest, ContractValueError, EvidenceStatus, FreshnessBasis, GenerationId,
    IdentityCatalogReservation, ProjectContractCodecError, ProjectContractVersion,
    ProjectCurrentRef, ProjectGenerationManifest, ProjectId, RecordDigest, RecordDigestList,
    RecordId, StoreAuthenticity, StoreLockScope, UnixMillis, canonical_project_json,
    decode_project_json,
};

use crate::identity::IdentityError;

/// Hard deadline for acquiring any store lock. S2-E005.
pub const LOCK_ACQUIRE_DEADLINE_MS: u64 = 2000;

/// Polling interval used while a store lock is contended. S2-E005.
pub const LOCK_POLL_INTERVAL_MS: u64 = 25;

/// Maximum bytes read for any single evidence record. S2-E004.
pub const MAX_RECORD_BYTES: usize = 1_048_576;

/// Maximum bytes read for a generation manifest. S2-E004.
pub const MAX_MANIFEST_BYTES: usize = 1_048_576;

/// Maximum bytes read for the `CURRENT` pointer. S2-E004.
pub const MAX_CURRENT_BYTES: usize = 65_536;

/// Producer contract version recorded in manifests written by this module.
pub const PRODUCER_CONTRACT_VERSION: u16 = 1;

const CATALOG_DIR: &str = "catalog";
const CATALOG_LOCK_FILE: &str = "catalog.lock";
const RESERVATIONS_DIR: &str = "reservations";
const PROJECTS_DIR: &str = "projects";
const PROJECT_LOCK_FILE: &str = "project.lock";
const GENERATIONS_DIR: &str = "generations";
const RECORDS_DIR: &str = "records";
const MANIFEST_FILE: &str = "manifest.json";
const CURRENT_FILE: &str = "CURRENT";
const TEMP_DIR: &str = "tmp";
const JSON_SUFFIX: &str = ".json";
const TEMP_SUFFIX: &str = ".tmp";

/// Classification of a store defect. S2-E010.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum StoreDefect {
    /// `CURRENT` is absent; the project store has no published generation.
    CurrentMissing,
    /// `CURRENT` exists but is not a usable pointer record: it does not decode,
    /// it exceeds its bounded read size, or it names a generation this store
    /// could never have addressed.
    ///
    /// The last case is reachable because the contract identifier charset is
    /// wider than the path projection. A persisted pointer carrying such an
    /// identifier is a defective pointer rather than a caller argument fault, so
    /// it is classified here and not as [`StoreError::UnsafeIdentifier`].
    CurrentCorrupt,
    /// `CURRENT` names a generation whose directory or manifest is absent.
    /// This is the signature of a crash between generation write and publish.
    CurrentDanglingGeneration,
    /// The manifest does not decode, or exceeds its bounded read size.
    ///
    /// Both are properties of the bytes on disk, so both are store defects. A
    /// bounded-read refusal is a caller-input error only when the caller itself
    /// supplied the oversized value.
    ManifestCorrupt,
    /// The manifest digest recorded in `CURRENT` does not match the manifest.
    ManifestDigestMismatch,
    /// A generation exists but carries no manifest, so it was never closed.
    ///
    /// This is the residue of an interrupted write. It is distinct from
    /// [`Self::CurrentDanglingGeneration`], which is specifically about a
    /// published pointer naming a generation that cannot be resolved; a
    /// generation can be unclosed while no pointer names it at all.
    GenerationManifestMissing,
    /// The manifest references a record that is not present.
    RecordMissing,
    /// A record does not decode, or exceeds its bounded read size.
    RecordCorrupt,
    /// A record digest does not match the manifest entry, which is the
    /// signature of a torn or partially written record.
    RecordDigestMismatch,
    /// The manifest omits a digest for a record it references.
    RecordDigestMissing,
    /// A persisted record describes a different project than the path it was
    /// read from. This covers a generation manifest and a catalog reservation
    /// alike: both name their project twice, and the two names must agree.
    ProjectMismatch,
    /// A schema version outside the supported contract range was persisted.
    ///
    /// # Currently unreachable, and why that is recorded rather than implied
    ///
    /// The contract codec rejects an unknown `schema_version` while decoding, so
    /// a persisted record carrying a future version fails to decode and surfaces
    /// as the corresponding corruption class instead of this one. The explicit
    /// version checks in this module are fail-closed guards that no current
    /// input can reach.
    ///
    /// Separating the two would mean reading the version before decoding the
    /// whole record, which needs either a version-tolerant decoder in the
    /// contract layer or a JSON parser of this module's own. This tranche holds
    /// authority for neither, so the gap is stated, and the classification a
    /// future version actually receives today is pinned by test rather than
    /// assumed.
    UnsupportedSchemaVersion,
    /// The manifest was written by a producer contract this reader does not
    /// support.
    ///
    /// The producer contract version records what the writer meant by the
    /// fields, which the serialization schema version does not capture. A reader
    /// that accepted any value would make the field decorative and would
    /// silently adopt a generation whose semantics it does not implement.
    UnsupportedProducerContractVersion,
}

impl fmt::Display for StoreDefect {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        let text = match self {
            Self::CurrentMissing => "no published generation pointer",
            Self::CurrentCorrupt => "current generation pointer is corrupt",
            Self::CurrentDanglingGeneration => "current pointer names a missing generation",
            Self::GenerationManifestMissing => "generation has no manifest and was never closed",
            Self::ManifestCorrupt => "generation manifest is corrupt",
            Self::ManifestDigestMismatch => "generation manifest digest mismatch",
            Self::RecordMissing => "referenced evidence record is missing",
            Self::RecordCorrupt => "evidence record is corrupt",
            Self::RecordDigestMismatch => "evidence record digest mismatch",
            Self::RecordDigestMissing => "manifest omits a digest for a referenced record",
            Self::ProjectMismatch => "generation manifest describes a different project",
            Self::UnsupportedSchemaVersion => "persisted schema version is unsupported",
            Self::UnsupportedProducerContractVersion => {
                "generation was written by an unsupported producer contract"
            }
        };
        formatter.write_str(text)
    }
}

#[derive(Debug)]
pub enum StoreError {
    /// A bounded lock deadline elapsed. Stable busy result, never a wait.
    Busy {
        scope: StoreLockScope,
    },
    /// The caller cancelled the operation while waiting for a lock.
    Cancelled {
        scope: StoreLockScope,
    },
    /// A structural defect was detected. S2-E010.
    Defect(StoreDefect),
    /// A bounded read limit was exceeded before parsing. S2-E004.
    TooLarge {
        limit: usize,
    },
    /// An opaque identifier could not be projected to a safe path. S2-E003.
    UnsafeIdentifier,
    /// The store root is not an absolute path.
    ///
    /// A relative root resolves against the process working directory, so one
    /// store handle would address different locations depending on when it was
    /// used, and creating the skeleton would put directories wherever the
    /// process happened to be. A Windows drive-relative root such as `C:work` is
    /// equally unanchored, because it resolves against a per-drive current
    /// directory; `Path::is_absolute` refuses both.
    RelativeStoreRoot,
    /// A project lock guard was presented for a different project.
    WrongProjectLock,
    /// A lock guard was presented that protects a different store root.
    ForeignLock,
    /// A write targeted a generation that is already closed by a manifest.
    ///
    /// Generations are immutable once closed. Rewriting a closed generation
    /// would let a published generation change underneath a reader that already
    /// selected it.
    GenerationAlreadyClosed,
    /// The canonical catalog-before-project lock order was violated.
    ///
    /// Canonical authority fixes the order when an operation needs both locks.
    /// Acquiring the catalog lock while the **calling thread** already holds any
    /// project lock is refused rather than allowed to invert the order. The
    /// refusal does not depend on which store root either guard names, because
    /// two roots can address one store.
    LockOrderViolation,
    Identity(IdentityError),
    Contract(ContractValueError),
    Codec(ProjectContractCodecError),
    Io(io::Error),
}

impl fmt::Display for StoreError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Busy { scope } => write!(formatter, "{} is busy", scope_name(*scope)),
            Self::Cancelled { scope } => {
                write!(
                    formatter,
                    "{} acquisition was cancelled",
                    scope_name(*scope)
                )
            }
            Self::Defect(defect) => write!(formatter, "evidence store defect: {defect}"),
            Self::TooLarge { limit } => {
                write!(formatter, "stored value exceeds bounded read limit {limit}")
            }
            Self::UnsafeIdentifier => {
                write!(formatter, "opaque identifier is not safe as a path segment")
            }
            Self::RelativeStoreRoot => {
                write!(formatter, "store root must be an absolute path")
            }
            Self::WrongProjectLock => write!(
                formatter,
                "project lock guard does not name the project being mutated"
            ),
            Self::ForeignLock => write!(
                formatter,
                "lock guard protects a different store root than the one being mutated"
            ),
            Self::GenerationAlreadyClosed => write!(
                formatter,
                "generation is closed by a manifest and is immutable"
            ),
            Self::LockOrderViolation => write!(
                formatter,
                "canonical lock order requires the identity catalog lock before a project lock"
            ),
            Self::Identity(error) => write!(formatter, "identity error: {error}"),
            Self::Contract(error) => write!(formatter, "contract value error: {error}"),
            Self::Codec(error) => write!(formatter, "contract codec error: {error}"),
            Self::Io(error) => write!(formatter, "input/output error: {error}"),
        }
    }
}

impl Error for StoreError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            Self::Io(error) => Some(error),
            Self::Identity(error) => Some(error),
            _ => None,
        }
    }
}

fn scope_name(scope: StoreLockScope) -> &'static str {
    match scope {
        StoreLockScope::IdentityCatalog => "identity catalog",
        StoreLockScope::ProjectStore => "project store",
    }
}

/// Stable machine error class for a busy scope.
///
/// These strings are part of the command-plane error contract.
pub fn busy_error_code(scope: StoreLockScope) -> &'static str {
    match scope {
        StoreLockScope::IdentityCatalog => "identity_catalog_busy",
        StoreLockScope::ProjectStore => "store_busy",
    }
}

impl From<io::Error> for StoreError {
    fn from(error: io::Error) -> Self {
        Self::Io(error)
    }
}

impl From<IdentityError> for StoreError {
    fn from(error: IdentityError) -> Self {
        Self::Identity(error)
    }
}

impl From<ContractValueError> for StoreError {
    fn from(error: ContractValueError) -> Self {
        Self::Contract(error)
    }
}

impl From<ProjectContractCodecError> for StoreError {
    fn from(error: ProjectContractCodecError) -> Self {
        Self::Codec(error)
    }
}

/// Lexically normalise a store root so equivalent spellings share one identity.
///
/// `.` components are dropped and `..` components pop the previous normal
/// component. A `..` that would climb above an absolute root is discarded,
/// because both POSIX and Windows resolve it to the root itself; leaving it
/// would keep two spellings of one location distinct and would name nothing.
/// For a relative path a leading `..` is meaningful and is preserved.
///
/// The relative-path branches below are unreachable through the public API,
/// because [`EvidenceStore::new`] refuses a root that is not absolute. They are
/// kept so the function is total and correct on its own terms rather than
/// correct only because of a caller's precondition.
///
/// Normalisation is purely lexical and therefore deterministic and independent
/// of whether the directory exists. It does not resolve symbolic links, so two
/// roots that alias through a link remain distinct store identities. The
/// operating-system lock still provides mutual exclusion in that case, but
/// mutual exclusion is not ordering, so the lock-order rule deliberately does
/// not depend on this identity at all: it counts project guards held by the
/// calling thread without regard to root.
fn normalize_root(root: PathBuf) -> PathBuf {
    let mut parts: Vec<Component<'_>> = Vec::new();
    let mut rooted = false;
    let mut depth: usize = 0;
    for component in root.components() {
        match component {
            Component::CurDir => {}
            Component::ParentDir => {
                if depth > 0 {
                    parts.pop();
                    depth -= 1;
                } else if !rooted {
                    parts.push(component);
                }
            }
            Component::RootDir => {
                rooted = true;
                parts.push(component);
            }
            // A Windows prefix alone does not make a path rooted: `C:a` is
            // drive-relative, so a following parent component is meaningful.
            Component::Prefix(_) => parts.push(component),
            Component::Normal(_) => {
                parts.push(component);
                depth += 1;
            }
        }
    }
    // Reassemble explicitly. Pushing a component whose text parses as a Windows
    // prefix would replace the whole accumulated path, so a directory named
    // `C:` would re-root the store and a verbatim prefix would be corrupted into
    // a drive-relative path.
    let mut assembled = OsString::new();
    let mut need_separator = false;
    for component in parts {
        match component {
            Component::Prefix(prefix) => {
                assembled.push(prefix.as_os_str());
                need_separator = false;
            }
            Component::RootDir => {
                assembled.push(MAIN_SEPARATOR_STR);
                need_separator = false;
            }
            other => {
                if need_separator {
                    assembled.push(MAIN_SEPARATOR_STR);
                }
                assembled.push(other.as_os_str());
                need_separator = true;
            }
        }
    }
    if assembled.is_empty() {
        return PathBuf::from(".");
    }
    PathBuf::from(assembled)
}

// Number of project guards held by the current thread.
//
// Canonical clarification Q26 fixes catalog-before-project ordering whenever a
// single operation needs both locks, while explicitly permitting a project-only
// lock for ordinary updates. The constraint is therefore a property of one
// caller, not of the whole process: a thread holding only the project lock and
// a different thread holding only the catalog lock is two single-resource
// operations, not an inverted acquisition.
//
// Tracking this per thread rather than per process makes the check exact and
// removes a race. A process-wide count had to be read and released before the
// operating-system acquisition, so another thread could register between the
// check and the acquisition; per-thread state cannot be mutated by another
// thread, so the check and the acquisition cannot interleave with anything that
// would change the answer.
//
// It is also no longer over-strict: an unrelated thread's project work no
// longer blocks catalog acquisition, which the process-wide count refused.
//
// The count is deliberately not keyed by store root. Keying it that way left
// the rule evadable, because store identity here is lexical: the same thread
// could hold a project guard taken through one root spelling and then pass the
// catalog check by naming a second root. Two roots that differ lexically can
// address one physical store through a symbolic link, in which case the two
// guards are the same pair of lock files acquired in the inverted order while
// the check saw nothing. Q26 constrains the caller that ends up holding both
// lock kinds, so the only question the check may ask is whether this thread
// holds a project guard at all.
thread_local! {
    static HELD_PROJECT_LOCKS: Cell<usize> = const { Cell::new(0) };
}

fn this_thread_holds_a_project_lock() -> bool {
    HELD_PROJECT_LOCKS.with(|held| held.get() > 0)
}

fn register_project_lock() {
    HELD_PROJECT_LOCKS.with(|held| held.set(held.get().saturating_add(1)));
}

fn release_project_lock() {
    HELD_PROJECT_LOCKS.with(|held| held.set(held.get().saturating_sub(1)));
}

/// A registry entry held while a project lock acquisition is in flight.
///
/// Registration must happen before the operating-system lock is taken, or the
/// calling thread could pass its own catalog-order check inside that window.
/// Holding it as a guard means the release runs on every exit path, including a
/// panic unwinding out of a caller-supplied cancellation callback.
struct PendingProjectLock {
    armed: bool,
}

impl PendingProjectLock {
    fn register() -> Self {
        register_project_lock();
        Self { armed: true }
    }

    /// Hand ownership of the registry entry to a constructed `ProjectLock`.
    fn into_owned(mut self) {
        self.armed = false;
    }
}

impl Drop for PendingProjectLock {
    fn drop(&mut self) {
        if self.armed {
            release_project_lock();
        }
    }
}

const HEX_DIGITS: &[u8; 16] = b"0123456789abcdef";

fn hex_lower(bytes: &[u8]) -> String {
    let mut rendered = String::with_capacity(bytes.len() * 2);
    for byte in bytes {
        rendered.push(char::from(HEX_DIGITS[usize::from(byte >> 4)]));
        rendered.push(char::from(HEX_DIGITS[usize::from(byte & 0x0f)]));
    }
    rendered
}

/// Digest bytes with SHA-256 and render the contract digest value.
///
/// The digest is unkeyed corruption/coherence evidence only. See S2-E017.
pub fn content_digest(bytes: &[u8]) -> Result<ContentDigest, StoreError> {
    let mut hasher = Sha256::new();
    hasher.update(bytes);
    Ok(ContentDigest::sha256(hex_lower(&hasher.finalize()))?)
}

/// Project an opaque identifier onto a single safe path segment. S2-E003.
///
/// The contract charset admits `:` and `.`, which are unsafe as filesystem path
/// segments: `:` selects an alternate data stream on Windows and `.`/`..` are
/// directory traversal. This projection therefore accepts a strictly narrower
/// set than the contract and fails closed on anything else. It never accepts a
/// separator, so an identifier can only ever name a leaf inside its parent.
pub fn safe_path_segment(identifier: &str) -> Result<String, StoreError> {
    if identifier.is_empty() || identifier.len() > 128 {
        return Err(StoreError::UnsafeIdentifier);
    }
    if identifier == "." || identifier == ".." {
        return Err(StoreError::UnsafeIdentifier);
    }
    if identifier.starts_with('.') || identifier.starts_with('-') {
        return Err(StoreError::UnsafeIdentifier);
    }
    let safe = identifier
        .bytes()
        .all(|byte| byte.is_ascii_alphanumeric() || matches!(byte, b'_' | b'-'));
    if !safe {
        return Err(StoreError::UnsafeIdentifier);
    }
    Ok(identifier.to_owned())
}

/// A WePLD-owned local store rooted at a per-user data directory.
#[derive(Debug, Clone)]
pub struct EvidenceStore {
    root: PathBuf,
}

/// A held store lock. Dropping the guard releases the operating-system lock.
///
/// Ownership is determined by the operating system lock, never by the presence
/// of a lock file. A crashed process releases its lock when its handles close,
/// so a stale lock file never blocks ownership recovery. See S2-E015.
#[derive(Debug)]
pub struct StoreLock {
    file: File,
    scope: StoreLockScope,
}

impl StoreLock {
    pub fn scope(&self) -> StoreLockScope {
        self.scope
    }
}

impl Drop for StoreLock {
    fn drop(&mut self) {
        let _ = self.file.unlock();
    }
}

/// Proof that the caller holds the store-wide identity catalog lock.
///
/// Catalog mutation requires this guard by type, so the locking protocol is
/// enforced by the API rather than only documented.
#[derive(Debug)]
pub struct CatalogLock {
    inner: StoreLock,
    root: PathBuf,
}

impl CatalogLock {
    pub fn scope(&self) -> StoreLockScope {
        self.inner.scope()
    }

    /// The store root this guard actually protects.
    pub fn root(&self) -> &Path {
        &self.root
    }

    fn require_store(&self, store: &EvidenceStore) -> Result<(), StoreError> {
        if self.root != store.root {
            return Err(StoreError::ForeignLock);
        }
        Ok(())
    }

    /// Acquire the project lock in the canonical order while holding this guard.
    ///
    /// S2-I011 fixes catalog-before-project. Reaching a project lock through the
    /// held catalog guard makes the ordered path the natural one and keeps the
    /// two guards bound to the same store.
    pub fn lock_project(
        &self,
        store: &EvidenceStore,
        project: &ProjectId,
        cancelled: &dyn Fn() -> bool,
    ) -> Result<ProjectLock, StoreError> {
        self.require_store(store)?;
        store.lock_project(project, cancelled)
    }
}

/// Proof that the caller holds the per-project store lock for one exact project.
///
/// Project mutation and publication require this guard by type, and every such
/// operation checks that the guard names the project being mutated. Holding the
/// guard across validation and the `CURRENT` replacement is what closes the
/// validate-then-publish window.
#[derive(Debug)]
pub struct ProjectLock {
    inner: StoreLock,
    project: ProjectId,
    root: PathBuf,
    /// Keeps the guard on its acquiring thread.
    ///
    /// Ordering accounting is thread-local, so moving a guard to another thread
    /// would leave the releasing thread decrementing a count it never
    /// incremented while the acquiring thread kept one forever. Making the guard
    /// `!Send` removes that possibility rather than documenting it.
    _not_send: PhantomData<*const ()>,
}

impl ProjectLock {
    pub fn scope(&self) -> StoreLockScope {
        self.inner.scope()
    }

    pub fn project(&self) -> &ProjectId {
        &self.project
    }

    /// The store root this guard actually protects.
    pub fn root(&self) -> &Path {
        &self.root
    }

    /// A guard proves an operation is protected only when it names both the
    /// store it was taken from and the project being mutated.
    ///
    /// Checking the project alone is insufficient: a guard taken from one store
    /// root would otherwise appear to protect a mutation applied to a different
    /// root, where no lock is actually held.
    fn require(&self, store: &EvidenceStore, project: &ProjectId) -> Result<(), StoreError> {
        if self.root != store.root {
            return Err(StoreError::ForeignLock);
        }
        if &self.project != project {
            return Err(StoreError::WrongProjectLock);
        }
        Ok(())
    }
}

impl Drop for ProjectLock {
    fn drop(&mut self) {
        release_project_lock();
    }
}

/// Result of reading the published generation. S2-E009.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PublishedGeneration {
    pub current: ProjectCurrentRef,
    pub manifest: ProjectGenerationManifest,
}

/// Freshness of a published generation relative to an observation time. S2-E011.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Freshness {
    pub basis: FreshnessBasis,
    pub status: EvidenceStatus,
    pub age_millis: u64,
}

impl EvidenceStore {
    /// Open a store rooted at an absolute WePLD-owned data root.
    ///
    /// A root that is not absolute is refused with
    /// [`StoreError::RelativeStoreRoot`] before any store handle exists. The
    /// requirement used to be documentation only, which meant a relative root
    /// was accepted and every later path resolved against the process working
    /// directory: the same handle would address different locations at different
    /// times, and [`Self::initialize`] would create the skeleton wherever the
    /// process happened to be. Refusing at construction is what makes the
    /// documented contract true.
    ///
    /// The root is lexically normalised once, here, so that two handles naming
    /// the same directory with different spellings share one store identity.
    /// Without this, `/state/wepld` and `/state/wepld/.` would be distinct
    /// registry keys and distinct guard bindings while addressing the same lock
    /// files, which would both bypass lock-order enforcement and make a valid
    /// guard look foreign.
    ///
    /// Normalisation is purely lexical and therefore deterministic and
    /// independent of whether the directory exists yet. It resolves `.` and
    /// `..` components. It does not resolve symbolic links, so two roots that
    /// alias through a link remain distinct store identities; the
    /// operating-system lock still provides mutual exclusion in that case, and
    /// acquisition remains bounded.
    ///
    /// Lock ordering does not rely on that identity. Counting held project
    /// guards per root would have made the ordering rule evadable by naming a
    /// second root, a symbolic-link alias of the same physical store included,
    /// so the ordering check is root-independent. See [`Self::lock_catalog`].
    pub fn new(root: impl Into<PathBuf>) -> Result<Self, StoreError> {
        let root = root.into();
        if !root.is_absolute() {
            return Err(StoreError::RelativeStoreRoot);
        }
        Ok(Self {
            root: normalize_root(root),
        })
    }

    pub fn root(&self) -> &Path {
        &self.root
    }

    fn catalog_dir(&self) -> PathBuf {
        self.root.join(CATALOG_DIR)
    }

    fn reservations_dir(&self) -> PathBuf {
        self.catalog_dir().join(RESERVATIONS_DIR)
    }

    fn project_dir(&self, project: &ProjectId) -> Result<PathBuf, StoreError> {
        let segment = safe_path_segment(project.as_str())?;
        Ok(self.root.join(PROJECTS_DIR).join(segment))
    }

    fn generation_dir(
        &self,
        project: &ProjectId,
        generation: &GenerationId,
    ) -> Result<PathBuf, StoreError> {
        let segment = safe_path_segment(generation.as_str())?;
        Ok(self
            .project_dir(project)?
            .join(GENERATIONS_DIR)
            .join(segment))
    }

    /// Create the store skeleton. Directory creation is idempotent.
    pub fn initialize(&self) -> Result<(), StoreError> {
        fs::create_dir_all(self.reservations_dir())?;
        fs::create_dir_all(self.root.join(PROJECTS_DIR))?;
        Ok(())
    }

    fn lock_path(
        &self,
        scope: StoreLockScope,
        project: Option<&ProjectId>,
    ) -> Result<PathBuf, StoreError> {
        match scope {
            StoreLockScope::IdentityCatalog => Ok(self.catalog_dir().join(CATALOG_LOCK_FILE)),
            StoreLockScope::ProjectStore => match project {
                Some(project) => Ok(self.project_dir(project)?.join(PROJECT_LOCK_FILE)),
                None => Err(StoreError::UnsafeIdentifier),
            },
        }
    }

    /// Acquire a bounded, cancellable exclusive lock. S2-E005.
    ///
    /// The call polls a non-blocking `try_lock` every
    /// [`LOCK_POLL_INTERVAL_MS`] until [`LOCK_ACQUIRE_DEADLINE_MS`] elapses, then
    /// returns a stable busy result. It never waits indefinitely and never
    /// interprets lock-file existence as ownership.
    ///
    /// The deadline bounds the polling loop, not wall-clock time. Sleep
    /// granularity, scheduling, directory creation, and the initial file open
    /// can each add time beyond it, so the deadline is an algorithmic bound
    /// rather than a hard real-time guarantee. Cancellation is observed once per
    /// poll, so cancellation latency is up to one poll interval.
    ///
    /// Callers that need both locks must acquire the identity catalog lock
    /// before the project lock. That order is fixed to prevent deadlock.
    fn acquire_lock(
        &self,
        scope: StoreLockScope,
        project: Option<&ProjectId>,
        cancelled: &dyn Fn() -> bool,
    ) -> Result<StoreLock, StoreError> {
        let path = self.lock_path(scope, project)?;
        if let Some(parent) = path.parent() {
            fs::create_dir_all(parent)?;
        }
        let file = OpenOptions::new()
            .read(true)
            .write(true)
            .create(true)
            .truncate(false)
            .open(&path)?;

        let deadline = Instant::now() + Duration::from_millis(LOCK_ACQUIRE_DEADLINE_MS);
        loop {
            if cancelled() {
                return Err(StoreError::Cancelled { scope });
            }
            match file.try_lock() {
                Ok(()) => return Ok(StoreLock { file, scope }),
                Err(TryLockError::WouldBlock) => {}
                Err(TryLockError::Error(error)) => return Err(StoreError::Io(error)),
            }
            if Instant::now() >= deadline {
                return Err(StoreError::Busy { scope });
            }
            thread::sleep(Duration::from_millis(LOCK_POLL_INTERVAL_MS));
        }
    }

    /// Acquire the store-wide identity catalog lock. S2-E005, S2-I011.
    ///
    /// Canonical clarification Q26 fixes catalog-before-project ordering when a
    /// single operation needs both locks. That is a property of one caller, so
    /// this refuses with [`StoreError::LockOrderViolation`] when the **calling
    /// thread** already holds any project guard.
    ///
    /// The refusal is deliberately independent of which root either guard
    /// names. Store identity here is lexical, so a per-root check could be
    /// evaded by naming a second root while the first guard is still held, and
    /// two lexically distinct roots can address one physical store through a
    /// symbolic link. In that case the same pair of lock files would be taken in
    /// the inverted order with the check seeing nothing. The cost of the wider
    /// rule is that one thread cannot hold a project guard on one store while
    /// taking the catalog lock on another; that combination is precisely the
    /// both-locks case Q26 orders, so refusing it is the rule rather than an
    /// over-restriction.
    ///
    /// A different thread holding only a project lock does not block this call.
    /// Those are two single-resource operations, not an inverted acquisition,
    /// and refusing them would be stricter than canonical authority requires.
    ///
    /// The check reads thread-local state, so no other thread can change the
    /// answer between the check and the acquisition. A process-wide count could
    /// not offer that: it had to be read and released before the
    /// operating-system call, leaving a window in which another thread
    /// registered.
    pub fn lock_catalog(&self, cancelled: &dyn Fn() -> bool) -> Result<CatalogLock, StoreError> {
        if this_thread_holds_a_project_lock() {
            return Err(StoreError::LockOrderViolation);
        }
        Ok(CatalogLock {
            inner: self.acquire_lock(StoreLockScope::IdentityCatalog, None, cancelled)?,
            root: self.root.clone(),
        })
    }

    /// Acquire the per-project store lock for one exact project. S2-E005.
    ///
    /// Use this only for operations that need no catalog access. A caller that
    /// also needs the catalog lock must use [`Self::lock_catalog_then_project`]
    /// or [`CatalogLock::lock_project`]. Acquiring the catalog lock while
    /// already holding a project lock inverts the canonical order and is
    /// prohibited: [`Self::lock_catalog`] returns
    /// [`StoreError::LockOrderViolation`] immediately for that caller, without
    /// waiting and without a busy result. A stable busy result is what ordinary
    /// contention produces, including a second process that ignores the order;
    /// the two outcomes are not interchangeable.
    pub fn lock_project(
        &self,
        project: &ProjectId,
        cancelled: &dyn Fn() -> bool,
    ) -> Result<ProjectLock, StoreError> {
        // Register the pending acquisition before taking the operating-system
        // lock. Registering afterwards leaves a window in which another thread
        // passes the catalog-order check while this project lock is already
        // held, which inverts the canonical order without the registry ever
        // seeing it.
        //
        // The registration is an RAII guard rather than a bare call, so it is
        // released on every exit path: a refused acquisition, an error, and a
        // panic unwinding out of the caller-supplied cancellation callback.
        let pending = PendingProjectLock::register();
        let inner = self.acquire_lock(StoreLockScope::ProjectStore, Some(project), cancelled)?;
        let guard = ProjectLock {
            inner,
            project: project.clone(),
            root: self.root.clone(),
            _not_send: PhantomData,
        };
        pending.into_owned();
        Ok(guard)
    }

    /// Acquire both locks in the canonical order: catalog first, then project.
    ///
    /// S2-I011 fixes this order to prevent deadlock.
    ///
    /// # Enforcement boundary
    ///
    /// This is the supported way to obtain both guards, and
    /// [`CatalogLock::lock_project`] is the only route to a project guard from a
    /// held catalog guard. The ordering is **not** fully enforced by the type
    /// system: [`Self::lock_project`] remains public because project-only
    /// operations legitimately need it, so a caller could still take a project
    /// guard first and then call [`Self::lock_catalog`].
    ///
    /// That residual case is stated rather than papered over. Within one
    /// process it is caught: the reversing thread is refused with
    /// [`StoreError::LockOrderViolation`] rather than being allowed to invert
    /// the order. Across processes there is no shared registry, so a second
    /// process can genuinely take the locks in the reverse order; that case
    /// cannot deadlock, because every acquisition is bounded and fails with a
    /// stable busy result after the deadline instead of waiting forever.
    ///
    /// Expressing the prohibition in the type system would require a session or
    /// type-state design that makes concurrent project work in one process
    /// impossible, which costs more than the residual risk.
    pub fn lock_catalog_then_project(
        &self,
        project: &ProjectId,
        cancelled: &dyn Fn() -> bool,
    ) -> Result<(CatalogLock, ProjectLock), StoreError> {
        let catalog = self.lock_catalog(cancelled)?;
        let project_lock = catalog.lock_project(self, project, cancelled)?;
        Ok((catalog, project_lock))
    }

    /// Read a whole file under a bounded limit. S2-E004.
    ///
    /// The limit is enforced while reading, so an oversized or endlessly growing
    /// file cannot exhaust memory before parsing.
    fn read_bounded(path: &Path, limit: usize) -> Result<Option<Vec<u8>>, StoreError> {
        let mut file = match File::open(path) {
            Ok(file) => file,
            Err(error) if error.kind() == io::ErrorKind::NotFound => return Ok(None),
            Err(error) => return Err(StoreError::Io(error)),
        };
        let mut buffer = Vec::new();
        let mut chunk = [0_u8; 8192];
        loop {
            let read = file.read(&mut chunk)?;
            if read == 0 {
                break;
            }
            if buffer.len() + read > limit {
                return Err(StoreError::TooLarge { limit });
            }
            buffer.extend_from_slice(&chunk[..read]);
        }
        Ok(Some(buffer))
    }

    /// Read a persisted store artifact, classifying an over-limit file.
    ///
    /// [`Self::read_bounded`] reports an over-limit file as
    /// [`StoreError::TooLarge`], which is the right answer when a caller
    /// supplied the oversized value. A file already on disk that exceeds its
    /// bound is a different thing: the artifact cannot be valid, and the
    /// [`StoreDefect`] documentation says so. Classifying it here stops one
    /// corruption from carrying two classes depending on which API observed it.
    fn read_persisted(
        path: &Path,
        limit: usize,
        defect: StoreDefect,
    ) -> Result<Option<Vec<u8>>, StoreError> {
        match Self::read_bounded(path, limit) {
            Err(StoreError::TooLarge { .. }) => Err(StoreError::Defect(defect)),
            other => other,
        }
    }

    fn temp_dir(&self, project: Option<&ProjectId>) -> Result<PathBuf, StoreError> {
        Ok(match project {
            Some(project) => self.project_dir(project)?.join(TEMP_DIR),
            None => self.catalog_dir().join(TEMP_DIR),
        })
    }

    fn temp_token() -> Result<String, StoreError> {
        let mut bytes = [0_u8; 16];
        getrandom::fill(&mut bytes).map_err(|_| IdentityError::RandomnessUnavailable)?;
        Ok(hex_lower(&bytes))
    }

    /// Write bytes durably and publish them by atomic rename.
    ///
    /// The temporary file is created in a sibling directory on the same
    /// filesystem so that the rename is atomic. The file contents are synced
    /// before the rename, so a published name never exposes partially written
    /// bytes. An interrupted write leaves only an unreferenced temporary file,
    /// which is an orphan and is never promoted.
    ///
    /// Nothing is deleted here. Superseded temporaries are recovered, not
    /// removed, because this tranche holds no deletion authority.
    fn write_atomic(
        &self,
        project: Option<&ProjectId>,
        destination: &Path,
        bytes: &[u8],
    ) -> Result<(), StoreError> {
        let temp_dir = self.temp_dir(project)?;
        fs::create_dir_all(&temp_dir)?;
        if let Some(parent) = destination.parent() {
            fs::create_dir_all(parent)?;
        }
        let temp_path = temp_dir.join(format!("{}{TEMP_SUFFIX}", Self::temp_token()?));
        {
            let mut file = OpenOptions::new()
                .write(true)
                .create_new(true)
                .open(&temp_path)?;
            file.write_all(bytes)?;
            file.flush()?;
            file.sync_all()?;
        }
        fs::rename(&temp_path, destination)?;
        // Best-effort directory durability. Not all platforms and filesystems
        // expose directory-entry syncing, so a failure here is not treated as a
        // durability claim either way. See S2-E016.
        if let Some(parent) = destination.parent()
            && let Ok(handle) = File::open(parent)
        {
            let _ = handle.sync_all();
        }
        Ok(())
    }

    fn reservation_path(&self, project: &ProjectId) -> Result<PathBuf, StoreError> {
        let segment = safe_path_segment(project.as_str())?;
        Ok(self
            .reservations_dir()
            .join(format!("{segment}{JSON_SUFFIX}")))
    }

    /// Persist a catalog reservation by temp-write and atomic replace. S2-E006.
    ///
    /// The caller must hold the identity catalog lock.
    pub fn write_reservation(
        &self,
        catalog: &CatalogLock,
        reservation: &IdentityCatalogReservation,
    ) -> Result<(), StoreError> {
        catalog.require_store(self)?;
        let bytes = canonical_project_json(reservation)?;
        let path = self.reservation_path(&reservation.project_id)?;
        self.write_atomic(None, &path, &bytes)
    }

    /// Read a catalog reservation, if one exists. S2-E006.
    pub fn read_reservation(
        &self,
        project: &ProjectId,
    ) -> Result<Option<IdentityCatalogReservation>, StoreError> {
        let path = self.reservation_path(project)?;
        let Some(bytes) =
            Self::read_persisted(&path, MAX_RECORD_BYTES, StoreDefect::RecordCorrupt)?
        else {
            return Ok(None);
        };
        // A malformed persisted record is a store defect, not a codec accident.
        // FR-023 requires malformed, truncated, digest-mismatched,
        // unsupported-version and partially committed records to be treated as
        // invalid consistently. Surfacing the raw codec error here while
        // `list_reservations` reports `RecordCorrupt` for the same bytes would
        // give one corruption two classifications depending on which API
        // observed it.
        let reservation: IdentityCatalogReservation = decode_project_json(&bytes)
            .map_err(|_| StoreError::Defect(StoreDefect::RecordCorrupt))?;
        if reservation.schema_version != ProjectContractVersion::V1 {
            return Err(StoreError::Defect(StoreDefect::UnsupportedSchemaVersion));
        }
        // The path names a project and so do the bytes. A record whose two names
        // disagree is well formed but misbound, and returning it would hand the
        // caller a reservation this project never made; recovery would then
        // resume an identifier the store never reserved under this name.
        if reservation.project_id != *project {
            return Err(StoreError::Defect(StoreDefect::ProjectMismatch));
        }
        Ok(Some(reservation))
    }

    /// List every reservation currently recorded in the catalog. S2-E006.
    ///
    /// Entries that fail to decode are reported as defects rather than skipped,
    /// so corruption cannot silently reduce the candidate set and cause a second
    /// identity to be allocated for an already-reserved project.
    ///
    /// Each entry is also bound to the exact path this store would have written
    /// it to. A well formed reservation filed under another project's name is
    /// reported as [`StoreDefect::ProjectMismatch`] rather than enumerated as
    /// valid, and so is one whose name this store could never have produced.
    ///
    /// The binding is a path comparison rather than a name comparison on
    /// purpose. The contract identifier charset is wider than the path
    /// projection: it admits `.` and `:`, which [`safe_path_segment`] refuses.
    /// Comparing decoded identifier against filename alone would therefore
    /// accept a hand-placed record whose identifier agrees with its name and
    /// which this store could still never write or address, leaving a caller
    /// holding a reservation for a project it cannot open.
    pub fn list_reservations(
        &self,
    ) -> Result<Vec<Result<IdentityCatalogReservation, StoreDefect>>, StoreError> {
        let dir = self.reservations_dir();
        let entries = match fs::read_dir(&dir) {
            Ok(entries) => entries,
            Err(error) if error.kind() == io::ErrorKind::NotFound => return Ok(Vec::new()),
            Err(error) => return Err(StoreError::Io(error)),
        };
        let mut found = Vec::new();
        let mut paths = Vec::new();
        for entry in entries {
            let entry = entry?;
            let path = entry.path();
            if path.extension().is_some_and(|value| value == "json") {
                paths.push(path);
            }
        }
        paths.sort();
        for path in paths {
            let bytes =
                match Self::read_persisted(&path, MAX_RECORD_BYTES, StoreDefect::RecordCorrupt) {
                    Ok(Some(bytes)) => bytes,
                    Ok(None) => continue,
                    // Enumeration reports a defective entry rather than aborting,
                    // so one oversized file cannot hide every other reservation.
                    Err(StoreError::Defect(defect)) => {
                        found.push(Err(defect));
                        continue;
                    }
                    Err(error) => return Err(error),
                };
            match decode_project_json::<IdentityCatalogReservation>(&bytes) {
                Ok(reservation) if reservation.schema_version == ProjectContractVersion::V1 => {
                    let expected = self.reservation_path(&reservation.project_id).ok();
                    if expected.as_deref() == Some(path.as_path()) {
                        found.push(Ok(reservation));
                    } else {
                        found.push(Err(StoreDefect::ProjectMismatch));
                    }
                }
                Ok(_) => found.push(Err(StoreDefect::UnsupportedSchemaVersion)),
                Err(_) => found.push(Err(StoreDefect::RecordCorrupt)),
            }
        }
        Ok(found)
    }

    fn record_path(
        &self,
        project: &ProjectId,
        generation: &GenerationId,
        record: &RecordId,
    ) -> Result<PathBuf, StoreError> {
        let segment = safe_path_segment(record.as_str())?;
        Ok(self
            .generation_dir(project, generation)?
            .join(RECORDS_DIR)
            .join(format!("{segment}{JSON_SUFFIX}")))
    }

    fn manifest_path(
        &self,
        project: &ProjectId,
        generation: &GenerationId,
    ) -> Result<PathBuf, StoreError> {
        Ok(self
            .generation_dir(project, generation)?
            .join(MANIFEST_FILE))
    }

    fn current_path(&self, project: &ProjectId) -> Result<PathBuf, StoreError> {
        Ok(self.project_dir(project)?.join(CURRENT_FILE))
    }

    /// Whether a generation has been closed by a manifest.
    ///
    /// A closed generation is immutable. This is checked by the presence of the
    /// manifest rather than by the `CURRENT` pointer, because a generation is
    /// sealed the moment its manifest exists, whether or not it was published.
    ///
    /// The check must distinguish absence from an unreadable answer.
    /// `Path::exists` collapses every metadata error into `false`, so a manifest
    /// that exists but cannot be stat'd would report the generation as open and
    /// a writer could then replace a closed, possibly published, generation. The
    /// error is therefore propagated as [`StoreError::Io`] and only an explicit
    /// `false` is treated as unclosed.
    fn generation_is_closed(
        &self,
        project: &ProjectId,
        generation: &GenerationId,
    ) -> Result<bool, StoreError> {
        Ok(self.manifest_path(project, generation)?.try_exists()?)
    }

    /// Write one immutable evidence record into a generation under construction.
    ///
    /// S2-E007. Records are written before the manifest and the manifest is
    /// written before `CURRENT`, so an interruption can only ever leave an
    /// unreferenced orphan generation.
    pub fn write_generation_record(
        &self,
        lock: &ProjectLock,
        project: &ProjectId,
        generation: &GenerationId,
        record: &RecordId,
        bytes: &[u8],
    ) -> Result<RecordDigest, StoreError> {
        lock.require(self, project)?;
        if self.generation_is_closed(project, generation)? {
            return Err(StoreError::GenerationAlreadyClosed);
        }
        if bytes.len() > MAX_RECORD_BYTES {
            return Err(StoreError::TooLarge {
                limit: MAX_RECORD_BYTES,
            });
        }
        let path = self.record_path(project, generation, record)?;
        self.write_atomic(Some(project), &path, bytes)?;
        Ok(RecordDigest {
            record_id: record.clone(),
            digest: content_digest(bytes)?,
        })
    }

    /// Write the manifest that closes an immutable generation. S2-E007.
    pub fn write_generation_manifest(
        &self,
        lock: &ProjectLock,
        manifest: &ProjectGenerationManifest,
    ) -> Result<ContentDigest, StoreError> {
        lock.require(self, &manifest.project_id)?;
        if self.generation_is_closed(&manifest.project_id, &manifest.generation_id)? {
            return Err(StoreError::GenerationAlreadyClosed);
        }
        let bytes = canonical_project_json(manifest)?;
        if bytes.len() > MAX_MANIFEST_BYTES {
            return Err(StoreError::TooLarge {
                limit: MAX_MANIFEST_BYTES,
            });
        }
        let path = self.manifest_path(&manifest.project_id, &manifest.generation_id)?;
        self.write_atomic(Some(&manifest.project_id), &path, &bytes)?;
        content_digest(&bytes)
    }

    /// Publish a completed generation by atomically replacing `CURRENT`.
    ///
    /// S2-E008. This is the commit point. The pointer is small, written to a
    /// temporary file on the same filesystem, synced, and renamed over the old
    /// pointer. Readers therefore observe either the previous generation or the
    /// new one, never a mixture.
    ///
    /// The manifest is re-read and fully validated before publication so that a
    /// torn or incoherent generation can never become current.
    ///
    /// The caller must hold the project lock, and must keep holding it across
    /// this call. Validation and the `CURRENT` replacement are a single critical
    /// section: without the guard another writer could rewrite the manifest or a
    /// record between validation and publication.
    pub fn publish_generation(
        &self,
        lock: &ProjectLock,
        project: &ProjectId,
        generation: &GenerationId,
    ) -> Result<ProjectCurrentRef, StoreError> {
        lock.require(self, project)?;
        let manifest_digest = self.validate_generation(project, generation)?;
        let current = ProjectCurrentRef {
            schema_version: ProjectContractVersion::V1,
            project_id: project.clone(),
            generation_id: generation.clone(),
            manifest_digest,
        };
        let bytes = canonical_project_json(&current)?;
        if bytes.len() > MAX_CURRENT_BYTES {
            return Err(StoreError::TooLarge {
                limit: MAX_CURRENT_BYTES,
            });
        }
        let path = self.current_path(project)?;
        self.write_atomic(Some(project), &path, &bytes)?;
        Ok(current)
    }

    /// Fully validate a generation and return its manifest digest.
    ///
    /// S2-E004, S2-E010. Every referenced record must exist, decode within its
    /// bounded read limit, carry a manifest digest, and match that digest.
    pub fn validate_generation(
        &self,
        project: &ProjectId,
        generation: &GenerationId,
    ) -> Result<ContentDigest, StoreError> {
        let manifest_path = self.manifest_path(project, generation)?;
        let Some(manifest_bytes) = Self::read_persisted(
            &manifest_path,
            MAX_MANIFEST_BYTES,
            StoreDefect::ManifestCorrupt,
        )?
        else {
            // Nothing here concerns `CURRENT`: this generation simply carries no
            // manifest, so it was never closed.
            return Err(StoreError::Defect(StoreDefect::GenerationManifestMissing));
        };
        let manifest: ProjectGenerationManifest = decode_project_json(&manifest_bytes)
            .map_err(|_| StoreError::Defect(StoreDefect::ManifestCorrupt))?;
        if manifest.schema_version != ProjectContractVersion::V1 {
            return Err(StoreError::Defect(StoreDefect::UnsupportedSchemaVersion));
        }
        if manifest.producer_contract_version != PRODUCER_CONTRACT_VERSION {
            return Err(StoreError::Defect(
                StoreDefect::UnsupportedProducerContractVersion,
            ));
        }
        if &manifest.project_id != project || &manifest.generation_id != generation {
            return Err(StoreError::Defect(StoreDefect::ProjectMismatch));
        }
        self.validate_manifest_records(&manifest)?;
        content_digest(&manifest_bytes)
    }

    fn digest_for(
        manifest: &ProjectGenerationManifest,
        record: &RecordId,
    ) -> Option<ContentDigest> {
        manifest
            .record_digests
            .as_slice()
            .iter()
            .find(|entry| &entry.record_id == record)
            .map(|entry| entry.digest.clone())
    }

    fn validate_manifest_records(
        &self,
        manifest: &ProjectGenerationManifest,
    ) -> Result<(), StoreError> {
        let mut referenced: Vec<RecordId> = Vec::new();
        referenced.push(manifest.identity_record_ref.clone());
        referenced.push(manifest.index_record_ref.clone());
        referenced.extend(manifest.evidence_record_refs.as_slice().iter().cloned());

        for record in &referenced {
            let path = self.record_path(&manifest.project_id, &manifest.generation_id, record)?;
            let Some(bytes) =
                Self::read_persisted(&path, MAX_RECORD_BYTES, StoreDefect::RecordCorrupt)?
            else {
                return Err(StoreError::Defect(StoreDefect::RecordMissing));
            };
            let Some(expected) = Self::digest_for(manifest, record) else {
                return Err(StoreError::Defect(StoreDefect::RecordDigestMissing));
            };
            let actual = content_digest(&bytes)?;
            if actual != expected {
                return Err(StoreError::Defect(StoreDefect::RecordDigestMismatch));
            }
        }
        Ok(())
    }

    /// Read the published generation exactly once. S2-E009.
    ///
    /// `CURRENT` is read a single time and the returned manifest is the one it
    /// names. Callers must not re-read `CURRENT` while consuming a generation;
    /// doing so is what would allow records from two generations to be mixed.
    pub fn read_published_generation(
        &self,
        project: &ProjectId,
    ) -> Result<PublishedGeneration, StoreError> {
        let current_path = self.current_path(project)?;
        let Some(current_bytes) = Self::read_persisted(
            &current_path,
            MAX_CURRENT_BYTES,
            StoreDefect::CurrentCorrupt,
        )?
        else {
            return Err(StoreError::Defect(StoreDefect::CurrentMissing));
        };
        let current: ProjectCurrentRef = decode_project_json(&current_bytes)
            .map_err(|_| StoreError::Defect(StoreDefect::CurrentCorrupt))?;
        if current.schema_version != ProjectContractVersion::V1 {
            return Err(StoreError::Defect(StoreDefect::UnsupportedSchemaVersion));
        }
        if &current.project_id != project {
            return Err(StoreError::Defect(StoreDefect::ProjectMismatch));
        }

        // The generation identifier came off disk, so an identifier this store
        // could never address is a property of the persisted pointer rather than
        // of the caller. `StoreError::UnsafeIdentifier` is the right answer for a
        // caller-supplied identifier and the wrong one here, because it would
        // report an argument fault for bytes the caller never chose. This is
        // reachable from a hand-written pointer alone, since the contract
        // identifier charset is wider than the path projection.
        let Ok(manifest_path) = self.manifest_path(project, &current.generation_id) else {
            return Err(StoreError::Defect(StoreDefect::CurrentCorrupt));
        };
        let Some(manifest_bytes) = Self::read_persisted(
            &manifest_path,
            MAX_MANIFEST_BYTES,
            StoreDefect::ManifestCorrupt,
        )?
        else {
            return Err(StoreError::Defect(StoreDefect::CurrentDanglingGeneration));
        };
        let observed_digest = content_digest(&manifest_bytes)?;
        if observed_digest != current.manifest_digest {
            return Err(StoreError::Defect(StoreDefect::ManifestDigestMismatch));
        }
        let manifest: ProjectGenerationManifest = decode_project_json(&manifest_bytes)
            .map_err(|_| StoreError::Defect(StoreDefect::ManifestCorrupt))?;
        if manifest.producer_contract_version != PRODUCER_CONTRACT_VERSION {
            return Err(StoreError::Defect(
                StoreDefect::UnsupportedProducerContractVersion,
            ));
        }
        if &manifest.project_id != project || manifest.generation_id != current.generation_id {
            return Err(StoreError::Defect(StoreDefect::ProjectMismatch));
        }
        self.validate_manifest_records(&manifest)?;
        Ok(PublishedGeneration { current, manifest })
    }

    /// Read one record belonging to an already-selected generation. S2-E009.
    ///
    /// The generation is supplied by the caller from a single
    /// [`Self::read_published_generation`] result, which is what prevents a
    /// mixed-generation read.
    ///
    /// The manifest argument is an ordinary public value, so this is a public
    /// entry point in its own right rather than only a continuation of a
    /// validated read. It therefore repeats the producer-contract refusal:
    /// checking it in [`Self::read_published_generation`] alone would leave the
    /// refusal bypassable by anyone who decoded or built a manifest and passed
    /// it here, which would make the stated reader boundary untrue.
    pub fn read_generation_record(
        &self,
        manifest: &ProjectGenerationManifest,
        record: &RecordId,
    ) -> Result<Vec<u8>, StoreError> {
        if manifest.producer_contract_version != PRODUCER_CONTRACT_VERSION {
            return Err(StoreError::Defect(
                StoreDefect::UnsupportedProducerContractVersion,
            ));
        }
        let Some(expected) = Self::digest_for(manifest, record) else {
            return Err(StoreError::Defect(StoreDefect::RecordDigestMissing));
        };
        let path = self.record_path(&manifest.project_id, &manifest.generation_id, record)?;
        let Some(bytes) =
            Self::read_persisted(&path, MAX_RECORD_BYTES, StoreDefect::RecordCorrupt)?
        else {
            return Err(StoreError::Defect(StoreDefect::RecordMissing));
        };
        if content_digest(&bytes)? != expected {
            return Err(StoreError::Defect(StoreDefect::RecordDigestMismatch));
        }
        Ok(bytes)
    }

    /// List generation directories that exist but are not the published one.
    ///
    /// S2-E010. Orphans are the expected residue of an interrupted publish.
    /// They are reported for diagnosis and are never promoted, never read as
    /// current, and never deleted by this tranche.
    ///
    /// An entry is reported only when it is one this store could itself have
    /// written: a directory whose name is exactly the path segment
    /// [`Self::generation_dir`] would produce for that identifier. The contract
    /// identifier charset is wider than the path projection, admitting `.` and
    /// `:` which [`safe_path_segment`] refuses, so a name can parse as a valid
    /// [`GenerationId`] and still be one this store can never address. Reporting
    /// such an entry would hand a caller an orphan identifier that every
    /// subsequent store call refuses.
    ///
    /// Entries that are not directories, whose names are not identifiers, or
    /// which fail that binding are therefore not listed. They are not
    /// generations, and this function makes no claim about them; a general
    /// account of unexpected store entries belongs to the Doctor rules that
    /// inspect the store as a whole.
    pub fn orphan_generations(&self, project: &ProjectId) -> Result<Vec<GenerationId>, StoreError> {
        let published = match self.read_published_generation(project) {
            Ok(generation) => Some(generation.current.generation_id),
            Err(StoreError::Defect(_)) => None,
            Err(error) => return Err(error),
        };
        let dir = self.project_dir(project)?.join(GENERATIONS_DIR);
        let entries = match fs::read_dir(&dir) {
            Ok(entries) => entries,
            Err(error) if error.kind() == io::ErrorKind::NotFound => return Ok(Vec::new()),
            Err(error) => return Err(StoreError::Io(error)),
        };
        let mut orphans = Vec::new();
        for entry in entries {
            let entry = entry?;
            if !entry.file_type()?.is_dir() {
                continue;
            }
            let name = entry.file_name();
            let Some(name) = name.to_str() else {
                continue;
            };
            let Ok(generation) = GenerationId::try_from(name) else {
                continue;
            };
            // Only an entry this store could have written is a generation of
            // this store. A wider contract charset must not produce an orphan
            // identifier that every later call would refuse.
            if self.generation_dir(project, &generation).ok().as_deref()
                != Some(entry.path().as_path())
            {
                continue;
            }
            if published.as_ref() == Some(&generation) {
                continue;
            }
            orphans.push(generation);
        }
        orphans.sort();
        Ok(orphans)
    }

    /// Compute freshness for a published generation. S2-E011.
    ///
    /// Freshness is derived from the recorded generation commit time, not from
    /// filesystem modification time. Modification time is not trustworthy as a
    /// freshness basis on its own, so it is not used here.
    pub fn freshness(
        manifest: &ProjectGenerationManifest,
        now: UnixMillis,
        max_age_millis: u64,
    ) -> Freshness {
        let created = manifest.created_at.get();
        let current = now.get();
        let age = current.saturating_sub(created);
        let status = if current < created {
            // A generation stamped in the future cannot be aged coherently.
            EvidenceStatus::Stale
        } else if age > max_age_millis {
            EvidenceStatus::Stale
        } else {
            EvidenceStatus::Complete
        };
        Freshness {
            basis: FreshnessBasis::GenerationCommit,
            status,
            age_millis: age,
        }
    }

    /// The authenticity level this store can honestly claim. S2-E017.
    ///
    /// Always structural coherence only. There is no keyed trust anchor, so a
    /// writer-capable actor can forge a self-consistent store. Callers must not
    /// present this as cryptographic authentication or tamper evidence.
    pub fn authenticity() -> StoreAuthenticity {
        StoreAuthenticity::UnauthenticatedStructuralCoherenceOnly
    }
}

/// Build a generation manifest from already-written record digests. S2-E007.
pub fn build_manifest(
    project_id: ProjectId,
    generation_id: GenerationId,
    identity_record_ref: RecordId,
    index_record_ref: RecordId,
    evidence_record_refs: wepld_contracts::EvidenceRecordRefs,
    digests: Vec<RecordDigest>,
    created_at: UnixMillis,
) -> Result<ProjectGenerationManifest, StoreError> {
    let count = digests.len();
    let record_digests =
        RecordDigestList::try_from(digests).map_err(|_| StoreError::TooLarge { limit: count })?;
    Ok(ProjectGenerationManifest {
        schema_version: ProjectContractVersion::V1,
        generation_id,
        project_id,
        identity_record_ref,
        index_record_ref,
        evidence_record_refs,
        record_digests,
        producer_contract_version: PRODUCER_CONTRACT_VERSION,
        created_at,
        authenticity: EvidenceStore::authenticity(),
    })
}

/// Current wall-clock time in Unix milliseconds.
///
/// A clock reading before the Unix epoch is reported as zero rather than
/// producing a panic or a negative age.
pub fn now_unix_millis() -> UnixMillis {
    let millis = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map(|elapsed| u64::try_from(elapsed.as_millis()).unwrap_or(u64::MAX))
        .unwrap_or(0);
    UnixMillis::new(millis)
}

/// Coarse size class of a redacted value.
///
/// An exact byte length is itself a disclosure: combined with an unkeyed digest
/// it narrows an offline candidate search considerably. Only a coarse bucket is
/// reported.
fn size_class(length: usize) -> &'static str {
    match length {
        0 => "empty",
        1..=32 => "xs",
        33..=128 => "s",
        129..=1024 => "m",
        1025..=32768 => "l",
        _ => "xl",
    }
}

/// Redact a value that must never be persisted or displayed raw. S2-E012.
///
/// The store persists only allowlisted structured contract fields. When a caller
/// must record that a sensitive value was observed, it records this summary
/// instead of the value.
///
/// # What this does and does not provide
///
/// The summary carries a coarse size class and a truncated unkeyed SHA-256
/// prefix. It exists so that repeat observations of the same value can be
/// correlated, and it never emits the value itself.
///
/// It is **not** resistant to an offline candidate search. The digest is
/// unkeyed, so anyone holding a guess can hash it and compare prefixes. For a
/// low-entropy value that is a realistic recovery path. Exact length is
/// deliberately withheld to widen the candidate space, but this remains
/// correlation evidence, not concealment against an adversary who can guess.
/// Defending a low-entropy secret requires a keyed construction, which needs a
/// trust anchor this slice does not have and must be planned separately.
pub fn redacted_summary(value: &[u8]) -> Result<String, StoreError> {
    let digest = content_digest(value)?;
    let prefix: String = digest.hex.as_str().chars().take(12).collect();
    Ok(format!("redacted:{}:{}", size_class(value.len()), prefix))
}
