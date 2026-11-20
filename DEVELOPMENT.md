# Tado X Enhanced — Development and Release Record

**Repository:** https://github.com/rleatherb/ha-tado-x-enhanced  
**Integration domain:** `tado_x`  
**Version described by this package:** `1.4.0`  
**Stable branch:** `main`  
**Development branch:** `develop`  
**Updated:** 20 November 2026

## v1.4.0 release record

The DEV-006 cycle is complete for feature development. Version 1.4.0 consolidates OpenTherm domestic hot-water setpoint support, depleted battery handling, room and home schedule controls, heating duration sensors and historical actions, coordinator health and refresh reliability, and physical-device identification. There are 31 registered actions. The integration domain, existing action interfaces and home-scoped storage are retained.

| Work package | Acceptance and validation |
|---|---|
| DEV-006.1 | OpenTherm setpoint operation reported working externally; latest default relay-control disablement not confirmed on OpenTherm hardware. Accepted with qualification. |
| DEV-006.2 | Depleted battery interpretation and translation coverage checked in standalone tests; physical exhaustion not live-tested. Accepted with qualification. |
| DEV-006.3 | Room and home schedule controls validated live. |
| DEV-006.4 | Heating duration sensors, room IDs and historical actions validated live. |
| DEV-006.5A | Eight live checks passed. |
| DEV-006.5B | Nine applicable live checks passed; mobile-device monitoring not used or live-tested. |
| DEV-006.5C | Eleven live checks passed. |
| DEV-006.6 | Blink Display validated on VA04 and SU04 devices. |
| Consolidation | All ten live checks passed on the maintainer's non-OpenTherm homes; 14 standalone regression scripts previously reported passing. |

The exceptional API failure paths have simulated rather than deliberately induced live coverage. The root cause of issue #16 remains unconfirmed. Battery exhaustion testing is disproportionate to the narrow change; unsupported OpenTherm relay-control calls may still produce API errors if controls remain enabled. These limitations were explicitly accepted by the maintainer. See CHANGELOG.md for public release details and contributor credits.

The last confirmed published baseline during this development cycle was v1.3.0 (10 November 2026), commit `d12fe8ef55b899af5169dbde3354a47a60807bac`. This record does not assert that a v1.4.0 tag has been created. Publication requires approval and validation of the exact final package. Changes after approval require renewed validation. Preserve previous release tags.

## Historical development records

The following records preserve decisions and evidence as recorded at the time, including superseded designs and interim testing status. They are not descriptions of outstanding work in v1.4.0.

## v1.3.0 release record

Published 10 November 2026 after DEV-005 and its documentation/release-readiness review. The release includes five home-wide actions, the Schedule profile status sensor, updated temperature selectors, Holiday Mode polling-default handling and the Marketplace/HACS installation guide. The release tag is immutable for this development cycle. Consult `CHANGELOG.md` for the published feature inventory and the precise scope of reported tests.

## DEV-006 — Post-v1.3.0 maintenance and enhancement planning (10 November 2026)

- Baseline: published v1.3.0 source and documentation, with the `main`, `develop` and release tag verified as synchronised before housekeeping.
- Initial task: update only the current development status and establish DEV-006 while retaining DEV-001 through DEV-005 history as an audit trail.
- Next task: collect, investigate and prioritise candidate work packages before functional editing.
- No version bump, release date, release-candidate package, Home Assistant functional test or Tado API test is implied by this record.

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

These are ongoing development verification priorities, not claims that all scenarios were tested for `v1.4.0`.

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



### DEV-006.3 validation iteration 4 (local test package)

- Established descriptive unique IDs for the three newly introduced home-device schedule controls, to generate distinct entity IDs on fresh registration. Existing room entities and all service action names are unchanged.
- Clarified that saving profiles already reads fresh Home and Away data per room, with no prerequisite refresh.
- Device-registry correction from iteration 3 retained. Home Assistant runtime verification pending.

## DEV-006.4 — Temporary Minder response diagnostic (19 November 2026)

- Test-only `tado_x.inspect_running_times` action returns the raw Minder response for a selected Tado X Home and optional inclusive date range (defaults to today; maximum 31 days). One explicit read-only API request per invocation; no new background polling or persistent data. A Home device must be selected when multiple homes are configured.
- This diagnostic exists solely to verify the actual home-level Minder summary structure and support retrospective comparisons before implementing the home Heating Time Today sensor.
- **Remove the action, schema, handler and `services.yaml` entry before a public release.** The current ZIP is for live diagnostic testing only. No heating sensor behaviour has been changed yet.

## DEV-006.4 — Heating durations validation package (19 November 2026)

- Two-decimal existing room duration, new home duration from Minder summary, new room-ID diagnostic sensor, and three read-only response actions implemented for Home Assistant validation. The temporary `inspect_running_times` action is replaced by `get_running_times`.
- The maintainer's real Minder response for home 2243481 (2026-11-19) confirmed `summary.totalRunningTimeInSeconds` and matching daily home `runningTimeInSeconds`. Retrospective queries have been observed to exceed the final daily maximum in Home Assistant history. No automated Yesterday sensor or additional routine polling is added.
- Validation so far: static Python/JSON/YAML and ZIP checks only. Live Home Assistant testing of the new actions, entities, date-range response shape, and multi-home behaviour remains outstanding.

### DEV-006.4 validation iteration 2 — response simplification (19 November 2026)

- Maintainer confirmed existing room sensor precision, home sensor, room-ID diagnostic sensor, all three actions, single-room comparisons, and both-home isolation in Home Assistant.
- Simplified all three action responses to seconds only; removed rounded `running_time_hours`.
- Detailed `get_running_times` now returns the original Minder structure, adding `name` to known zones only, without duplicating processed and raw data.
- No changes to polling, sensors, or API request counts. Runtime testing of iteration 2 remains outstanding.


### DEV-006.6 experimental identification validation package (19 November 2026)

- Added an experimental `tado_x.identify_device` response action to the DEV-006.4 validated baseline. It selects an existing Tado X physical-device entity, validates home ownership and model (VA04/RU04/IB02), and issues one GraphQL identify mutation. It returns success status but hardware blinking must be confirmed independently.
- No physical-device buttons are included yet; the API endpoint and mutation remain unverified on actual Tado X hardware. No automatic identification or extra background polling.
- If the experiment fails, remove the action and API method before publication. If successful, retain the action and implement buttons only for confirmed device types.

### DEV-006.6 device selector correction

The experimental identify_device action now selects a physical device_id instead of an entity_id. The device registry identifier is matched against the owning home coordinator’s serial-number dictionary; room and Home devices are rejected. No API or polling changes.

### DEV-006.6 — Final metadata investigation (temporary test build)
- VA04 and IB02 identify requests returned `NOT_FOUND` in live tests.
- Temporary `inspect_device_metadata` action performs one read-only `roomsAndDevices` request and returns field names/types for a selected physical device; no serials, identifiers, or credentials.
- Remove diagnostic action before publication. No additional background polling.

### DEV-006.6 — Metadata follow-up (19 November 2026)

- Live VA04 and IB02 metadata revealed a boolean `supportsIdentify` field; previous diagnostic returned only field types.
- This test iteration returns the actual `supports_identify` boolean (or null if missing/invalid) without exposing serial numbers or credentials.
- Added `SU04` (Temperature Sensor X, used as a wireless room temperature sensor/thermostat) to the **experimental** `identify_device` device-type allowlist, alongside VA04, RU04 and IB02. This is not evidence that the GraphQL identification request works for SU04.
- No new automatic polling. `inspect_device_metadata` remains a read-only, on-demand API request. No permanent Blink Display buttons have been added.

### DEV-006.6 — HOPS identification experiment (19 November 2026)

- Experimental `tado_x.identify_device` checks the selected physical device's live `supportsIdentify` field and, only if true, sends a single `POST` to candidate HOPS path `/homes/{home_id}/roomsAndDevices/devices/{serial}/identify`.
- **Endpoint is inferred, not verified.** Test with one VA04 first; HTTP success also requires physical confirmation.
- Previous GraphQL experiment returned `NOT_FOUND` for VA04 and IB02; no GraphQL fallback.
- On-demand action performs one read-only metadata GET and one POST; no scheduled requests, button entities, or device setting changes. Shared transport retains its existing 401 authentication retry.

### DEV-006.6 — GraphQL LINE_X and capability-driven test

- Official Tado web application network capture established the working `identifyDevice` GraphQL mutation and `{home_id}:LINE_X:{serial}` identifier for a VA04 device. The previous `PRE_LINE_X` identifier returned `NOT_FOUND`; the experimental HOPS `/identify` endpoint returned HTTP 404.
- Restored GraphQL using `LINE_X`. Store `supportsIdentify` in `TadoXDevice` from the existing coordinator `roomsAndDevices` response for room and other devices; default false. The action uses the stored capability without additional API reads and without a device-type allowlist.
- No buttons yet. Test the existing physical-device action with a VA04 first, then other capability-advertising devices. GraphQL success and physical display response both require confirmation.

### DEV-006.6 — Permanent identification buttons (20 November 2026)

The maintainer confirmed `identify_device` returned `success: true` and the physical displays flashed for VA04 and SU04 in home 2243481 using GraphQL `LINE_X`. The permanent implementation creates physical-device **Blink Display** buttons for cached `supportsIdentify: true` devices, retains the action without experimental labelling and removes the temporary `inspect_device_metadata` action. The new buttons require live Home Assistant testing. No automatic API requests, configuration migrations, or existing entity identity changes. Earlier experimental notes remain as history.

## DEV-006.5A — Coordinator health diagnostics (20 November 2026)

Baseline: DEV-006.6 Blink Display Final Fixes; maintainer confirmed button/icon/action tests. Issue #16 root cause remains unconfirmed. Instrument actual coordinator fetches, distinguish cached rate-limit returns from fresh snapshots, record timing/counters and existing isolated optional failures, add per-home diagnostic sensor with independent 30-second local watchdog and transition logging. No additional API requests or changes to command, failure, or retry semantics. Staleness threshold is max(90 seconds, three main intervals); error categories are exception class names only. Post-command attribution and optional failure isolation are deferred to B/C. Sensor watchdog runs while entity is enabled and loaded. Live testing outstanding.

### DEV-006.5A — Live validation (20 November 2026)

Maintainer reported PASS for all eight tests: installation, entity registration on both homes, normal operation, attribute updates, polling configuration, command refreshes, diagnostic logging and independent integration reload. Exceptional conditions were not deliberately induced live.

## DEV-006.5B — Refresh reliability (20 November 2026)

Ordinary optional request or parsing failures retain cached values and permit fresh core snapshots. Existing polling cadence is unchanged; running-time cache remains same-day only. Authentication and HTTP 429 exceptions propagate from optional requests to whole-update handlers. Rate limiting returns a replacement cached snapshot without advancing fresh-success timestamps. Repeated 401 after token refresh triggers authentication failure. Mandatory API response shapes are validated. Optional warning logs report error-category transitions. No added polling or automatic reloads. Simulated regression and static checks passed; live validation outstanding. Issue #16 root cause remains unconfirmed.

### DEV-006.5B — Live validation

Maintainer reported PASS for all applicable live checks (installation, health, heating data and commands, hot water, weather, supplementary data, polling/API usage, multi-home independence). Mobile device monitoring was not used and remains unverified live.

## DEV-006.5C — Post-command refresh monitoring

Track existing post-command coordinator requests with a per-home sequence. A fetch must start after the latest request to resolve it; requests made before the same fetch are coalesced. An already-running fetch cannot resolve a later request. Record pending, success, degraded, error, rate_limited, authentication_required or cancelled; normal read-only refreshes and holiday boundary refreshes are not labelled as commands. A subsequent scheduled fetch can resolve a pending request. Refresh request exceptions are logged separately from successful writes; cancellation propagates. No added API calls. Existing dedicated schedule/holiday read-back operations are unchanged. Static and simulated attribution tests passed; live validation pending. Issue #16 root cause remains unconfirmed.

## v1.4.0 pre-release consolidation — 20 November 2026

All DEV-006 work packages accepted for intended release. OpenTherm implementation restored from DEV-006.1 Relay Validation v2; contributor @gmagniez reported setpoint discovery/read/write/app synchronisation and MANUAL_ON, with a relay resume 404. The follow-up default-disablement guard is retained and extended to options reconciliation. Existing enabled entries and user choices are preserved. Live OpenTherm retest remains outstanding. Depleted battery handling accepted on narrow scope and standalone tests; physical exhaustion not tested. DEV-006.5A: eight live checks passed; 5B: nine applicable checks passed, mobile devices not tested; 5C: eleven live checks passed. Issue #16 root cause remains unconfirmed.

Setpoint constraints now travel with cached hot-water data and writes use command refresh monitoring. Historical test fixtures and action counts updated; all standalone scripts executed successfully. The merged package requires live non-OpenTherm regression testing and the full documentation audit before release candidate preparation.

## v1.4.0 release candidate review — 20 November 2026

Maintainer reported PASS for CON.1–CON.10 (installation, non-OpenTherm compatibility, capability detection, hot water, options, health, heating controls, schedule management, other enhancements and multi-home independence). The maintainer reported successful live tests of schedule controls, heating durations, device identification, coordinator diagnostics and command refreshes, and all ten combined-system checks on two non-OpenTherm homes. OpenTherm setpoint operation was reported working by an external tester; the latest relay-control default-disablement behaviour has not been confirmed on OpenTherm hardware. Physical battery depletion and mobile device monitoring were not live-tested. Exceptional API failure conditions have simulated coverage. The root cause of [issue #16](https://github.com/rleatherb/ha-tado-x-enhanced/issues/16) remains unconfirmed.

Hot-water temperature control builds on [upstream PR #74 by lchovanec](https://github.com/exabird/ha-tado-x/pull/74), with integration testing and feedback from [@gmagniez](https://github.com/gmagniez). Depleted-battery handling addresses [upstream issue #72](https://github.com/exabird/ha-tado-x/issues/72) and [PR #87 by @Somberland](https://github.com/exabird/ha-tado-x/pull/87).

RC1 used the validated consolidation code unchanged except for the manifest version. The subsequent documentation review reorganised README, added action version history, expanded entity and diagnostic guidance, updated examples and adopted the maintainer’s revised schedule guide. This documentation-only review does not constitute new live testing.
