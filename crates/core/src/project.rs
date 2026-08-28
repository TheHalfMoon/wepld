#![forbid(unsafe_code)]

use std::fmt;
use std::io;
use std::path::{Component, Path, PathBuf};

use wepld_contracts::{
    ContractValueError, MachinePath, Observation, ObservationErrorClass, OptionalObservation,
    ProjectContractVersion, ProjectLocator, UnixMillis,
};

#[cfg(unix)]
use std::os::unix::ffi::OsStrExt as _;
#[cfg(windows)]
use std::os::windows::ffi::OsStrExt as _;
#[cfg(windows)]
use std::os::windows::fs::MetadataExt as _;

pub const MAX_PATH_COMPONENT_OBSERVATIONS: usize = 256;
#[cfg(windows)]
const WINDOWS_FILE_ATTRIBUTE_REPARSE_POINT: u32 = 0x0000_0400;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ProjectObservationError {
    EmptyInput,
    LexicalBaseNotAbsolute,
    PlatformRelativePathUnsupported,
    ObservedPathNotAbsolute,
    PathTooDeep { components: usize, max: usize },
    DataRootBaseUnavailable,
    DataRootBaseNotAbsolute,
    UnsupportedPlatform,
    Contract(ContractValueError),
}

impl fmt::Display for ProjectObservationError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::EmptyInput => write!(formatter, "project locator input must not be empty"),
            Self::LexicalBaseNotAbsolute => {
                write!(formatter, "lexical base path must be absolute")
            }
            Self::PlatformRelativePathUnsupported => write!(
                formatter,
                "platform-relative path requires ambient drive/current-directory state"
            ),
            Self::ObservedPathNotAbsolute => {
                write!(formatter, "observed filesystem path must be absolute")
            }
            Self::PathTooDeep { components, max } => write!(
                formatter,
                "path component count {components} exceeds maximum {max}"
            ),
            Self::DataRootBaseUnavailable => {
                write!(
                    formatter,
                    "qualified platform data-root base is unavailable"
                )
            }
            Self::DataRootBaseNotAbsolute => {
                write!(
                    formatter,
                    "qualified platform data-root base must be absolute"
                )
            }
            Self::UnsupportedPlatform => write!(formatter, "platform data-root is unsupported"),
            Self::Contract(error) => write!(formatter, "project contract value error: {error}"),
        }
    }
}

impl From<ContractValueError> for ProjectObservationError {
    fn from(value: ContractValueError) -> Self {
        Self::Contract(value)
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PathEntryKind {
    File,
    Directory,
    Symlink,
    Other,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PathMetadataObservation {
    pub path: MachinePath,
    pub entry_kind: Observation<PathEntryKind>,
    pub reparse_point: OptionalObservation<bool>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PathMetadataTrail {
    pub components: Vec<PathMetadataObservation>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ProjectRootBasis {
    Resolved,
    LexicalAbsolute,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NonGitProjectRoot {
    pub path: MachinePath,
    pub basis: ProjectRootBasis,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DataRootSource {
    XdgStateHome,
    HomeLocalStateFallback,
    MacosApplicationSupport,
    WindowsLocalAppData,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DataRootObservation {
    pub path: MachinePath,
    pub source: DataRootSource,
    pub ignored_relative_xdg_state_home: bool,
}

#[derive(Debug, Clone, Copy)]
pub struct DataRootInputs<'a> {
    pub xdg_state_home: Option<&'a Path>,
    pub home: Option<&'a Path>,
    pub macos_application_support: Option<&'a Path>,
    pub windows_local_app_data: Option<&'a Path>,
}

#[cfg(unix)]
pub fn machine_path_from_path(path: &Path) -> Result<MachinePath, ProjectObservationError> {
    MachinePath::unix_bytes(path.as_os_str().as_bytes().to_vec()).map_err(Into::into)
}

#[cfg(windows)]
pub fn machine_path_from_path(path: &Path) -> Result<MachinePath, ProjectObservationError> {
    MachinePath::windows_wtf16(path.as_os_str().encode_wide().collect()).map_err(Into::into)
}

#[cfg(not(any(unix, windows)))]
pub fn machine_path_from_path(_path: &Path) -> Result<MachinePath, ProjectObservationError> {
    Err(ProjectObservationError::UnsupportedPlatform)
}

pub fn lexical_absolute_path(
    input: &Path,
    lexical_base: &Path,
) -> Result<PathBuf, ProjectObservationError> {
    if input.as_os_str().is_empty() {
        return Err(ProjectObservationError::EmptyInput);
    }

    #[cfg(windows)]
    if !input.is_absolute()
        && (input.has_root() || matches!(input.components().next(), Some(Component::Prefix(_))))
    {
        return Err(ProjectObservationError::PlatformRelativePathUnsupported);
    }

    let combined = if input.is_absolute() {
        input.to_path_buf()
    } else {
        if !lexical_base.is_absolute() {
            return Err(ProjectObservationError::LexicalBaseNotAbsolute);
        }
        lexical_base.join(input)
    };

    normalize_absolute(&combined)
}

fn normalize_absolute(path: &Path) -> Result<PathBuf, ProjectObservationError> {
    if !path.is_absolute() {
        return Err(ProjectObservationError::LexicalBaseNotAbsolute);
    }

    let mut normalized = PathBuf::new();
    let mut normal_depth = 0usize;

    for component in path.components() {
        match component {
            Component::Prefix(prefix) => normalized.push(prefix.as_os_str()),
            Component::RootDir => normalized.push(component.as_os_str()),
            Component::CurDir => {}
            Component::ParentDir => {
                if normal_depth > 0 {
                    normalized.pop();
                    normal_depth -= 1;
                }
            }
            Component::Normal(value) => {
                normalized.push(value);
                normal_depth += 1;
            }
        }
    }

    Ok(normalized)
}

pub fn classify_path_io_error(error: &io::Error) -> ObservationErrorClass {
    if is_symlink_loop(error) {
        return ObservationErrorClass::SymlinkLoop;
    }

    match error.kind() {
        io::ErrorKind::NotFound => ObservationErrorClass::NotFound,
        io::ErrorKind::PermissionDenied => ObservationErrorClass::PermissionDenied,
        io::ErrorKind::InvalidInput | io::ErrorKind::InvalidData => {
            ObservationErrorClass::InvalidPath
        }
        io::ErrorKind::Unsupported => ObservationErrorClass::Unsupported,
        _ => ObservationErrorClass::Io,
    }
}

#[cfg(target_os = "linux")]
fn is_symlink_loop(error: &io::Error) -> bool {
    error.raw_os_error() == Some(40)
}

#[cfg(target_os = "macos")]
fn is_symlink_loop(error: &io::Error) -> bool {
    error.raw_os_error() == Some(62)
}

#[cfg(windows)]
fn is_symlink_loop(error: &io::Error) -> bool {
    error.raw_os_error() == Some(1921)
}

#[cfg(not(any(target_os = "linux", target_os = "macos", windows)))]
fn is_symlink_loop(_error: &io::Error) -> bool {
    false
}

pub fn observe_project_locator(
    input: &Path,
    lexical_base: &Path,
    observation_time: UnixMillis,
) -> Result<ProjectLocator, ProjectObservationError> {
    let lexical = lexical_absolute_path(input, lexical_base)?;
    let input_path = machine_path_from_path(input)?;
    let lexical_absolute_path = machine_path_from_path(&lexical)?;
    let resolved_path = match std::fs::canonicalize(&lexical) {
        Ok(path) => Observation::Available {
            value: machine_path_from_path(&path)?,
        },
        Err(error) => Observation::Unavailable {
            error: classify_path_io_error(&error),
        },
    };

    Ok(ProjectLocator {
        schema_version: ProjectContractVersion::V1,
        input_path,
        lexical_absolute_path,
        resolved_path,
        observation_time,
    })
}

pub fn observe_path_metadata(
    lexical_absolute_path: &Path,
) -> Result<PathMetadataTrail, ProjectObservationError> {
    if !lexical_absolute_path.is_absolute() {
        return Err(ProjectObservationError::ObservedPathNotAbsolute);
    }
    let normal_components = lexical_absolute_path
        .components()
        .filter(|component| matches!(component, Component::Normal(_)))
        .count();
    if normal_components > MAX_PATH_COMPONENT_OBSERVATIONS {
        return Err(ProjectObservationError::PathTooDeep {
            components: normal_components,
            max: MAX_PATH_COMPONENT_OBSERVATIONS,
        });
    }

    let mut current = PathBuf::new();
    let mut observations = Vec::with_capacity(normal_components);

    for component in lexical_absolute_path.components() {
        current.push(component.as_os_str());
        if !matches!(component, Component::Normal(_)) {
            continue;
        }

        let path = machine_path_from_path(&current)?;
        match std::fs::symlink_metadata(&current) {
            Ok(metadata) => observations.push(PathMetadataObservation {
                path,
                entry_kind: Observation::Available {
                    value: entry_kind(&metadata),
                },
                reparse_point: reparse_point(&metadata),
            }),
            Err(error) => {
                observations.push(PathMetadataObservation {
                    path,
                    entry_kind: Observation::Unavailable {
                        error: classify_path_io_error(&error),
                    },
                    reparse_point: OptionalObservation::Unavailable {
                        error: classify_path_io_error(&error),
                    },
                });
                break;
            }
        }
    }

    Ok(PathMetadataTrail {
        components: observations,
    })
}

fn entry_kind(metadata: &std::fs::Metadata) -> PathEntryKind {
    let file_type = metadata.file_type();
    if file_type.is_symlink() {
        PathEntryKind::Symlink
    } else if file_type.is_dir() {
        PathEntryKind::Directory
    } else if file_type.is_file() {
        PathEntryKind::File
    } else {
        PathEntryKind::Other
    }
}

#[cfg(windows)]
fn reparse_point(metadata: &std::fs::Metadata) -> OptionalObservation<bool> {
    OptionalObservation::Value {
        value: metadata.file_attributes() & WINDOWS_FILE_ATTRIBUTE_REPARSE_POINT != 0,
    }
}

#[cfg(not(windows))]
fn reparse_point(_metadata: &std::fs::Metadata) -> OptionalObservation<bool> {
    OptionalObservation::None
}

pub fn observe_non_git_project_root(
    locator: &ProjectLocator,
    lexical_absolute_path: &Path,
) -> Result<Observation<NonGitProjectRoot>, ProjectObservationError> {
    if !lexical_absolute_path.is_absolute() {
        return Err(ProjectObservationError::ObservedPathNotAbsolute);
    }

    match &locator.resolved_path {
        Observation::Available {
            value: first_resolved,
        } => {
            let resolved = match std::fs::canonicalize(lexical_absolute_path) {
                Ok(path) => path,
                Err(_) => {
                    return Ok(Observation::Unavailable {
                        error: ObservationErrorClass::RaceDetected,
                    });
                }
            };
            let second_resolved = machine_path_from_path(&resolved)?;
            if &second_resolved != first_resolved {
                return Ok(Observation::Unavailable {
                    error: ObservationErrorClass::RaceDetected,
                });
            }
            match std::fs::symlink_metadata(&resolved) {
                Ok(metadata) if metadata.file_type().is_dir() => Ok(Observation::Available {
                    value: NonGitProjectRoot {
                        path: second_resolved,
                        basis: ProjectRootBasis::Resolved,
                    },
                }),
                Ok(_) => Ok(Observation::Unavailable {
                    error: ObservationErrorClass::InvalidPath,
                }),
                Err(_) => Ok(Observation::Unavailable {
                    error: ObservationErrorClass::RaceDetected,
                }),
            }
        }
        Observation::Unavailable { error } => {
            match std::fs::symlink_metadata(lexical_absolute_path) {
                Ok(metadata) if metadata.file_type().is_dir() => {
                    if matches!(
                        error,
                        ObservationErrorClass::NotFound
                            | ObservationErrorClass::InvalidPath
                            | ObservationErrorClass::SymlinkLoop
                    ) {
                        return Ok(Observation::Unavailable {
                            error: ObservationErrorClass::RaceDetected,
                        });
                    }
                    Ok(Observation::Available {
                        value: NonGitProjectRoot {
                            path: machine_path_from_path(lexical_absolute_path)?,
                            basis: ProjectRootBasis::LexicalAbsolute,
                        },
                    })
                }
                Ok(metadata) if metadata.file_type().is_symlink() => {
                    Ok(Observation::Unavailable { error: *error })
                }
                Ok(_) => Ok(Observation::Unavailable {
                    error: ObservationErrorClass::InvalidPath,
                }),
                Err(metadata_error) => Ok(Observation::Unavailable {
                    error: classify_path_io_error(&metadata_error),
                }),
            }
        }
    }
}

#[cfg(target_os = "linux")]
pub fn platform_data_root(
    inputs: DataRootInputs<'_>,
) -> Result<DataRootObservation, ProjectObservationError> {
    if let Some(xdg_state_home) = inputs.xdg_state_home
        && xdg_state_home.is_absolute()
    {
        return data_root_from_base(xdg_state_home, "wepld", DataRootSource::XdgStateHome, false);
    }

    let home = inputs
        .home
        .ok_or(ProjectObservationError::DataRootBaseUnavailable)?;
    if !home.is_absolute() {
        return Err(ProjectObservationError::DataRootBaseNotAbsolute);
    }
    data_root_from_base(
        &home.join(".local").join("state"),
        "wepld",
        DataRootSource::HomeLocalStateFallback,
        inputs.xdg_state_home.is_some(),
    )
}

#[cfg(target_os = "macos")]
pub fn platform_data_root(
    inputs: DataRootInputs<'_>,
) -> Result<DataRootObservation, ProjectObservationError> {
    let application_support = inputs
        .macos_application_support
        .ok_or(ProjectObservationError::DataRootBaseUnavailable)?;
    data_root_from_base(
        application_support,
        "WePLD",
        DataRootSource::MacosApplicationSupport,
        false,
    )
}

#[cfg(windows)]
pub fn platform_data_root(
    inputs: DataRootInputs<'_>,
) -> Result<DataRootObservation, ProjectObservationError> {
    let local_app_data = inputs
        .windows_local_app_data
        .ok_or(ProjectObservationError::DataRootBaseUnavailable)?;
    data_root_from_base(
        local_app_data,
        "WePLD",
        DataRootSource::WindowsLocalAppData,
        false,
    )
}

#[cfg(not(any(target_os = "linux", target_os = "macos", windows)))]
pub fn platform_data_root(
    _inputs: DataRootInputs<'_>,
) -> Result<DataRootObservation, ProjectObservationError> {
    Err(ProjectObservationError::UnsupportedPlatform)
}

fn data_root_from_base(
    base: &Path,
    application_component: &str,
    source: DataRootSource,
    ignored_relative_xdg_state_home: bool,
) -> Result<DataRootObservation, ProjectObservationError> {
    if !base.is_absolute() {
        return Err(ProjectObservationError::DataRootBaseNotAbsolute);
    }
    let path = base.join(application_component);
    Ok(DataRootObservation {
        path: machine_path_from_path(&path)?,
        source,
        ignored_relative_xdg_state_home,
    })
}
