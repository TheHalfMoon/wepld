# WePLD PR #136 Agile Independent Advisory Qualification

```text
DOCUMENT_DATE=2026-08-24
EVIDENCE_CLASS=STATIC_INDEPENDENT_ADVISORY_DATABASE_QUALIFICATION
SUBJECT_PR=136
SUBJECT_HEAD=28f0023b8ffb90c585213762dae5f4c1d57322ef
SUBJECT_PYPROJECT_GIT_BLOB=6d7152f8debe8620cc98c3ab33bf0565b591434c
RESOLUTION_EVIDENCE_PR=159
RESOLUTION_EVIDENCE_PRIOR_HEAD=b45c785cee9c2b6b0e0b4c6ad4cb0c8329d2ee40

ADVISORY_DATABASE=pypa/advisory-database
ADVISORY_DATABASE_COMMIT=071b32d25546bb337f19bb72c90392a020f5759a
ADVISORY_DATABASE_TREE=1fd75eee954b79371365efe66186657defaa00f8
ADVISORY_DATABASE_COMMIT_DATE_UTC=2026-08-21T15:30:24Z

DEPENDENCY_ADMISSION=NONE
PACKAGE_INSTALLATION=NONE
PACKAGE_IMPORT_OR_EXECUTION=NONE
DONOR_CODE_EXECUTION=NONE
MODEL_PROVIDER_EXECUTION=NONE
PRODUCT_RUNTIME_ADMISSION=NONE
```

## Method

The 15 exact package/version identities in the metadata-resolution evidence were checked against the immutable PyPA advisory-database snapshot above. The check was repository-data-only: inspect the exact `vulns/<normalized-package>/` directory at the pinned commit, then inspect every advisory record present for that package and compare its ecosystem affected/fixed range with the selected version.

No advisory scanner binary, package manager, package, donor code, build backend, hook, test, provider, credential, or runtime surface was executed.

## Selected identities

```text
typer==0.27.1
click==8.4.2
rich==15.0.0
platformdirs==4.11.2
readchar==4.2.2
PyYAML==6.0.3
packaging==26.3
pathspec==1.1.1
json5==0.15.0
shellingham==1.5.4
annotated-doc==0.0.5
markdown-it-py==4.2.0
Pygments==2.20.0
mdurl==0.1.2
colorama==0.4.6 [Windows conditional]
```

## Snapshot inventory result

```text
PACKAGE_IDENTITIES_CHECKED=15
PACKAGES_WITH_ADVISORY_DIRECTORIES=4
PACKAGES_WITHOUT_ADVISORY_DIRECTORIES=11
TOTAL_ADVISORY_RECORDS_REVIEWED=12
SELECTED_IDENTITIES_AFFECTED=0
```

Packages with records:

### click 8.4.2

```text
PYSEC-2026-2132
AFFECTED=<8.3.3
FIXED=8.3.3
SELECTED=8.4.2
DISPOSITION=NOT_AFFECTED
```

### PyYAML 6.0.3

```text
PYSEC-2018-49     FIXED=5.1    SELECTED=6.0.3 DISPOSITION=NOT_AFFECTED
PYSEC-2020-176    FIXED=5.2b1  SELECTED=6.0.3 DISPOSITION=NOT_AFFECTED
PYSEC-2020-96     FIXED=5.3.1  SELECTED=6.0.3 DISPOSITION=NOT_AFFECTED
PYSEC-2021-142    FIXED=5.4    SELECTED=6.0.3 DISPOSITION=NOT_AFFECTED
```

### markdown-it-py 4.2.0

```text
PYSEC-2023-23     FIXED=2.2.0  SELECTED=4.2.0 DISPOSITION=NOT_AFFECTED
PYSEC-2023-24     FIXED=2.2.0  SELECTED=4.2.0 DISPOSITION=NOT_AFFECTED
```

### Pygments 2.20.0

```text
PYSEC-2016-32     FIXED=2.1     SELECTED=2.20.0 DISPOSITION=NOT_AFFECTED
PYSEC-2021-140    FIXED=2.7.4   SELECTED=2.20.0 DISPOSITION=NOT_AFFECTED
PYSEC-2021-141    FIXED=2.7.4   SELECTED=2.20.0 DISPOSITION=NOT_AFFECTED
PYSEC-2023-117    FIXED=2.15.1  SELECTED=2.20.0 DISPOSITION=NOT_AFFECTED
PYSEC-2026-2987   FIXED=2.20.0  SELECTED=2.20.0 DISPOSITION=NOT_AFFECTED
```

Packages without a `vulns/<package>/` directory at the exact pinned snapshot:

```text
typer
rich
platformdirs
readchar
packaging
pathspec
json5
shellingham
annotated-doc
mdurl
colorama
```

Absence of a package directory is interpreted only as absence from this exact database snapshot. It is not a universal claim that no vulnerability exists.

## Reconciliation with PyPI observation

The prior metadata-resolution evidence observed an empty PyPI `vulnerabilities` array for all 15 selected version identities. The independent immutable PyPA advisory-database snapshot now provides a second source and finds zero selected identities inside an affected ecosystem range.

```text
PYPI_REPORTED_VULNERABILITIES=0
PYPA_PINNED_SNAPSHOT_AFFECTED_IDENTITIES=0
CROSS_SOURCE_RESULT=CONSISTENT
```

This still does not establish universal absence of undisclosed vulnerabilities, future advisories, malicious-package risk, package provenance trust, or runtime safety.

## Security / supply-chain verdict

```text
AGILE_INDEPENDENT_ADVISORY_DB_SNAPSHOT=PINNED
AGILE_INDEPENDENT_ADVISORY_DB_TREE=PINNED
AGILE_SELECTED_VERSION_RANGE_RECONCILIATION=PASS
AGILE_SELECTED_IDENTITIES_KNOWN_AFFECTED_IN_PINNED_PYPA_DB=0
AGILE_STATIC_ADVISORY_QUALIFICATION=PASS

DEPENDENCY_ADMISSION=NONE
RUNTIME_ADMISSION=NONE
PRODUCT_IMPLEMENTATION_AUTHORITY=NONE
PR136_READY=NO
PR136_MERGE=NO
```

## Remaining limitations

```text
DONOR_AUTHORED_AGILE_LOCKFILE=ABSENT
TARGET_SPECIFIC_PYYAML_WHEEL_SET=NOT_ADMITTED
RUNTIME_LICENSE_NOTICE_ADMISSION=NOT_PERFORMED
PACKAGE_PROVENANCE_ATTESTATION=NOT_PROVEN
FUTURE_ADVISORY_RECHECK_BEFORE_ANY_DEPENDENCY_ADMISSION=REQUIRED
```

This document supersedes only the earlier `INDEPENDENT_PYTHON_ADVISORY_DATABASE_SNAPSHOT=NOT_PINNED` limitation in the PR #159 metadata-resolution report. It does not change any other limitation or grant any new authority.
