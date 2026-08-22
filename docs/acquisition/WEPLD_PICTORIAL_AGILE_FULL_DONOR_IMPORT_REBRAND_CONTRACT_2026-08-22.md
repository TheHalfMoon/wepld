# WePLD Pictorial + Agile Full Donor Import / Rebrand Contract

```text
DOCUMENT_DATE = 2026-08-22
BASE_MAIN = 27886783008bd594f95b8d1439fff74bb87914f3
WORKSTREAM = PICTORIAL_AND_AGILE_FULL_DONOR_IMPORT
STATUS = AUTHORIZED_TO_PREPARE_FULL_TRACKED_SOURCE_IMPORT

PICTORIAL_USER_NAME = Pictorial
PICTORIAL_UPSTREAM = pbakaus/impeccable
PICTORIAL_UPSTREAM_REVISION = 56f44523f76efdcec813e67b38ee550e49b16f48
PICTORIAL_UPSTREAM_TREE = 3626999bc9c8be4d31f3028c37c74cf544576d15
PICTORIAL_LICENSE = Apache-2.0
PICTORIAL_LICENSE_BLOB = bb3f6d23b1f8025514a62a12b51b47d73e3c9aa9

AGILE_USER_NAME = Agile
AGILE_UPSTREAM = github/spec-kit
AGILE_UPSTREAM_REVISION = 27f50f7e6b618ea14d74dd4037f9e7c60218b16c
AGILE_UPSTREAM_TREE = 5622442d5ff74d21b2cb4349f255d08380f3d69d
AGILE_LICENSE = MIT
AGILE_LICENSE_BLOB = 28a50fa22639e32febe14e4ffc7a732b0ba8c90a

IMPORT_MODE = FULL_TRACKED_SOURCE_SNAPSHOT + DERIVATIVE_REBRAND + WEPLD_ADAPTERS
GIT_HISTORY_IMPORT = NOT_REQUIRED
UPSTREAM_AUTO_UPDATE = FORBIDDEN
UPSTREAM_WORKFLOW_AUTO_EXECUTION = FORBIDDEN
RUNTIME_DEPENDENCY_ADMISSION = SEPARATE_GATE
USER_VISIBLE_UPSTREAM_BRANDING = FORBIDDEN
LEGAL_AND_PROVENANCE_ATTRIBUTION = REQUIRED
```

## Founder decision

WePLD will absorb the complete functional source surface of both donors at the exact pinned revisions above and expose them as first-class WePLD capabilities named **Pictorial** and **Agile**.

A GitHub fork is not the target architecture. A fork preserves upstream repository identity and branding in the product-development surface. WePLD instead uses pinned derivative source snapshots behind WePLD-owned contracts so the capabilities are versioned, replaceable, security-qualified, and presented as one unified system.

The earlier `REFERENCE_ONLY` / `SOURCE_MINE_ADAPT` posture for these donor families is superseded for this new workstream by the explicit founder decision in this document. Historical S1 records remain historical truth and are not rewritten retroactively.

## Product naming contract

End users must see only these names:

```text
Pictorial
Agile
```

The following upstream brands or package identities must never appear in normal product UI, command help, generated project files, prompts shown to users, logs intended for users, settings, feature names, onboarding, documentation shipped as WePLD product documentation, or public capability labels:

```text
Impeccable
impeccable
Spec Kit
spec-kit
speckit
specify-cli
```

Legal attribution and maintainer provenance are the only exceptions. Upstream repository names/URLs may appear only in dedicated legal/provenance records and in preserved notices that the applicable license requires.

This is a rebrand, not an attempt to erase authorship.

## Deterministic rename map

### Pictorial

```text
product name: Impeccable -> Pictorial
npm/package identity: impeccable -> @wepld/pictorial
CLI: impeccable -> pictorial
integrated CLI: wepld pictorial
config root: .impeccable -> .pictorial
config names: impeccable.* -> pictorial.*
environment prefix: IMPECCABLE_* -> PICTORIAL_*
agent names: impeccable-* -> pictorial-*
skill names: impeccable -> pictorial
internal user-visible labels/messages/URLs -> Pictorial / WePLD-owned equivalents
```

### Agile

```text
product name: Spec Kit -> Agile
Python distribution: specify-cli -> wepld-agile
Python package/module namespace: specify_cli -> agile_cli or WePLD-owned adapter namespace
CLI: specify -> agile
integrated CLI: wepld agile
workflow label/path: speckit -> agile
product-facing config/cache names -> agile
product-facing environment prefix -> AGILE_*
product-facing docs/help/templates -> Agile / WePLD-owned equivalents
```

Ordinary English uses of the verb "specify" are not prohibited; the old CLI/product identity is.

## Full-source meaning

`FULL_TRACKED_SOURCE_SNAPSHOT` means every tracked upstream file at the pinned revision is accounted for in the import manifest. A file may be:

1. imported and mechanically rebranded;
2. imported but kept inert because it is repository administration, CI, release, community, or provider-specific machinery;
3. replaced by a WePLD-owned equivalent with an explicit source-map record; or
4. excluded only by an explicit security/license/architecture finding with a recorded reason.

Nothing may silently disappear.

Imported upstream `.github/workflows`, release automation, hooks, install scripts, telemetry, network behavior, package publishing, or provider integrations are **data only** until separately qualified. They must not become active WePLD authority or execute merely because they were copied.

## Pictorial functional parity target

Pictorial inherits the complete useful design-system surface of the pinned donor, including design skills, commands, critique, audit, polish, harden, layout, accessibility/design anti-pattern detection, CLI behavior, browser/live design behavior, agent adapters, extension behavior, assets, tests, fixtures, and supporting scripts.

The objective is functional parity or a documented WePLD-superior replacement. A capability must not be silently dropped because its upstream name is removed.

Pictorial is the WePLD design-intelligence and design-assurance capability. It may inspect, critique, propose, transform, and validate UI/UX work. It is not Trusted Core, protocol authority, completion authority, or permission authority. When v0 or another builder produces UI, Pictorial may shape/critique/audit/polish/harden that output, but the builder does not become authority through Pictorial.

## Agile functional parity target

Agile inherits the complete useful specification-development surface of the pinned donor, including project bootstrap, constitution, specification, clarification, planning, task decomposition, analysis, templates, scripts, presets, extensions, workflows, bundles, integrations, air-gapped behavior, tests, and supporting CLI machinery.

The objective is functional parity or a documented WePLD-superior replacement. Agile is the WePLD specification and delivery-method capability; it does not own permissions, secrets, effects, canonical completion, deployment, merge, or Trusted Core state.

## WePLD architecture placement

```text
Mirefa
  -> qualifies, versions, composes, routes, monitors, replaces, or revokes Pictorial and Agile

Agile
  -> specification / constitution / plan / tasks / analyze / workflow mechanics

Pictorial
  -> design intelligence / critique / audit / polish / harden / design QA

Fehrest
  -> context and project intelligence; never authority

Edara
  -> minimum-sufficient worker topology

Nawat
  -> effect-time authorization and revalidation

Trusted Completion
  -> independent completion decision
```

Required invariants:

```text
PICTORIAL != AUTHORITY
AGILE != AUTHORITY
DONOR_SOURCE != AUTHORITY
DONOR_CONFIG != AUTHORITY
DONOR_WORKFLOW != AUTHORITY
DONOR_REVIEW != COMPLETION_DECISION
MIREFA_QUALIFIES != NAWAT_AUTHORIZES
```

## Legal / attribution boundary

Pictorial's donor is Apache-2.0. Redistribution therefore must preserve the Apache-2.0 license, relevant copyright/patent/trademark/attribution notices, and modification notices required by the license. The current upstream `LICENSE` contains `Copyright 2025 Paul Bakaus`. No upstream `NOTICE` file was present at the pinned revision when checked.

Agile's donor is MIT. Redistribution must preserve the MIT copyright and permission notice; the pinned upstream license states `Copyright GitHub, Inc.`.

The product rebrand must not imply that WePLD authored the upstream work originally. Legal/provenance files remain available to maintainers and recipients even though the normal product surface uses only Pictorial and Agile.

## Embedded immutable provenance records

These machine-readable records replace separate provenance files during this authorization stage so the candidate remains inside the currently permitted acquisition-document surface. They are immutable evidence inputs for the later full source-map generation.

```json
{
  "component": "Pictorial",
  "component_role": "WePLD design intelligence and design assurance",
  "upstream_repository": "pbakaus/impeccable",
  "upstream_url": "https://github.com/pbakaus/impeccable",
  "upstream_revision": "56f44523f76efdcec813e67b38ee550e49b16f48",
  "upstream_tree": "3626999bc9c8be4d31f3028c37c74cf544576d15",
  "upstream_license": "Apache-2.0",
  "upstream_license_blob": "bb3f6d23b1f8025514a62a12b51b47d73e3c9aa9",
  "upstream_notice_file": null,
  "import_mode": "full_tracked_source_snapshot_derivative_rebrand",
  "user_facing_upstream_brand_allowed": false,
  "legal_provenance_retention_required": true,
  "runtime_authority": "none",
  "automatic_update": false,
  "full_path_map_status": "pending_source_import"
}
```

```json
{
  "component": "Agile",
  "component_role": "WePLD specification and delivery-method capability",
  "upstream_repository": "github/spec-kit",
  "upstream_url": "https://github.com/github/spec-kit",
  "upstream_revision": "27f50f7e6b618ea14d74dd4037f9e7c60218b16c",
  "upstream_tree": "5622442d5ff74d21b2cb4349f255d08380f3d69d",
  "upstream_license": "MIT",
  "upstream_license_blob": "28a50fa22639e32febe14e4ffc7a732b0ba8c90a",
  "import_mode": "full_tracked_source_snapshot_derivative_rebrand",
  "user_facing_upstream_brand_allowed": false,
  "legal_provenance_retention_required": true,
  "runtime_authority": "none",
  "automatic_update": false,
  "full_path_map_status": "pending_source_import"
}
```

## Source-map requirement

The full import must produce machine-readable provenance maps with, for every upstream tracked path:

```text
upstream_repository
upstream_revision
upstream_path
upstream_blob_sha
import_disposition
wepld_path
wepld_blob_sha
renamed_or_modified
license
modification_notice_status
```

Expected destination families after explicit source-import policy activation:

```text
vendor/pictorial/**
vendor/agile/**
legal/third-party/PICTORIAL_*
legal/third-party/AGILE_*
```

No raw upstream project-name directory is allowed in the user-facing component layout.

## Import and qualification sequence

1. Freeze exact upstream commits, trees, licenses, and source inventory.
2. Import every tracked file through a deterministic path/name/content transformation into `vendor/pictorial/**` and `vendor/agile/**`.
3. Generate complete upstream-to-WePLD source maps.
4. Preserve required licenses/attribution and record modifications.
5. Disable imported CI/release/hooks/telemetry/network/install execution by default.
6. Inventory dependencies, lockfiles, package-manager surfaces, executables, scripts, model/provider calls, browser behavior, and remote egress.
7. Generate SBOMs and run repository-policy security/supply-chain qualification before runtime admission.
8. Add WePLD-owned Mirefa adapters and Nawat effect gates.
9. Run donor parity tests and WePLD-specific authority/security negative tests.
10. Run a product-surface branding gate proving users see only Pictorial and Agile.
11. Independently review the exact candidate head.
12. Merge only after all material findings are reconciled and the final base/head/blob/diff race is clean.

## Branding gate

Outside dedicated legal/provenance records and legally required preserved notices, the final product candidate must fail if user-visible strings or product-facing paths contain upstream branding.

At minimum inspect for:

```text
(?i)\bimpeccable\b
(?i)\bspec[-_ ]?kit\b
(?i)\bspeckit\b
(?i)\bspecify-cli\b
```

Pictorial and Agile names must be used consistently in UX, CLI, help, errors, templates, generated project content, docs, settings, and capability discovery.

## Current boundary

This commit establishes the exact full-import/rebrand contract and provenance pins. It does **not** itself import or execute the large donor trees, install dependencies, run donor hooks/workflows, call model providers, or grant runtime authority.

```text
FULL_IMPORT_DECISION = AUTHORIZED
SOURCE_BYTES_IMPORTED = NO
DEPENDENCIES_INSTALLED = NO
DONOR_WORKFLOWS_EXECUTED = NO
MODEL_PROVIDER_EXECUTION = NO
RUNTIME_ADMISSION = NO
USER_FACING_NAMES = PICTORIAL_AND_AGILE_ONLY
```
