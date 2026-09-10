#![forbid(unsafe_code)]

use std::path::{Path, PathBuf};

use wepld_contracts::{
    MachinePath, Observation, ObservationErrorClass, ProjectContractVersion, ProjectLocator,
    UnixMillis,
};
#[cfg(unix)]
use wepld_core::identity::{
    ProjectMatchFacts, ReservationRecovery, allocate_project_id, build_reservation,
    recover_reservation,
};
use wepld_core::{
    DataRootInputs, DataRootSource, MAX_PATH_COMPONENT_OBSERVATIONS, PathEntryKind,
    ProjectObservationError, ProjectRootBasis, classify_path_io_error, lexical_absolute_path,
    machine_path_from_path, observe_non_git_project_root, observe_path_metadata,
    observe_project_locator, platform_data_root,
};

fn manifest_dir() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
}

#[test]
fn lexical_absolute_path_normalizes_without_filesystem_resolution() {
    let base = manifest_dir();
    let actual = lexical_absolute_path(Path::new("alpha/./beta/../gamma"), &base)
        .expect("lexical path should be derivable from an explicit absolute base");
    assert_eq!(actual, base.join("alpha").join("gamma"));

    let absolute = base.join("one").join("..").join("two");
    let normalized = lexical_absolute_path(&absolute, Path::new("relative-base"))
        .expect("an absolute input must not depend on the lexical base");
    assert_eq!(normalized, base.join("two"));
}

#[test]
fn lexical_absolute_path_rejects_empty_and_relative_base() {
    assert_eq!(
        lexical_absolute_path(Path::new(""), &manifest_dir()),
        Err(ProjectObservationError::EmptyInput)
    );
    assert_eq!(
        lexical_absolute_path(Path::new("relative"), Path::new("also-relative")),
        Err(ProjectObservationError::LexicalBaseNotAbsolute)
    );
}

#[cfg(windows)]
#[test]
fn windows_drive_relative_locator_is_rejected_without_ambient_drive_state() {
    assert_eq!(
        lexical_absolute_path(Path::new(r"C:relative"), &manifest_dir()),
        Err(ProjectObservationError::PlatformRelativePathUnsupported)
    );
}

#[test]
fn project_locator_preserves_input_lexical_and_resolved_layers() {
    let base = manifest_dir();
    let locator = observe_project_locator(Path::new("."), &base, UnixMillis::new(7))
        .expect("the Core crate directory should be observable");

    assert_eq!(
        locator.input_path,
        machine_path_from_path(Path::new(".")).unwrap()
    );
    assert_eq!(
        locator.lexical_absolute_path,
        machine_path_from_path(&base).unwrap()
    );
    assert!(matches!(
        locator.resolved_path,
        Observation::Available { .. }
    ));
    assert_eq!(locator.observation_time, UnixMillis::new(7));
}

#[test]
fn project_locator_records_canonicalization_failure_instead_of_fabricating_resolution() {
    let base = manifest_dir();
    let missing = Path::new("definitely-missing-wepld-s2-observation-fixture");
    let locator = observe_project_locator(missing, &base, UnixMillis::new(9))
        .expect("an unavailable resolved path is still a valid locator observation");

    assert_eq!(
        locator.resolved_path,
        Observation::Unavailable {
            error: ObservationErrorClass::NotFound
        }
    );
}

/// S2-S001 (project-locator layer): a `..` sequence that would climb past the
/// lexical base, and a path carrying an interior NUL byte, are each handled as
/// a bounded, deterministic observation. The parent-escape is fully collapsed
/// (no `..` survives, the result is anchored at the filesystem root, never a
/// path "above" root), the raw traversal spelling is preserved verbatim in
/// `input_path` rather than silently rewritten, and neither input panics or is
/// fabricated into an `Observation::Available` resolution. This is distinct
/// from the `safe_path_segment` store-ID layer already covered by S2-S009 /
/// S2-E003: here the attack is on `observe_project_locator` itself.
#[cfg(unix)]
#[test]
fn project_locator_clamps_parent_escape_and_types_invalid_paths_without_fabrication() {
    use std::ffi::OsStr;
    use std::os::unix::ffi::OsStrExt;
    use std::path::Component;

    let base = manifest_dir();

    // (1) Far more `..` than `base` is deep. Lexical normalization collapses
    // every ParentDir, anchors the result at `/`, and leaves none behind.
    let escaping = Path::new(
        "../../../../../../../../../../../../../../../../../../../../etc/wepld-s2-s001-absent-target",
    );
    let lexical = lexical_absolute_path(escaping, &base)
        .expect("an over-deep parent escape must still normalize, not error");
    assert!(
        !lexical
            .components()
            .any(|component| matches!(component, Component::ParentDir)),
        "the normalizer must fully collapse `..`, leaving none: {lexical:?}"
    );
    // Exact clamp: every `..` past the base collapses to the filesystem root,
    // independent of workspace depth -- not merely absolute, not merely
    // ending with the tail.
    assert_eq!(
        lexical,
        Path::new("/etc/wepld-s2-s001-absent-target"),
        "the escape must collapse to exactly the root-anchored target: {lexical:?}"
    );

    // (2) The locator records the raw traversal spelling unchanged and does
    // not fabricate a resolution for the (non-existent) escaped target.
    let locator = observe_project_locator(escaping, &base, UnixMillis::new(11))
        .expect("a parent-escape input is still a valid locator observation");
    assert_eq!(
        locator.input_path,
        machine_path_from_path(escaping).unwrap(),
        "the exact `..`-bearing spelling must be preserved, not normalized away"
    );
    assert_eq!(
        locator.lexical_absolute_path,
        machine_path_from_path(&lexical).unwrap()
    );
    assert_eq!(
        locator.resolved_path,
        Observation::Unavailable {
            error: ObservationErrorClass::NotFound
        }
    );

    // (3) A path with an interior NUL byte is a bounded, typed InvalidPath
    // observation -- never a panic, never a fabricated resolve.
    let injected = Path::new(OsStr::from_bytes(b"/tmp/wepld-s2-s001\0injected"));
    let locator = observe_project_locator(injected, &base, UnixMillis::new(12))
        .expect("an invalid-byte path is still a valid locator observation");
    assert_eq!(
        locator.input_path,
        machine_path_from_path(injected).unwrap()
    );
    assert_eq!(
        locator.resolved_path,
        Observation::Unavailable {
            error: ObservationErrorClass::InvalidPath
        }
    );
}

#[test]
fn metadata_observation_is_bounded_to_path_components_and_does_not_walk_the_tree() {
    let base = manifest_dir();
    let trail =
        observe_path_metadata(&base).expect("manifest directory metadata should be readable");
    let expected_components = base
        .components()
        .filter(|component| matches!(component, std::path::Component::Normal(_)))
        .count();

    assert_eq!(trail.components.len(), expected_components);
    assert!(trail.components.len() <= MAX_PATH_COMPONENT_OBSERVATIONS);
    let last = trail
        .components
        .last()
        .expect("manifest path has normal components");
    assert_eq!(
        last.entry_kind,
        Observation::Available {
            value: PathEntryKind::Directory
        }
    );
}

#[test]
fn metadata_observation_rejects_non_absolute_input() {
    assert_eq!(
        observe_path_metadata(Path::new("relative")),
        Err(ProjectObservationError::ObservedPathNotAbsolute)
    );
}

#[cfg(target_os = "linux")]
#[test]
fn linux_eloop_maps_to_symlink_loop() {
    let error = std::io::Error::from_raw_os_error(40);
    assert_eq!(
        classify_path_io_error(&error),
        ObservationErrorClass::SymlinkLoop
    );
}

#[cfg(target_os = "macos")]
#[test]
fn macos_eloop_maps_to_symlink_loop() {
    let error = std::io::Error::from_raw_os_error(62);
    assert_eq!(
        classify_path_io_error(&error),
        ObservationErrorClass::SymlinkLoop
    );
}

#[cfg(windows)]
#[test]
fn windows_cant_resolve_filename_maps_to_symlink_loop() {
    let error = std::io::Error::from_raw_os_error(1921);
    assert_eq!(
        classify_path_io_error(&error),
        ObservationErrorClass::SymlinkLoop
    );
}

#[test]
fn non_git_directory_root_uses_revalidated_resolved_path() {
    let base = manifest_dir();
    let locator = observe_project_locator(Path::new("."), &base, UnixMillis::new(11)).unwrap();
    let root = observe_non_git_project_root(&locator, &base)
        .expect("root observation should be structurally valid");

    match root {
        Observation::Available { value } => {
            assert_eq!(value.basis, ProjectRootBasis::Resolved);
            assert_eq!(
                value.path,
                machine_path_from_path(&std::fs::canonicalize(&base).unwrap()).unwrap()
            );
        }
        Observation::Unavailable { error } => panic!("unexpected root unavailability: {error:?}"),
    }
}

#[test]
fn non_git_directory_root_rejects_locator_path_mismatch_before_fallback() {
    let base = manifest_dir();
    let locator = ProjectLocator {
        schema_version: ProjectContractVersion::V1,
        input_path: machine_path_from_path(Path::new("different")).unwrap(),
        lexical_absolute_path: machine_path_from_path(&base.join("different")).unwrap(),
        resolved_path: Observation::Unavailable {
            error: ObservationErrorClass::PermissionDenied,
        },
        observation_time: UnixMillis::new(12),
    };

    assert_eq!(
        observe_non_git_project_root(&locator, &base).unwrap(),
        Observation::Unavailable {
            error: ObservationErrorClass::RaceDetected
        }
    );
}

#[cfg(target_os = "linux")]
#[test]
fn linux_data_root_prefers_absolute_xdg_state_home() {
    let xdg = Path::new("/qualified/xdg-state");
    let home = Path::new("/qualified/home");
    let root = platform_data_root(DataRootInputs {
        xdg_state_home: Some(xdg),
        home: Some(home),
        macos_application_support: None,
        windows_local_app_data: None,
    })
    .unwrap();

    assert_eq!(root.source, DataRootSource::XdgStateHome);
    assert!(!root.ignored_relative_xdg_state_home);
    assert_eq!(
        root.path,
        machine_path_from_path(&xdg.join("wepld")).unwrap()
    );
}

#[cfg(target_os = "linux")]
#[test]
fn linux_data_root_ignores_relative_xdg_and_uses_absolute_home_fallback() {
    let home = Path::new("/qualified/home");
    let root = platform_data_root(DataRootInputs {
        xdg_state_home: Some(Path::new("relative-state")),
        home: Some(home),
        macos_application_support: None,
        windows_local_app_data: None,
    })
    .unwrap();

    assert_eq!(root.source, DataRootSource::HomeLocalStateFallback);
    assert!(root.ignored_relative_xdg_state_home);
    assert_eq!(
        root.path,
        machine_path_from_path(&home.join(".local").join("state").join("wepld")).unwrap()
    );
}

#[cfg(target_os = "linux")]
#[test]
fn linux_data_root_fails_closed_when_fallback_home_is_unavailable() {
    assert_eq!(
        platform_data_root(DataRootInputs {
            xdg_state_home: Some(Path::new("relative-state")),
            home: None,
            macos_application_support: None,
            windows_local_app_data: None,
        }),
        Err(ProjectObservationError::DataRootBaseUnavailable)
    );
}

#[cfg(target_os = "macos")]
#[test]
fn macos_data_root_uses_explicit_application_support_base() {
    let support = Path::new("/Users/example/Library/Application Support");
    let root = platform_data_root(DataRootInputs {
        xdg_state_home: None,
        home: None,
        macos_application_support: Some(support),
        windows_local_app_data: None,
    })
    .unwrap();
    assert_eq!(root.source, DataRootSource::MacosApplicationSupport);
    assert_eq!(
        root.path,
        machine_path_from_path(&support.join("WePLD")).unwrap()
    );
}

#[cfg(windows)]
#[test]
fn windows_data_root_uses_explicit_local_app_data_base() {
    let local = Path::new(r"C:\Users\example\AppData\Local");
    let root = platform_data_root(DataRootInputs {
        xdg_state_home: None,
        home: None,
        macos_application_support: None,
        windows_local_app_data: Some(local),
    })
    .unwrap();
    assert_eq!(root.source, DataRootSource::WindowsLocalAppData);
    assert_eq!(
        root.path,
        machine_path_from_path(&local.join("WePLD")).unwrap()
    );
}

#[cfg(unix)]
#[test]
fn unix_machine_path_preserves_non_utf8_bytes_losslessly() {
    use std::ffi::OsString;
    use std::os::unix::ffi::OsStringExt as _;

    let units = vec![b'/', b't', b'm', b'p', b'/', 0xff, b'x'];
    let path = PathBuf::from(OsString::from_vec(units.clone()));
    assert_eq!(
        machine_path_from_path(&path).unwrap(),
        MachinePath::UnixBytes(units)
    );
}

#[cfg(windows)]
#[test]
fn windows_machine_path_preserves_wtf16_units_losslessly() {
    use std::ffi::OsString;
    use std::os::windows::ffi::OsStringExt as _;

    let units = vec![
        u16::from(b'C'),
        u16::from(b':'),
        u16::from(b'\\'),
        0xd800,
        u16::from(b'x'),
    ];
    let path = PathBuf::from(OsString::from_wide(&units));
    assert_eq!(
        machine_path_from_path(&path).unwrap(),
        MachinePath::WindowsWtf16(units)
    );
}

/// Scratch directory under the cargo target tmpdir, auto-scoped per run.
fn scratch_dir(label: &str) -> PathBuf {
    use std::sync::atomic::{AtomicUsize, Ordering};
    static COUNTER: AtomicUsize = AtomicUsize::new(0);
    let n = COUNTER.fetch_add(1, Ordering::Relaxed);
    let mut root = PathBuf::from(env!("CARGO_TARGET_TMPDIR"));
    root.push(format!(
        "wepld-project-obs-{label}-{}-{n}",
        std::process::id()
    ));
    std::fs::create_dir_all(&root).expect("scratch dir must be creatable");
    root
}

/// S2-S002: a real symlink cycle resolves to an explicit `SymlinkLoop`
/// classification with bounded completion -- the standard resolution API
/// returns `ELOOP`, no manual unbounded following occurs, and no resolved
/// path is fabricated. Complements `*_eloop_maps_to_symlink_loop`, which only
/// exercises the injected-error classifier.
#[cfg(unix)]
#[test]
fn real_symlink_cycle_resolves_to_symlink_loop_without_hanging() {
    use std::os::unix::fs::symlink;

    let dir = scratch_dir("symlink-cycle");
    let a = dir.join("a");
    let b = dir.join("b");
    symlink(&b, &a).expect("create symlink a -> b");
    symlink(&a, &b).expect("create symlink b -> a");

    let started = std::time::Instant::now();
    let locator = observe_project_locator(&a, &dir, UnixMillis::new(11))
        .expect("a cyclic symlink is still a valid locator observation");
    assert!(
        started.elapsed() < std::time::Duration::from_secs(5),
        "resolution must be bounded, not a hang"
    );
    assert_eq!(
        locator.resolved_path,
        Observation::Unavailable {
            error: ObservationErrorClass::SymlinkLoop
        },
        "a real symlink cycle must resolve to an explicit SymlinkLoop"
    );
}

/// S2-S002: a symlink to a nonexistent target resolves to an explicit
/// `NotFound` -- the broken link is not silently followed, guessed, or
/// fabricated -- while path-component metadata still observes the link entry
/// itself as a `Symlink`.
#[cfg(unix)]
#[test]
fn broken_symlink_target_is_reported_not_fabricated() {
    use std::os::unix::fs::symlink;

    let dir = scratch_dir("broken-symlink");
    let link = dir.join("dangling");
    symlink(dir.join("does-not-exist-wepld-s2-fixture"), &link).expect("create dangling symlink");

    let locator = observe_project_locator(&link, &dir, UnixMillis::new(12))
        .expect("a broken symlink is still a valid locator observation");
    assert_eq!(
        locator.resolved_path,
        Observation::Unavailable {
            error: ObservationErrorClass::NotFound
        },
        "a broken symlink target must be reported as NotFound, never fabricated"
    );

    let trail = observe_path_metadata(&link).expect("link path metadata must be observable");
    let last = trail
        .components
        .last()
        .expect("the link path has normal components");
    assert_eq!(
        last.entry_kind,
        Observation::Available {
            value: PathEntryKind::Symlink
        },
        "the dangling link entry itself is observed as a Symlink"
    );
}

/// S2-S001 / threat model T-002 (TOCTOU replacement).
///
/// The attacker reserves nothing directly; instead, between an opener's
/// reservation and a later recovery of that same reservation, the attacker
/// retargets a symlink that both observations name by the same input path.
/// `ProjectMatchFacts::facts_digest` is documented to bind identity to the
/// *resolved* path precisely so this race is detected rather than silently
/// merged, so recovery over the retargeted link must report `Mismatch`.
/// Complements `reservation_for_different_facts_is_not_adopted` in
/// `identity_store_v1.rs`, which proves the same decision against two
/// independently synthetic facts values and never touches a filesystem;
/// this test proves the decision fires against a genuine same-input-path
/// race, where the attacker changes what the *link* resolves to rather than
/// what path is asked for.
#[cfg(unix)]
#[test]
fn symlink_retargeted_between_reservation_and_recovery_is_a_toctou_mismatch() {
    use std::os::unix::fs::symlink;

    let dir = scratch_dir("toctou-symlink");
    let real_original = dir.join("real-original");
    let real_attacker = dir.join("real-attacker");
    std::fs::create_dir_all(&real_original).expect("create original real directory");
    std::fs::create_dir_all(&real_attacker).expect("create attacker real directory");

    let link = dir.join("project-link");
    symlink(&real_original, &link).expect("create initial symlink to the original directory");

    let locator_at_reservation = observe_project_locator(&link, &dir, UnixMillis::new(21))
        .expect("initial locator observation through the symlink must succeed");
    let facts_at_reservation = ProjectMatchFacts::new(locator_at_reservation);
    let project_id = allocate_project_id().expect("allocate a project id");
    let reservation = build_reservation(
        project_id.clone(),
        &facts_at_reservation,
        UnixMillis::new(21),
    )
    .expect("build the initial reservation");

    // The attacker retargets the same link, still at the same input path, to
    // a different real directory before recovery observes it again.
    std::fs::remove_file(&link).expect("remove the original symlink");
    symlink(&real_attacker, &link).expect("retarget the symlink to the attacker directory");

    let locator_at_recovery = observe_project_locator(&link, &dir, UnixMillis::new(22))
        .expect("post-retarget locator observation through the symlink must succeed");
    let facts_at_recovery = ProjectMatchFacts::new(locator_at_recovery);

    assert_eq!(
        recover_reservation(&reservation, &facts_at_recovery)
            .expect("recovery decision must not itself fail"),
        ReservationRecovery::Mismatch,
        "a retargeted link must never let recovery resume the reservation under a different real location"
    );

    // Sanity: recovering against the *original*, unretargeted facts still
    // resumes normally, so the mismatch above is caused by the retarget and
    // not by some unrelated defect in observation or digesting.
    let recovered = recover_reservation(&reservation, &facts_at_reservation)
        .expect("recovery decision must not itself fail");
    match recovered {
        ReservationRecovery::ResumeSameProject {
            project_id: resumed,
        } => {
            assert_eq!(resumed, project_id);
        }
        other => panic!("expected ResumeSameProject for the unretargeted facts, got {other:?}"),
    }
}

/// S2-S004: machine-path representation preserves the caller's exact case; it
/// is never generically lowercased (threat model T-003). The bytes/units of a
/// mixed-case path round-trip unchanged, and the locator layers keep the same
/// spelling.
#[test]
fn machine_path_preserves_exact_case_and_never_lowercases() {
    #[cfg(unix)]
    {
        use std::ffi::OsString;
        use std::os::unix::ffi::OsStringExt as _;
        let bytes = b"/Tmp/MixedCase/FooBar".to_vec();
        let path = PathBuf::from(OsString::from_vec(bytes.clone()));
        assert_eq!(
            machine_path_from_path(&path).unwrap(),
            MachinePath::UnixBytes(bytes)
        );
    }
    #[cfg(windows)]
    {
        use std::ffi::OsString;
        use std::os::windows::ffi::OsStringExt as _;
        let text = "C:\\Tmp\\MixedCase\\FooBar";
        let units: Vec<u16> = text.encode_utf16().collect();
        let path = PathBuf::from(OsString::from_wide(&units));
        assert_eq!(
            machine_path_from_path(&path).unwrap(),
            MachinePath::WindowsWtf16(units)
        );
    }

    // A real mixed-case directory: the caller-spelling locator layers (input
    // and lexical absolute) keep the exact spelling rather than a folded form.
    // The resolved layer is filesystem-derived and not asserted here.
    let dir = scratch_dir("MixedCaseObservation");
    let nested = dir.join("SubDir_MixedCase");
    std::fs::create_dir_all(&nested).expect("nested mixed-case dir");
    let locator = observe_project_locator(&nested, &dir, UnixMillis::new(13))
        .expect("mixed-case directory is observable");
    assert_eq!(
        locator.input_path,
        machine_path_from_path(&nested).unwrap(),
        "the input layer must preserve the exact mixed-case spelling"
    );
    assert_eq!(
        locator.lexical_absolute_path,
        machine_path_from_path(&nested).unwrap(),
        "the lexical absolute layer must preserve the exact mixed-case spelling"
    );
}

/// S2-S004 (identity half): two paths that differ only by ASCII case are
/// resolved through `observe_project_locator` and turned into identity facts.
/// `ProjectMatchFacts::facts_digest` binds identity to the *resolved* path and
/// excludes the caller spelling and lexical path, so the real filesystem's case
/// semantics decide the outcome, and each CI leg exercises the arm that matches
/// its own filesystem:
///
///   * case-INSENSITIVE filesystem (macOS APFS on the `secondary-platform`
///     matrix): both spellings `canonicalize` to the one real directory, so
///     `resolved_path` is identical, `facts_digest` is identical, and a
///     reservation built under the mixed-case spelling is `ResumeSameProject`
///     when recovered under the lowercase spelling -- one project identity,
///     never a spurious second one;
///   * case-SENSITIVE filesystem (Linux ext4): only the exact-case directory
///     exists, so the lowercase spelling's `resolved_path` is a bounded
///     `Unavailable { NotFound }` -- the observation reports the miss and never
///     fabricates a resolution onto the directory that does exist.
///
/// The branch is chosen by a runtime probe of the real filesystem, not by
/// `target_os`, so the assertion is correct on whatever host runs the suite.
#[cfg(unix)]
#[test]
fn case_only_paths_collapse_to_one_identity_iff_the_filesystem_is_case_insensitive() {
    let dir = scratch_dir("case-identity");
    let mixed = dir.join("CaseProject");
    std::fs::create_dir_all(&mixed).expect("create the mixed-case project directory");

    // The same final component, all lowercase. Never created on disk.
    let lower = dir.join("caseproject");

    // Runtime probe: does the lowercase spelling resolve to the same real
    // directory that the mixed-case spelling was created as?
    let case_insensitive = match (std::fs::canonicalize(&mixed), std::fs::canonicalize(&lower)) {
        (Ok(resolved_mixed), Ok(resolved_lower)) => resolved_mixed == resolved_lower,
        _ => false,
    };

    let mixed_locator = observe_project_locator(&mixed, &dir, UnixMillis::new(31))
        .expect("mixed-case locator observation succeeds");
    let lower_locator = observe_project_locator(&lower, &dir, UnixMillis::new(32))
        .expect("lowercase locator observation is still a bounded observation, not an error");

    // The caller-spelling input layer always preserves exactly what was asked
    // for, regardless of filesystem case behaviour.
    assert_eq!(
        lower_locator.input_path,
        machine_path_from_path(&lower).unwrap(),
        "the input layer preserves the exact lowercase spelling"
    );

    if case_insensitive {
        assert_eq!(
            mixed_locator.resolved_path, lower_locator.resolved_path,
            "case-insensitive fs: both spellings resolve to the one real directory"
        );

        let mixed_facts = ProjectMatchFacts::new(mixed_locator);
        let lower_facts = ProjectMatchFacts::new(lower_locator);
        assert_eq!(
            mixed_facts
                .facts_digest()
                .expect("mixed-case facts digest is computable"),
            lower_facts
                .facts_digest()
                .expect("lowercase facts digest is computable"),
            "identity is bound to the resolved path, so a case-only difference is one identity"
        );

        let project_id = allocate_project_id().expect("allocate a project id");
        let reservation = build_reservation(project_id.clone(), &mixed_facts, UnixMillis::new(31))
            .expect("build a reservation under the mixed-case spelling");
        match recover_reservation(&reservation, &lower_facts)
            .expect("recovery decision must not itself fail")
        {
            ReservationRecovery::ResumeSameProject {
                project_id: resumed,
            } => {
                assert_eq!(
                    resumed, project_id,
                    "the lowercase spelling recovers the very same project"
                );
            }
            other => panic!(
                "a case-only path difference on a case-insensitive fs must resume the same project, got {other:?}"
            ),
        }
    } else {
        assert_eq!(
            lower_locator.resolved_path,
            Observation::Unavailable {
                error: ObservationErrorClass::NotFound
            },
            "case-sensitive fs: the unspelled lowercase directory is NotFound, never fabricated"
        );
        assert_ne!(
            mixed_locator.resolved_path, lower_locator.resolved_path,
            "case-sensitive fs: distinct directories give distinct resolution outcomes"
        );
    }
}
