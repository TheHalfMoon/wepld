#![forbid(unsafe_code)]

use std::path::{Path, PathBuf};

use wepld_contracts::{
    MachinePath, Observation, ObservationErrorClass, ProjectContractVersion, ProjectLocator,
    UnixMillis,
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