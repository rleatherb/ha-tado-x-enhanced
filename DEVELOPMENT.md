> **Development history:** DEV-001 through DEV-005 records below preserve intermediate decisions, superseded designs and testing status as recorded at the time. Earlier references to unpublished builds, release candidates or pending testing are historical and do not describe the published v1.3.0 release. Refer to the release records and `CHANGELOG.md` for final published behaviour and validation evidence.

# Tado X Enhanced — Development Status

**Repository:** https://github.com/rleatherb/ha-tado-x-enhanced  
**Integration domain:** `tado_x`  
**Current published release:** `v1.3.0` (10 November 2026)  
**Release tag:** `v1.3.0` (commit `d12fe8ef55b899af5169dbde3354a47a60807bac`)  
**Stable branch:** `main`  
**Development branch:** `develop`  
**Development baseline:** Both branches synchronised at the v1.3.0 release commit before this housekeeping update  
**Current development cycle:** DEV-006 (scoping and prioritisation)  
**Next release:** Not yet agreed; no version number or release date assigned  
**DEV-003 integration:** PR #9, commit `1ad377480c674e718f413d29bdc6416d63ae7f78`  
**Updated:** 10 November 2026

## Current development position

Version `v1.3.0` was published on 10 November 2026 following DEV-005. It adds five whole-home actions, the home-level Schedule profile status sensor, 0.1 °C temperature selectors for the affected actions, the corrected default for automatic Holiday Mode polling, and revised installation and migration guidance. The release registers 25 `tado_x` actions. Existing multi-home support, schedule profiles and Home/Away settings, extended climate timers, domestic hot water, Holiday Mode, historic data, authentication reliability, polling options and API monitoring remain part of the published baseline.

The published `v1.3.0` tag, `main` and `develop` were verified at the same commit (`d12fe8ef55b899af5169dbde3354a47a60807bac`) before this documentation-only housekeeping change. The release tag and `main` must remain unchanged. New development documentation and any subsequently approved work are to be committed to `develop` without retroactively modifying the release.

The maintainer reported successful Home Assistant functional checks of the v1.3.0 whole-home actions, profile-status sensor and temperature selectors. Two replacement trials in a disposable Home Assistant 2026.11 VirtualBox environment retained the specifically checked device and renamed entity IDs, but required reconfiguration and reauthorisation. That result is not a guarantee of identity preservation elsewhere. The updated Holiday Mode polling default has static regression coverage but no separately reported live verification. Flow Temperature could not be tested on the available homes; dynamic addition of rooms and every upgrade path were not live-tested. Refer to `CHANGELOG.md` for release-specific validation and limitations.

DEV-006 starts with identifying, investigating and prioritising proposed maintenance and enhancement work packages. No functional change is authorised by this initial housekeeping, and no subsequent version or release date has been selected. Significant architectural changes require design discussion before implementation.

## v1.3.0 release record

Published 10 November 2026 after DEV-005 and its documentation/release-readiness review. The release includes five home-wide actions, the Schedule profile status sensor, updated temperature selectors, Holiday Mode polling-default handling and the Marketplace/HACS installation guide. The release tag is immutable for this development cycle. Consult `CHANGELOG.md` for the published feature inventory and the precise scope of reported tests.

## DEV-006 — Post-v1.3.0 maintenance and enhancement planning (10 November 2026)

- Baseline: published v1.3.0 source and documentation, with the `main`, `develop` and release tag verified as synchronised before housekeeping.
- Initial task: update only the current development status and establish DEV-006 while retaining DEV-001 through DEV-005 history as an audit trail.
- Next task: collect, investigate and prioritise candidate work packages before functional editing.
- No version bump, release date, release-candidate package, Home Assistant functional test or Tado API test is implied by this record.

## DEV-006.1 — OpenTherm domestic hot-water setpoint (design review, 11 November 2026)

Source contribution: PR #13 by @gmagniez (https://github.com/rleatherb/ha-tado-x-enhanced/pull/13), addressing issue #14. The contributor reports a successful live read of a 50 °C setpoint and write to 51 °C on an OpenTherm-connected TR04, confirmed in the Tado app. This is contributor-reported evidence, not maintainer verification.

**Decision:** Accept the feature in principle, but do not merge the PR unchanged. It currently targets `main`, is reported by GitHub as conflicting, and was authored against an earlier baseline. Reconcile changes against the latest `develop` source and preserve v1.3.0 functionality.

**Implementation design:**
- Add a home-scoped Hot Water Temperature number entity only where the existing DHW state response exposes a valid setpoint and numeric, ordered constraints. Use the existing home-scoped Hops API client and `manualControl` POST; avoid extra periodic requests. Refresh after a successful write.
- Preserve existing entity unique IDs, configuration entries and the Hot Water feature flag. New entity identity: `{home_id}_dhw_setpoint`. Capability and state must remain isolated per home.
- Recognise `MANUAL_ON` and `MANUAL_OFF` as raw Hot Water State sensor values. Do not map them to Schedule, Boost or Off without validated semantics. For installations where relay mode control is unsupported, the mode selector must not imply it is usable.
- Preserve relay-based Boost, Off, Resume Schedule and Hot Water Mode functionality on non-OpenTherm homes. An OpenTherm interface alone does not prove relay controls are unavailable. On setpoint-capable OpenTherm homes, default-disable unverified relay controls for newly registered entities, while respecting existing registrations and explicit user choices. Keep capability handling separate from Hot Water feature-flag reconciliation.
- Validate finite numeric setpoint/limits, ordered bounds and accepted increments; handle missing or malformed API fields, write failures and read-back cleanly. Document setup-time capability discovery and reload requirements if a setpoint appears later.
- Update relevant translations, entity documentation and changelog in the development baseline; no release version or date is assigned.

**Validation plan:** Static/mocked checks for both home types, mixed-capability multi-home accounts, entity registry states, feature toggles, API errors and quotas. Maintainer to perform live regression on two non-OpenTherm homes, especially existing DHW controls and automations. Request contributor to verify the corrected development build on OpenTherm hardware, including setpoint read/write, reload and default-disabled controls. Do not claim live OpenTherm validation of the revised build until reported.

No functional code has been changed or approved for release by this design record.

## v1.2.0 release record

Published 9 November 2026 after completion of DEV-004. The release includes 20 registered actions, coordinator-driven supplementary Holiday Mode polling (rather than an independent Holiday Mode periodic timer), the 5× default multiplier, and observed and theoretical daily API usage estimates. The published v1.2.0 tag must remain unchanged. Refer to `CHANGELOG.md` for the public release record and its validation limitations.

## DEV-005 — Documentation reconciliation (9 November 2026)

The v1.2.0 source was reviewed before editing. This documentation-only package corrects the current development status in this file, the registered action count and `set_polling_options` inventory in `docs/ARCHITECTURE.md`, and outdated Holiday Mode polling descriptions in `docs/ENTITIES.md`, `README.md` and the architecture lifecycle section. The architecture diagram also identifies the Holiday Mode manager and its coordinator-driven polling/boundary callbacks. Public documentation was reviewed for contradictory descriptions. No integration code, manifest, translations, action schemas, API requests, entity identities or stored settings were changed. Static validation results are reported with the accompanying DEV-005 package; no additional live Home Assistant test is claimed.

## Next-cycle verification priorities

1. Establish future changes against the latest accepted `develop` baseline and complete source package.
2. Verify both configured homes, entity identities, device associations and existing automations when changes could affect them.
3. Regression-test schedule profiles, extended climate timer, hot-water selection, Holiday Mode, historical data, API monitoring and setup/unload as appropriate to the change.
4. Check translations, Home Assistant action selectors and labels after user-facing changes.
5. Measure or assess additional Tado API calls before introducing new polling or verification requests.

These are ongoing development verification priorities, not claims that all scenarios were tested for `v1.3.0`.

## Development rules

1. Preserve the integration domain `tado_x`, existing config entries, entity identities, action interfaces and supported behaviour unless a change is explicitly agreed.
2. Keep all state and operations scoped to the correct Tado home, including where room IDs overlap.
3. Preserve schedule profiles, Home/Away settings, climate timers, hot water, historical data and API monitoring.
4. Avoid unnecessary Tado API calls; consider both main and schedule polling and account quotas.
5. Discuss architectural implications before implementation. Make minimal, focused changes.
6. Update `services.yaml`, `strings.json`, relevant `translations/*.json`, documentation and `CHANGELOG.md` when behaviour changes.
7. Validate Python syntax, JSON/YAML parsing, package layout, ZIP integrity and internal consistency. Record live Home Assistant/Tado API tests separately; static validation is not runtime verification.
8. Do not bump the version or publish a release without explicit approval.

## Working procedure

1. Start from the latest complete integration source and check its relationship to the `develop` branch.
2. Investigate an issue, agree the design and record decisions in this file.
3. Implement minimal changes and produce complete replacement files or an updated complete development ZIP.
4. Perform and report static validation, then install and test in Home Assistant as appropriate.
5. Record test results, unresolved problems and any follow-up corrections.
6. Commit accepted changes to `develop`, with descriptive commit messages.
7. Replace the Project's development ZIP and update this file and relevant individual documentation Sources to match the accepted baseline.
8. When release scope and testing are agreed, prepare release notes, agree a semantic version, merge to `main`, tag and publish. Do not do this automatically.

## Previous investigations

DEV-001 introduced Holiday Mode entities and state management in `v1.1.0`; DEV-002 corrected date updates in `v1.1.1`. The Stage C–G diagnostic builds and associated Home Assistant logs are historical evidence rather than release-facing changelog entries. The `CHANGELOG.md` records published changes and their stated validation scope.

## DEV-003 — Authentication reliability (v1.1.2)

A consolidated implementation based on community PRs #5 (rotating refresh-token race), #6 (Home Assistant SSL context and authorisation-code logging) and #7 (transient refresh failures). Contributions by @cmatte are acknowledged in PR #9 and the v1.1.2 changelog. DEV-003 was incorporated into v1.1.2 following PR #9.

- `api.py`: per-client refresh lock covers explicit, expiry-triggered and HTTP-401-triggered refreshes; a 401 retries once using the current token, avoiding duplicate rotations. Refresh errors distinguish known rejected credentials from transient network/server conditions. The existing token persistence callback remains in place. Device authorisation uses Home Assistant's SSL context and no longer logs the user code.
- `__init__.py`: setup refreshes only when the access token is missing or close to expiry; initial coordinator update still checks connectivity. Transient refresh errors become `ConfigEntryNotReady` rather than reauthentication requests.
- No config-entry, entity-ID, unique-ID, integration-domain, schedule, hot-water, Holiday Mode or action-interface changes. Per-home API instances and credentials remain independent. Same-account multi-home refresh-token behaviour remains unverified.
- Logging enhancement: debug-only success entries identify `home_id`, refresh `reason` (`expiry`, `missing_token`, `http_401`, or `explicit`) and `expires_in`; token persistence logs identify `home_id`. No credentials or device codes are logged. The home ID is assigned before startup refresh.
- Maintainer confirmed live token refresh and persistence for both homes with the enhanced logging build on 2026-11-07: home_id=2243481 at 22:53:37 UTC and home_id=1985739 at 22:54:08 UTC, both reason=expiry and expires_in=599s. Normal operation was also reported. Live error-path recovery, revoked-token handling and same-account multi-home behaviour remain unverified.
- `tests/test_dev003.py`: standalone mocked tests; no Home Assistant or live Tado API exercised. Run `python tests/test_dev003.py` from the package root.

Validation scope: standalone mocked tests covered concurrent refresh and HTTP 401 recovery. The maintainer confirmed routine live refresh and persistence for both homes. Live revoked-token handling, transient failure recovery, reauthentication, and same-account multi-home behaviour were not verified. These are known limits of the evidence, not claims of successful live testing.

Community contribution: DEV-003 draws on PR #5 (serialised refresh), PR #6 (SSL context and authorisation-code logging) and PR #7 (transient refresh failures), submitted by @cmatte. This work is acknowledged in PR #9 and the changelog; the consolidated implementation contains additional changes and should not be described as a direct merge of those PRs.

## v1.1.2 release record

Version 1.1.2 contains DEV-003 authentication reliability improvements. The release retains the existing integration domain, configuration-entry model, entities, actions, schedule profiles, climate timers, hot-water controls, Holiday Mode, historical data and API monitoring.

Validation evidence includes static checks, standalone mocked authentication tests and the maintainer's successful live refresh/persistence observations for both independently authenticated homes. A complete Home Assistant regression run and live authentication-failure injection were not reported. Future maintenance should verify those scenarios when practical without exposing credentials or generating unnecessary API traffic.

## DEV-004 — API polling and configuration (unreleased development build)

- DEV-004.1: Schedule and Holiday Mode polling share the existing check interval, with independent enable/disable checkboxes. Holiday polling defaults to enabled for existing entries and supports live interval reconfiguration. Initial read, manual refresh, boundary events and action-triggered refresh are preserved.
- DEV-004.2: Correct the coordinator per-update API accounting to include optional flow-temperature requests.
- DEV-004.3: Explain three mandatory main-update requests, per-feature costs and theoretical scheduled daily usage; distinguish these from server-reported API usage. Detailed investigation of the historical predicted/observed discrepancy is deferred.
- DEV-004.4: Optional reduced supplementary polling for weather, air comfort and running times, approximately every five main intervals. Off by default. Retain cached values between updates; discard running-time values from prior dates. Debug-only coordinator logs mark each actual supplementary API request (weather, air comfort, running times) with its home ID for live polling-cadence verification, without adding API calls.

No release version change, GitHub commit or live Home Assistant/Tado API testing is implied by this development record.

### DEV-004 Check 3 — polling diagnostics (unreleased)

- Debug-only schedule and Holiday Mode polling configuration messages show enabled state, interval and home ID, including on live options changes.
- Separate scheduled callbacks log `Schedule polling started` and `Holiday Mode polling started` only for periodic checks. Initial/manual schedule comparisons, Holiday Mode manual refreshes and Holiday Mode boundary-triggered refreshes do not emit these periodic markers.
- No additional API requests or entity/configuration interface changes. These markers report the start of a check, not successful API completion.
- Live verification of all four checkbox combinations remains pending.

### DEV-004 consolidated design update (unreleased)

- The supplementary reduction checkbox is replaced with a per-home selector of 1×, 2×, 5× or 10× (default 1×). No migration code is introduced for unpublished DEV-004 builds.
- Supplementary features: Weather, Air Comfort, Heating Running Times, Flow Temperature and Holiday Mode. Mobile Devices and Hot Water remain on the main cadence; schedule checking remains independent. Holiday Mode no longer has a periodic timer separate from the coordinator.
- Flow-temperature control actions invalidate the cached dataset before requesting a coordinator refresh. Holiday Mode initial/manual/boundary refreshes remain independent of periodic checks.
- DEV-004.5: `tado_x.set_polling_options` action, using the standard optional Home device selector, with partial updates, shared live options logic, persistence and validation.
- Earlier Check 3 Holiday Mode cadence results apply to the superseded shared-interval design and must be repeated for the new coordinator-driven polling.
- No actual Home Assistant runtime testing of this consolidated design is claimed.

### DEV-004 options UI correction (unpublished)

- Main polling, Supplementary polling and Schedule checking are now native Home Assistant sections on one options page.
- Supplementary multiplier is an explicit 1×/2×/5×/10× dropdown with 1× preselected for entries without a stored multiplier; existing selected values are retained.
- Section form submissions are flattened before applying the existing shared polling configuration logic; stored entry keys and action parameters remain unchanged. No migration code is included.
- Home Assistant frontend rendering and live persistence require user verification; static validation does not constitute a live HA test.

- DEV-004 action UI correction: `set_polling_options` now shares the existing home-device resolution convention, requiring a Tado X Home device only for multi-home installations; the unpublished numeric `home_id` argument was removed.

### DEV-004 Check 7 diagnostic logging (unpublished)

Added source-labelled debug logs around Holiday Mode API reads (initial, periodic, button, action and boundary), including success and failure. The manual refresh button continues to bypass the supplementary polling cadence. No polling frequency, action interface or API request count is intentionally changed. This is static validation only; repeat Check 7A in Home Assistant.

### DEV-004 default supplementary multiplier decision (unpublished)

- Adopt **5×** as the supplementary polling default for new installations and upgrades from published releases without this option. At 30-second main polling, supplementary datasets are normally checked approximately every 150 seconds.
- Preserve an explicitly stored multiplier, including 1×. No migration is required: absent values resolve to 5× in runtime and options, and the options form saves 5× when submitted.
- Keep earlier DEV-004 notes describing the original 1× development default as historical context; the final intended default is now 5×.
- This change does not affect the main polling interval, schedule checking interval, or immediate Holiday Mode reads. Home Assistant live testing of the new default remains pending.

### DEV-004 Check 8C and regression review (unpublished)

- Maintainer confirmed in Home Assistant that the 5× default is described in options and that existing explicit multipliers (1× for home 2243481 and 5× for home 1985739) were preserved after installing the default-5× build and restarting.
- API monitoring source review: current usage uses the server-reported quota/remaining headers when available; estimated daily usage extrapolates observed consumption since the quota reset to a 24-hour rate. Neither sensor directly computes a forecast from the configured supplementary multiplier.
- Corrected the source-level `tests/test_dev004.py` translation assertion to inspect the new three-section options schema. This fixes an obsolete test assumption, not a runtime issue. Standalone DEV-003, DEV-004, DEV-004.5 and default-5× checks pass. No new Home Assistant test is implied.

### DEV-004 — Rolling API usage estimate (unpublished)

- Replaced since-quota-reset daily extrapolation with a rolling 60-minute projection, based on existing API rate-limit response headers. No extra requests.
- A minimum 10-minute observation period provides a provisional estimate; full-window stabilization takes 60 minutes. History is per API client/home, bounded, in memory only, and cleared on quota changes or counter decreases.
- Existing API estimated daily usage sensor identity retained; current usage and remaining quota sensors unchanged. Live HA testing pending.

### DEV-004 — complementary theoretical API usage projection (unpublished)

Added the **API theoretical daily usage** sensor, preserving existing API sensor identities. The new home-scoped diagnostic projects the current periodic API workload immediately from the applied coordinator settings, supplementary multiplier, enabled features, independent schedule interval and discovered room count. Attributes separate main, supplementary and schedule contributions. The existing 60-minute observed estimate is unchanged except that its freshness tolerance now follows slower main polling. Live option changes notify sensors without issuing a Tado API refresh. No migration or new API requests. Requires Home Assistant verification; theoretical model excludes manual actions, retries, startup and API-specific variation.

### DEV-004 — Configuration wording refinement (9 November 2026)

Updated the Configure dialogue introduction to recommend quota-conscious starting settings for both subscription tiers, clarified that Auto-Assist does not automatically change a configured polling interval, standardised “API request” terminology, and shortened Weather, Air Comfort and Heating Running Times descriptions. Updated all five shipped translations and `docs/CONFIGURATION.md`. No polling logic or entity identities changed.

### DEV-004 — Final Configure dialogue wording (9 November 2026)

- Corrected quota warning Markdown so the full phrase “Keep actual usage below 100%” is bold. Home Assistant frontend rendering still requires visual verification.
- Clarified that larger supplementary multipliers reduce polling frequency and API requests; removed the multiplier default from the Configure description without changing the actual 5× default.
- Simplified Flow Temperature description and removed upgrade/default wording from schedule checking description.
- Aligned `strings.json` and the five shipped translation files with the agreed options text. No functional code, entity identities, polling behaviour or API request counts changed.

## DEV-005 — Whole-home actions (development, not released)

Implemented `set_climate_timer_home`, `set_away_schedule_home`, `save_schedule_profile_home`, and `restore_schedule_profile_home` with home-device resolution, preflight profile-name validation, sequential room processing, aggregated failure reporting, and a startup-room/Normal-profile eligibility guard. Per-room restore retains its rollback logic; bulk restores use one final coordinator refresh. Dynamic room addition is explicitly out of scope. Live Home Assistant/Tado testing remains outstanding.

### DEV-005 Fix 2 — whole-home enhancements (2026-11-10)

Following live maintainer testing of the four whole-home actions (successful startup, save/restore profiles, invalid-name rejection, timer modes and Away settings), added `set_hvac_mode_home` (`auto`, `heat`, `off`), a home-level Schedule profile status sensor (`Custom` takes precedence over `Mixed`), and corrected all four action temperature selectors to 0.1 °C increments, with 5–30 °C Away UI sliders. The backend Away validation remains unchanged. Reviewed bulk restore: room-level schedule and Away requests are sequential and the batch already requests one coordinator refresh; no speculative parallelisation was introduced. Fix 2 requires live Home Assistant validation.

### DEV-005 post-test and Marketplace migration review (10 November 2026)

- Maintainer reported all DEV-005 Fix 2 Home Assistant functional tests passed. This does not include a real new-room addition (explicitly out of scope).
- Home Assistant 2026.11 Marketplace migration from original Exabird Tado X to Enhanced was repeated twice in a disposable VirtualBox installation. The original integration was explicitly deleted through two destructive warnings; Enhanced required new setup and Tado authorisation. Four checked device IDs and five deliberately renamed entity IDs were retained in those tests. This is not a general preservation guarantee.
- Added `docs/INSTALLATION.md` with separate Marketplace/HACS fresh and replacement instructions, strongly emphasised backup and recovery requirements, and a conservative account of the observed migration results.
- Corrected absent-value Holiday Mode periodic polling defaults to follow Auto-Assist (enabled with subscription, disabled without); explicitly stored values remain unchanged. The initial/manual/action/boundary reads remain unaffected.
- Documented initial Custom profile status when automatic schedule checking is off. No automatic API requests were added.
- These changes are development-stage pending static checks and maintainer confirmation; they are not yet a publication-ready v1.3.0 candidate.

## v1.3.0 publication-readiness review (10 November 2026)

Prepared a publication-ready candidate from the DEV-005 Marketplace Review development package. Version metadata and public documentation were reconciled with the 25 registered actions, the home profile status sensor, 0.1 °C selectors, the Holiday Mode polling default and the tested Marketplace migration procedure. Public DEV/Fix labels were removed; historical development notes above remain as an audit trail. The API Reset Time timestamp sensor remains unchanged by decision. Candidate status and any outstanding approval or live verification are recorded here rather than in public-facing release documentation.

