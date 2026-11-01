# Tado X Enhanced — Development Status

**Repository:** https://github.com/rleatherb/ha-tado-x-enhanced  
**Integration domain:** `tado_x`  
**Published baseline:** `v1.0.0`  
**Active development branch:** `develop`  
**Current development package:** `Tado_X_Enhanced_Development.zip` (ChatGPT Project source)  
**Status:** Unreleased development; no version change agreed  
**Last updated:** 1 November 2026

## Purpose and source of truth

This file records the current development state, outstanding work, validation and release readiness. It supplements, but does not replace, `CHANGELOG.md`, the documentation under `docs/`, or Git commit history.

- **GitHub** is authoritative for committed code. The `v1.0.0` tag is the immutable published baseline.
- **`main`** contains published code and any subsequent committed documentation updates.
- **`develop`** is the integration branch for accepted, unreleased changes.
- **`Tado_X_Enhanced_Development.zip`** is the complete working snapshot used in the ChatGPT Project, including any not-yet-committed changes. After each accepted change, replace this snapshot and ensure it agrees with the intended `develop` state.
- **`Latest complete source.zip`** is retained unchanged as the historical initial integration-only snapshot.
- Before editing, inspect the latest complete development package and relevant dependencies. Do not reconstruct the integration from isolated excerpts.

## Development rules

1. Preserve the integration domain `tado_x`, existing config entries, entity identities, action interfaces and supported behaviour unless a change is explicitly agreed.
2. Keep all state and operations scoped to the correct Tado home, including where room IDs overlap.
3. Preserve schedule profiles, Home/Away settings, climate timers, hot water, historical data and API monitoring.
4. Avoid unnecessary Tado API calls; consider both main and schedule polling and account quotas.
5. Discuss architectural implications before implementation. Make minimal, focused changes.
6. Update `services.yaml`, `strings.json`, relevant `translations/*.json`, documentation and `CHANGELOG.md` when behaviour changes.
7. Validate Python syntax, JSON/YAML parsing, package layout, ZIP integrity and internal consistency. Record live Home Assistant/Tado API tests separately; static validation is not runtime verification.
8. Do not bump the version or publish a release without explicit approval.

## Issue register

| ID | Issue | Status | Implementation | Live testing |
|---|---|---|---|---|
| DEV-001 | Holiday Mode visibility, controls, hot-water state, schedule interpretation and date entry | **Completed and accepted for development baseline** | Implemented in refined DEV-001 candidate | User-confirmed functional checks on both homes; see validation register |

### DEV-001 — Holiday Mode enhancements

**Implemented behaviour**

- Home-scoped Holiday Mode switch, Holiday Status sensor, Holiday Start and Holiday End sensors, and Refresh Holiday Mode button.
- Holiday Status distinguishes Off, Scheduled, Active and Ended, with error/unknown handling as appropriate.
- Holiday Start and Holiday End display absolute **local** date/time text (for example, `02 Dec 2026, 12:00`). Their original UTC timestamps are retained in `utc_datetime` attributes. The temporary duplicate `(Local)` sensors were removed from the integration; their orphaned Home Assistant entity-registry entries were subsequently deleted by the user.
- The names **Holiday Start** and **Holiday End** are retained. Home Assistant may display End before Start due to alphabetical sorting; no artificial numbering is required.
- The `tado_x.set_holiday_mode` action provides date/time selectors for **both** `start_date` and `end_date`, while continuing to accept explicit ISO-8601 values, including historical dates.
- Holiday Mode refreshes are home-scoped and independent of per-room schedule-profile comparison settings. Scheduled start/end callbacks and successful holiday-setting operations refresh holiday data; relevant operations also refresh the main coordinator to update hot-water entities.
- Switching Holiday Mode on preserves valid stored dates if the end remains in the future. If the stored holiday has expired, it creates a new seven-day period beginning immediately. Switching off preserves the stored dates and settings. Existing per-room temperature and hot-water holiday settings are preserved through read-modify-write; a failed initial read is not treated as an empty configuration.
- The existing Next Schedule Change/Power/Temperature sensors continue to describe the underlying room schedule, which Holiday Mode can override.
- Hot Water State accepts the Tado-specific values `HOLIDAY_MODE_OFF` and `HOLIDAY_MODE_ON`; Hot Water Mode maps them to **Off** and **Schedule**, respectively. Holiday Mode changes trigger refreshes of hot-water entities.

**Live observations and acceptance (1 November 2026)**

- On both configured homes, the user confirmed the Holiday Mode switch, status/start/end sensors and refresh button are present and working.
- The user confirmed that Holiday Mode switching on and off updates hot-water entities, including returning to ordinary hot-water states when Holiday Mode is disabled.
- With active Holiday Mode and hot water off: **Hot Water State = `HOLIDAY_MODE_OFF`; Hot Water Mode = Off**.
- With hot water enabled during Holiday Mode: **Hot Water State = `HOLIDAY_MODE_ON`**. The user also confirmed the final functional checklist; the integration maps this to Hot Water Mode = Schedule.
- The user confirmed the simplified absolute local date/time sensors and both action date/time selectors work.
- The user removed the obsolete `(Local)` entity-registry entries; they no longer need code support.
- These are **user-reported live Home Assistant/Tado tests**. They are not independent automated tests, and do not establish exhaustive API, timezone, scheduled-boundary or regression coverage.

**Files involved in DEV-001:** Integration modules for API/coordinator, switch, sensor, button, select and action handling; `services.yaml`, `strings.json`, translations, and relevant documentation and changelog. Consult the accepted source ZIP and Git diff for the definitive changed-file list.

**Acceptance decision:** DEV-001 is closed for the agreed functional scope. The refined candidate is the accepted development baseline, pending replacement of the Project Source ZIP and commit to `develop`. No published release or version change has been made.

## Validation register

| Check | Current result |
|---|---|
| Development ZIP structure | Repository-root layout with `custom_components/tado_x/` and `docs/` verified during development |
| Development ZIP integrity | Refined candidate archive integrity verified during preparation |
| Manifest | Domain `tado_x`; version remains `1.0.0` |
| Python syntax | Passed for DEV-001 candidate (static validation) |
| JSON/YAML parsing | Passed for DEV-001 candidate (static validation) |
| Home Assistant startup and entity creation | User confirmed after installation/restart; Holiday Mode and hot-water entities available |
| Multi-home functionality | User confirmed functional checks on both configured homes |
| Holiday Mode switch and refresh button | User confirmed working |
| Holiday Status, Start and End | User confirmed working; absolute local dates verified |
| `set_holiday_mode` UI selectors | User confirmed both date/time selectors working |
| Hot water when Holiday Mode active | `HOLIDAY_MODE_OFF` and `HOLIDAY_MODE_ON` observed live; selector handling and switching checks confirmed |
| Automatic scheduled-boundary transitions | Implemented, but no specific live boundary test was reported |
| Full automated HA/Tado regression suite | Not performed or reported |

## Working procedure

1. Start from the latest `Tado_X_Enhanced_Development.zip` and check its relationship to the `develop` branch.
2. Investigate an issue, agree the design, and record decisions in this file.
3. Implement minimal changes and produce complete replacement files or an updated complete development ZIP.
4. Perform and report static validation, then install and test in Home Assistant as appropriate.
5. Record test results, unresolved problems and any follow-up corrections.
6. Commit accepted changes to `develop`, with descriptive commit messages.
7. Replace the Project's development ZIP and update this file and the relevant individual documentation sources to match the accepted baseline.
8. When release scope and testing are agreed, prepare release notes, agree a semantic version, merge to `main`, tag and publish. Do not do this automatically.

## Release planning

**Next release:** Not yet decided. A patch or minor version will be chosen when release scope is agreed; no release date has been set.

**Completed development issues:** DEV-001 — Holiday Mode enhancements (accepted 1 November 2026).

**Outstanding issues:** None recorded in this document at the time of this update. Further improvements or regressions should receive new issue IDs.

**Repository and Project Source status:** The refined DEV-001 ZIP has passed the reported live functional checks and is approved as the new development baseline. Replacing the existing Project Source `Tado_X_Enhanced_Development.zip` and committing to GitHub's `develop` branch are separate housekeeping actions; this document does not imply either action has already occurred.

**Version:** The integration remains `1.0.0` until a release is explicitly agreed.
