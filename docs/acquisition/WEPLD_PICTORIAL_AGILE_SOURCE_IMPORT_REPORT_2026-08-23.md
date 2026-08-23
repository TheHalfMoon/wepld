# WePLD Pictorial + Agile source import report

```text
BASE_MAIN=2ab2fae14bc3b3b1f1e9bc2059972456955aeff7
BRANCH=import/pictorial-agile-full-source-snapshot-2026-08-23
SOURCE_IMPORT_EXECUTION=COMPLETE
SOURCE_BYTES_IMPORTED=YES
SOURCE_ADMISSION=SOURCE_ONLY
DEPENDENCY_ADMISSION=NONE
DEPENDENCIES_INSTALLED=NO
DONOR_WORKFLOW_EXECUTION=NONE
IMPORTED_WORKFLOW_ACTIVATION=NONE
IMPORTED_HOOK_EXECUTION=NONE
IMPORTED_INSTALL_SCRIPT_EXECUTION=NONE
IMPORTED_TELEMETRY_ACTIVATION=NONE
IMPORTED_NETWORK_ACTIVATION=NONE
H0_014_PLUS=NOT_STARTED
H0_SCREEN_EXECUTION=NONE
MODEL_PROVIDER_EXECUTION=NONE
MODEL_WEIGHT_ACCESS=NONE
MODEL_INFERENCE=NONE
PR88_MINIMAX_CHAIN=SEPARATE_UNCHANGED_BY_IMPORTER
PR126_DIAGNOSTIC=LEFT_CLOSED_UNCHANGED
```

## Exact-set accounting

```json
{
  "Agile": {
    "binary_entries": 6,
    "binary_visual_branding_review_candidates": [
      "docs/images/spec-kit-logo.webp",
      "media/bootstrap-claude-code.gif",
      "media/logo_large.webp",
      "media/logo_small.webp",
      "media/spec-kit-video-header.jpg",
      "media/specify_cli.gif"
    ],
    "dispositions": {
      "imported": 545
    },
    "exact_set_equality": true,
    "excluded_gitlinks": 0,
    "git_modes": {
      "100644": 539,
      "100755": 6
    },
    "git_types": {
      "blob": 545
    },
    "inventory_sha256": "ed2f9e5e5892b980cc45a920f2c8e8f70264f603e70dbe136af0d796c722385c",
    "modified_text_entries": 416,
    "repository": "github/spec-kit",
    "revision": "27f50f7e6b618ea14d74dd4037f9e7c60218b16c",
    "root_tree": "5622442d5ff74d21b2cb4349f255d08380f3d69d",
    "source_map_records": 545,
    "tracked_non_tree_entries": 545
  },
  "Pictorial": {
    "binary_entries": 6,
    "binary_visual_branding_review_candidates": [
      "extension/icons/icon-128.png",
      "extension/icons/icon-16.png",
      "extension/icons/icon-32.png",
      "extension/icons/icon-48.png",
      "extension/icons/promo-small.png",
      "scripts/lib/assets/plugin-icon.png"
    ],
    "dispositions": {
      "imported": 3267
    },
    "exact_set_equality": true,
    "excluded_gitlinks": 0,
    "git_modes": {
      "100644": 3264,
      "100755": 3
    },
    "git_types": {
      "blob": 3267
    },
    "inventory_sha256": "1fdcb041c9883ab670a35b0f2107a6c7320ceec62b144deaca20f365e31ceb3b",
    "modified_text_entries": 2024,
    "repository": "pbakaus/impeccable",
    "revision": "56f44523f76efdcec813e67b38ee550e49b16f48",
    "root_tree": "3626999bc9c8be4d31f3028c37c74cf544576d15",
    "source_map_records": 3267,
    "tracked_non_tree_entries": 3267
  }
}
```

## Inertness

Donor workflows, hooks, install surfaces, lockfiles, release/telemetry/network material remain nested under `vendor/**` as inert source data. The importer does not execute them, install dependencies, register vendor packages in the root Cargo workspace, or add donor workflows to the WePLD root workflow surface.

## Merge readiness

`NOT_READY_FOR_MERGE`. Independent exact-head review, listed binary visual-branding review, repository policy/security qualification, and remaining canonical contract gates are still required. Dependency/runtime admission remains separately unauthorized.
