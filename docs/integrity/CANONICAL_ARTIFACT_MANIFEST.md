# WePLD Canonical Artifact Integrity Manifest

**Manifest scope:** fresh-reconstitution canonical planning/source artifacts.  
**Repository:** `TheHalfMoon/wepld`  
**Date:** 2026-08-14

This manifest is verification evidence. It does not grant implementation, source admission, dependency admission, or completion authority.

## 1. Master Architecture & Execution Plan V2.2

```text
CANONICAL_SHA256 = e269b10ef711731c4ad3af7b1135546f92d82a78975cabc9ff52c2dea4b5bf44
SHARD_COUNT = 18
RECONSTRUCTION = concatenate PART-01.md ... PART-18.md in byte order
```

| Part | SHA-256 |
|---|---|
| `PART-01.md` | `08277c75727135dae71687e679b24ebecf6bbbfeb47090f0946d228a186c7848` |
| `PART-02.md` | `351de5a9a34bf8d96f8352635a5807f11e84c88dae152cb2ed148b26783d6e57` |
| `PART-03.md` | `be65ab30363c64344e920f73a95c311c2d65ad0bd5293388e900eeb91fcf77d9` |
| `PART-04.md` | `d6c86d86bb6ec260ebd51f3b12872640403e5c8244a79f28fc8d1bf70296f5ed` |
| `PART-05.md` | `628fb5c493dc40c5cbea9958892cd264d37d58f8acd48dc64f026e6008cf5e57` |
| `PART-06.md` | `ff9d3eb15a67585f0bbb85dd8c276d600f5d28a9f2410fe83ce9957c7849c60e` |
| `PART-07.md` | `1584b49158e6c95571e35021c5f23feeceb0fea1162ea46fd1358e2e03e19c7f` |
| `PART-08.md` | `11854690de82fe9d816f2e593eaac8796b081ac5ce65a9391582644e685f9c46` |
| `PART-09.md` | `1f8fb50c170ac998d62f6b48655b9c81a2f6112500607494c8b35d54376b00e0` |
| `PART-10.md` | `1b6a1fe3e82c89e5186f3b2dad632011c0a7c8a0c6eb49b67ee50001d173afb3` |
| `PART-11.md` | `8dfc915ba08be033d4841061b8319318d9b807a7c2596ed29dfc149059a34ac0` |
| `PART-12.md` | `885bfb0ea9813bf7157cd27b7294526afb3f8b256478eb99819e2fee109702a9` |
| `PART-13.md` | `2829e1681b683d05e73498b45f15630a8991c83c84dc45238622226f427c5a9e` |
| `PART-14.md` | `4227f0d807e3a737ce1e73eab302e121ffe2920d85837b2aae0bfb8a7e2409c2` |
| `PART-15.md` | `cebfade9d10ff0e3776f45c71d10b66e0e5ee37cef5b42972c909c87d22d3ec6` |
| `PART-16.md` | `98eec7cbce9a0f2b937fffd1d4798bed0e66d53923cb70d1f1735841bdd403e2` |
| `PART-17.md` | `35a732fd439ea4f13537ce763c97db20445d6ab01aa65ac49e8d7e6ce5e31c81` |
| `PART-18.md` | `4b669a595fba426f6b2f38fa86e844b9e52775c22e60cda04358e80a2e75c57d` |

The shard text is immutable issuance evidence. Current ratification/repository/blocker state is controlled by `docs/canonical/CURRENT_STATE.md` and `docs/canonical/FOUNDER_RATIFICATION.md`.

## 2. Master Source Registry V1

```text
CANONICAL_MARKDOWN_SHA256 = d0880e346dea6899375f9683ac1141a819dbcb3fc154f2905966e4022f62598b
SHARD_COUNT = 7
NAMED_SOURCE_ENTRIES = 402
EXPECTED_ID_RANGE = SRC-0001..SRC-0402
ADMISSION_STATE = ALL NOT_ADMITTED
RECONSTRUCTION = concatenate PART-01.md ... PART-07.md in byte order
```

| Part | SHA-256 |
|---|---|
| `PART-01.md` | `203b65ece814d0799e3f2c460acd1216b76097d3650bdb49cf134fca10055a33` |
| `PART-02.md` | `c8e908f724858c938a35214b4f85caaf5498e18fd12ce35fee0f2aa03ae0cf07` |
| `PART-03.md` | `687f6de9b4d74ed9c2f712e8a948140c801dce2595fec49e33e372ed729b29b8` |
| `PART-04.md` | `bebd4983934b3303384f8fc1196942ee8223161b895c8d26292a81a653be5052` |
| `PART-05.md` | `b96f5bb080429994e91bcc6f6110968784b92f10be69e231b646357a88519762` |
| `PART-06.md` | `558ac47c355cd8c4865e058eacdd97a6e8a65c0bc53b73283eb4ac06c8ab9e3f` |
| `PART-07.md` | `fb08a210d421f5ecf297a76c9b49f6b7762472f278721cf05bd1d76f35d24576` |

## 3. Foundation invariants checked by review

```text
IMPLEMENTATION_SOURCE = NONE
IMPLEMENTATION_DEPENDENCIES_ADMITTED = 0
SOURCE_ADMISSION = NONE
S1_IMPLEMENTATION_AUTHORIZATION = NONE
SPEC_KIT_BUILD_METHOD = REQUIRED
PONYTAIL_MODE = FULL
ReviewOutcome != CompletionDecision
```

## 4. Validation rule

A mismatch in any shard hash or reconstructed canonical hash is a blocking integrity defect. Do not update this manifest merely to bless changed bytes. Either restore the intended canonical bytes or create an explicitly versioned successor artifact with new provenance and authorization.
