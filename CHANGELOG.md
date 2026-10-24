# Changelog

All notable changes to **Tado X Enhanced** will be documented in this file.

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The project is independently maintained and is derived from the original Tado X integration for Home Assistant. Version **1.0.0** is the first release under this project's own versioning scheme; earlier development revisions are not listed individually.

## [Unreleased]

### Added

### Changed

### Fixed

## [1.0.0] - Unreleased

### Added

- Support for configuring multiple Tado homes in one Home Assistant installation, with home-scoped entities, operations, and schedule data.
- Home and Away schedule management through Home Assistant actions, including retrieving, updating, and refreshing room schedules.
- Room schedule profiles named **Normal**, **Alternative**, **Eco**, and **Not in use**, including saving, restoring, and detecting schedules that differ from a saved profile (**Custom**).
- Per-home default schedule profiles, alongside room-specific profiles and predefined fallback schedules.
- Support for saving and restoring Away settings as part of schedule profiles, including Away temperature and preheating configuration where supported by the Tado API.
- Home Assistant controls to refresh schedules and manage schedule profiles.
- Additional hot-water state handling, including Away modes, boost status, remaining boost time, and next scheduled change where available.
- Additional room information, including upcoming schedule changes and temperatures, manual-control timing, and open-window expiry and remaining time where available.
- API quota monitoring, including server-reported quota limits and remaining calls, current usage percentage, observed reset-time detection, and estimated daily usage percentage.
- Additional actions for schedule management, Away settings, historical/day reports, and home-level schedule defaults.
- Translations for English, German, French, Italian, and Spanish.

### Changed

- Extended the original integration's controls, sensors, and service handling while retaining the Home Assistant integration domain `tado_x`.
- Improved multi-home action routing, including home-device selection for actions that need an explicit home target.
- Improved `set_climate_timer` validation for **TIMER**, **MANUAL**, and **NEXT_TIME_BLOCK** termination types.
- Added configurable automatic schedule-change checks and a separate schedule polling interval (15 minutes to 24 hours; default one hour). Automatic checking defaults to enabled for Auto-Assist configurations and disabled otherwise, unless explicitly configured.
- Reduced unnecessary schedule API requests by reusing retrieved data and avoiding redundant schedule comparisons.
- Renamed the displayed **API usage** sensor to **API current usage** while retaining its existing entity identity.
- Replaced the fixed API reset-time assumption with an observed, account-response-based estimate. The reset-time and projected-usage sensors can remain `unknown` until sufficient observations are available.
- Updated the integration's translated service descriptions, labels, and options.

### Fixed

- Service registration and routing when more than one Tado home is configured.
- Hot-water mode presentation in Away and boost scenarios.
- Schedule and historical-data action handling and validation.
- Home Assistant device-registry compatibility issues affecting certain controls.
- Configuration-flow errors affecting the integration's **Configure** dialog.

### Removed

- The previous fixed daily API reset-time assumption.
- The full weekly schedule stored as a climate entity attribute, to reduce entity-state overhead; schedule data remains accessible through the relevant actions and profile controls.

### Compatibility notes

- The Home Assistant integration domain remains `tado_x`. This project **replaces** other installations using the same domain; it cannot run alongside the original integration in one Home Assistant instance.
- Back up Home Assistant before replacing an existing installation. Verify both home entries, entities, and stored schedule profiles after migration.
- Some functionality depends on the connected Tado devices, the account's subscription, and API responses. Cloud API quotas apply.
- API reset-time detection is observational rather than an exact server-announced reset timestamp. Estimated daily usage may exceed 100% and may initially be unavailable.

[Unreleased]: https://github.com/rleatherb/ha-tado-x-enhanced/compare/1.0.0...HEAD
[1.0.0]: https://github.com/rleatherb/ha-tado-x-enhanced/releases/tag/1.0.0
