# WePLD PR #136 Agile Static Dependency Metadata Qualification

```text
DOCUMENT_DATE=2026-08-24
EVIDENCE_CLASS=STATIC_DEPENDENCY_METADATA_RESOLUTION
SUBJECT_PR=136
SUBJECT_HEAD=28f0023b8ffb90c585213762dae5f4c1d57322ef
SUBJECT_PYPROJECT_GIT_BLOB=6d7152f8debe8620cc98c3ab33bf0565b591434c
CANONICAL_BASE_MAIN=08a06e9f2664735eb55db5b2f49f95d3d3f91c3f
OBSERVED_AT_UTC=2026-08-24T06:47:00Z
AUTHORITY=AGILE_DEPENDENCY_METADATA_RESOLUTION_ONLY

DEPENDENCY_ADMISSION=NONE
DEPENDENCIES_INSTALLED=NO
PACKAGE_IMPORT_OR_EXECUTION=NONE
PEP517_BUILD_HOOK_EXECUTION=NONE
SETUP_PY_EXECUTION=NONE
DONOR_CODE_EXECUTION=NONE
DONOR_WORKFLOW_EXECUTION=NONE
DONOR_HOOK_EXECUTION=NONE
DONOR_INSTALL_SCRIPT_EXECUTION=NONE
MODEL_PROVIDER_EXECUTION=NONE
MODEL_WEIGHT_ACCESS=NONE
MODEL_INFERENCE=NONE
PRODUCT_IMPLEMENTATION_AUTHORITY=NONE
PRODUCT_RUNTIME_ADMISSION=NONE
H0_014_PLUS=NOT_STARTED
H0_SCREEN_EXECUTION=NONE
```

## Bound declaration

The exact `vendor/agile/pyproject.toml` at the bound head requires Python `>=3.11` and declares these runtime requirements:

```text
typer>=0.24.0
click>=8.2.1
rich
platformdirs
readchar
pyyaml>=6.0
packaging>=23.0
pathspec>=0.12.0
json5>=0.13.0
```

`hatchling` is build-only. `pytest>=7.0` and `pytest-cov>=4.0` are optional test dependencies. They are inventoried but excluded from the runtime SBOM. No build/test dependency was installed or executed.

## Resolution method

```text
INDEX=PUBLIC_PYPI_METADATA
SELECTION=LATEST_NON_YANKED_STABLE_SATISFYING_ACTIVE_CONSTRAINTS
PYTHON_BASELINE=>=3.11
EXTRAS=NONE
PEP508_ENVIRONMENT_MARKERS=PRESERVED
DONOR_LOCKFILE=ABSENT
RESOLUTION_CLASS=EXTERNALLY_RECONSTRUCTED_METADATA_GRAPH
```

This is not represented as a donor-authored lock and grants no dependency admission.

## Resolved graph

```text
UNCONDITIONAL_PACKAGE_IDENTITIES=14
WINDOWS_CONDITIONAL_PACKAGE_IDENTITIES=1
TOTAL_PARAMETERIZED_PACKAGE_IDENTITIES=15

wepld-agile
├── typer 0.27.1
│   ├── shellingham 1.5.4
│   ├── rich 15.0.0
│   │   ├── markdown-it-py 4.2.0
│   │   │   └── mdurl 0.1.2
│   │   └── Pygments 2.20.0
│   ├── annotated-doc 0.0.5
│   └── colorama 0.4.6 [platform_system == "Windows"]
├── click 8.4.2
│   └── colorama 0.4.6 [platform_system == "Windows"]
├── rich 15.0.0
├── platformdirs 4.11.2
├── readchar 4.2.2
├── PyYAML 6.0.3
├── packaging 26.3
├── pathspec 1.1.1
└── json5 0.15.0
```

Typer 0.27.1 states that Typer has vendored Click since 0.26.0. Agile separately declares external Click. The embedded Click code is recorded as an embedded-code surface inside Typer, not fabricated as a second PyPI dependency identity.

## Package identities

| Package | Version | Scope | Artifact | SHA-256 | Published license |
|---|---:|---|---|---|---|
| `typer` | `0.27.1` | direct | wheel | `53150287edd11baeb4e4722c8e394fcdf8181c0ae89485cba8d25c778d5edd56` | MIT |
| `click` | `8.4.2` | direct | wheel | `e6f9f66136c816745b9d65817da91d61d957fb16e02e4dcd0552553c5a197b76` | BSD-3-Clause |
| `rich` | `15.0.0` | direct | wheel | `33bd4ef74232fb73fe9279a257718407f169c09b78a87ad3d296f548e27de0bb` | MIT |
| `platformdirs` | `4.11.2` | direct | wheel | `7f89089b6ea71bda7962953edcf784b2e2d9d285b40ad88be2bb75c6e9d82ab4` | MIT |
| `readchar` | `4.2.2` | direct | wheel | `92daf7e42c52b0787e6c75d01ecfb9a94f4ceff3764958b570c1dddedd47b200` | MIT |
| `PyYAML` | `6.0.3` | direct | sdist | `d76623373421df22fb4cf8817020cbb7ef15c725b9d5e45f17e189bfc384190f` | MIT |
| `packaging` | `26.3` | direct | wheel | `d7193f7c8e4e93f444fde0262bf90af30e16fa0ad0ad44cb553c87339b23cd1c` | Apache-2.0 OR BSD-2-Clause |
| `pathspec` | `1.1.1` | direct | wheel | `a00ce642f577bf7f473932318056212bc4f8bfdf53128c78bbd5af0b9b20b189` | MPL-2.0 |
| `json5` | `0.15.0` | direct | wheel | `56636a30c0e8a4665fe2179c0212f32eae3796dea89ea6f649b9436ecdb39618` | Apache-2.0 |
| `shellingham` | `1.5.4` | transitive | wheel | `7ecfff8f2fd72616f7481040475a65b2bf8af90a56c89140852d1120324e8686` | ISC |
| `annotated-doc` | `0.0.5` | transitive | wheel | `117bac03a25ede5df5440e855b32d556049ca169ead221505badf432fed4b101` | MIT |
| `markdown-it-py` | `4.2.0` | transitive | wheel | `9f7ebbcd14fe59494226453aed97c1070d83f8d24b6fc3a3bcf9a38092641c4a` | MIT |
| `Pygments` | `2.20.0` | transitive | wheel | `81a9e26dd42fd28a23a2d169d86d7ac03b46e2f8b59ed4698fb4785f946d0176` | BSD-2-Clause |
| `mdurl` | `0.1.2` | transitive | wheel | `84008a41e51615a49fc9966191ff91509e3c40b939176e643fd50a5c2196b8f8` | MIT |
| `colorama` | `0.4.6` | conditional | wheel | `4f1d9991f5acc0ca119f9d443620b77f9d6b33703e51011c16baf57afb285fc6` | BSD-3-Clause |

PyYAML uses its source-distribution SHA-256 because its wheels are target-specific. All other hashes above bind the selected universal wheel.

For all 15 selected version identities, the observed PyPI version metadata reported an empty `vulnerabilities` array.

```text
PYPI_VERSION_IDENTITIES_CHECKED=15
PYPI_REPORTED_VULNERABILITIES=0
INDEPENDENT_PYTHON_ADVISORY_DATABASE_SNAPSHOT=NOT_PINNED
GLOBAL_NO_VULNERABILITY_CLAIM=FORBIDDEN
```

The result means only that the selected PyPI metadata source reported no vulnerabilities at the observation point.

## Supply-chain findings

1. No Agile lockfile exists, so the donor snapshot itself does not prove a resolved transitive environment.
2. `colorama==0.4.6` is conditional on Windows.
3. PyYAML runtime admission would require target-specific artifact/lock evidence.
4. Typer vendors Click internally while Agile also declares external Click.
5. Shellingham 1.5.4, mdurl 0.1.2, and colorama 0.4.6 have older latest-release dates; this is a maintenance-review signal, not an unmaintained claim.
6. Published license declarations are recorded, but redistribution/license-file/NOTICE admission is not performed.
7. No package, hook, build backend, test, provider, model, credential, or runtime surface was executed.

## CycloneDX artifact

The complete deterministic package-level runtime SBOM is stored beside this report:

```text
PATH=docs/acquisition/WEPLD_PR136_AGILE_RUNTIME_METADATA_SBOM_2026-08-24.cdx.md
FORMAT=CYCLONEDX_JSON_EMBEDDED_IN_MARKDOWN
SPEC_VERSION=1.5
SERIAL=urn:uuid:29aad68c-5988-59de-bb31-ce58661f18d9
PAYLOAD_SHA256=4317c72dac0b103df0b2378e034766933f4688acbf8fb7f605e65e1840d105ff
HASH_INPUT=EXACT_JSON_PAYLOAD_PLUS_ONE_TRAILING_LF
```

The `.md` wrapper preserves the current docs-only evidence posture; the fenced payload itself is valid CycloneDX JSON after exact extraction.

## Update / exit

```text
UPDATE_PLAN=NEW_CONTENT_ADDRESSED_RESOLUTION_PLUS_FULL_REQUALIFICATION
EXIT_STRATEGY=PRESERVE_WEPLD_OWNED_AGILE_CONTRACTS_AND_REMOVE_OR_REPLACE_PACKAGE_GRAPH
```

## Verdict

```text
AGILE_RUNTIME_DECLARATION_INVENTORY=PASS
AGILE_METADATA_RESOLUTION_CLOSURE=PASS
AGILE_PARAMETERIZED_RUNTIME_GRAPH=PASS
AGILE_PACKAGE_LEVEL_CYCLONEDX_SBOM=PASS
AGILE_SELECTED_ARTIFACT_HASH_BINDING=PASS
AGILE_PYPI_ADVISORY_OBSERVATION=PASS_NO_REPORTED_VULNERABILITIES

AGILE_DONOR_AUTHORED_RESOLVED_LOCK=NOT_PROVEN
AGILE_INDEPENDENT_ADVISORY_DB_SNAPSHOT=NOT_PROVEN
AGILE_TARGET_SPECIFIC_PYYAML_ARTIFACT_SET=NOT_ADMITTED
AGILE_RUNTIME_LICENSE_NOTICE_ADMISSION=NOT_PERFORMED
AGILE_DEPENDENCY_ADMISSION=NONE

PR136_SOURCE_HEAD_MUTATED=NO
PR136_READY=NO
PR136_MERGE=NO
```

## Remaining canonical gates

```text
PICTORIAL_FORMAL_COMPLETE_SBOM=NOT_RECORDED_BY_THIS_EVIDENCE
MIREFA_NAWAT_ADAPTER_IMPLEMENTATION=BLOCKED_BY_PRODUCT_IMPLEMENTATION_AUTHORITY
DONOR_PARITY_EXECUTION=BLOCKED_BY_DONOR_EXECUTION_AUTHORITY
WEPLD_RUNTIME_AUTHORITY_TESTS=NOT_EXECUTED
INDEPENDENT_EXACT_HEAD_REVIEW_OF_PR136=NOT_PROVEN
FINAL_CLEAN_RACE=NOT_ELIGIBLE
```

This evidence advances only static Agile dependency/SBOM qualification. It grants no dependency, runtime, product, model, or completion authority.
