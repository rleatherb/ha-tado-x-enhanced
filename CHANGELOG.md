# Changelog

All notable changes to **Tado X Enhanced** will be documented in this file.

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The project is independently maintained and is derived from the original Tado X integration for Home Assistant. Version **1.0.0** is the first release under this project's own versioning scheme; earlier development revisions are not listed individually.

**[Readme](README.md)** · [Report an issue](https://github.com/rleatherb/ha-tado-x-enhanced/issues) · [Releases](https://github.com/rleatherb/ha-tado-x-enhanced/releases)

## [1.0.0](https://github.com/rleatherb/ha-tado-x-enhanced/releases/tag/v1.0.0) - Initial Release

This integration is a development of the original [Tado X integration by exabird](https://github.com/exabird/ha-tado-x) (version 1.8.11). Changes from this are as below:

### Added

- Extended support for configuring multiple Tado homes in one Home Assistant installation, with home-scoped entities, operations, and schedule data.

- Home and Away schedule management through Home Assistant actions, including retrieving, updating, and refreshing room schedules.

  - This feature is an enhanced version of the implementation specified in the following pull request: [Feat/schedule and historic data by ilyesAj · Pull Request #90 · exabird/ha-tado-x](https://github.com/exabird/ha-tado-x/pull/90). Differences include implementing full multi-room compatibility, adding Away schedule information.

- Room-specific heating schedule profiles named **Normal**, **Alternative**, **Eco**, and **Not in use**, including saving, restoring, and detecting schedules that differ from a saved profile (displayed as **Custom** when no match is stored). The heating schedules include both the Home and Away settings, including the preheating configuration supported by the Tado API.

  - [Full  description of how heating schedule profiles are used.](docs/SCHEDULES.md)

  - On start-up, if a room has no saved **Normal** profile, the current heating schedule defined by the Tado app is automatically saved for future use. This means that the current heating schedule can easily be restored without needing to save this explicitly. This will, in general, only happen the first time that this integration is used.

  - Per-home default schedule profiles for each of these four named schedules. Selecting one of these for a room that has no specific version stored will use the default. The defaults for each home can also be set, allowing rooms access to customised but generic schedules when selecting one of these.

  - Home Assistant controls added to refresh schedules and manage schedule profiles.

- Added hot-water state handling, including Away modes, boost status, remaining boost time, and next scheduled change where available.

  - This feature is an enhanced version specified in the following pull request: [DHW Control by donalfenwick · Pull Request #53 · exabird/ha-tado-x](https://github.com/exabird/ha-tado-x/pull/53)

- Added retrieval of historic heating data from Tado

  - This feature is inspired by the implementation specified in the following pull request: [Feat/schedule and historic data by ilyesAj · Pull Request #90 · exabird/ha-tado-x](https://github.com/exabird/ha-tado-x/pull/90).

- Additional room information added, including upcoming schedule changes and temperatures, manual-control timing, and open-window expiry and remaining time where available.

- Additional API quota monitoring, including server-reported quota limits and remaining calls, current usage percentage, observed reset-time detection, and estimated daily usage percentage.

- Enhanced temperature setting

  - Changes to temperature via Home Assistant thermostat cards now work the same way as if the change is made on a Tado device, using the per-room settings shown in the Tado app to determine whether the temperature change is for a set time period, until the next schedule change, or lasts indefinitely.

  - The per-room settings for how manual control of temperature should be interpreted (indefinite, until next schedule change, for a defined period of time) are now available as a per-room Termination Type select entity and Timer Duration number entity.

- Support to read and set holiday mode

  - This feature is inspired by the implementation specified in the following pull request: [Feat/schedule and historic data by ilyesAj · Pull Request #90 · exabird/ha-tado-x](https://github.com/exabird/ha-tado-x/pull/90).

- Added display of serial number information for all Tado X devices

- Translations for English, German, French, Italian, and Spanish.

  - Please note that the non-English translations are machine coded.

### Changed

- Extended the original integration's controls, sensors, and service handling while retaining the Home Assistant integration domain `tado_x`.
- Improved multi-home action routing, including home-device selection for actions that need an explicit home target.
- Improved `set_climate_timer` implementation that includes  **TIMER**, **MANUAL**, and **NEXT_TIME_BLOCK** termination types.
  - This feature is inspired by the implementation specified in the following pull request: [Feature: Termination type configuration by xiic · Pull Request #54 · exabird/ha-tado-x](https://github.com/exabird/ha-tado-x/pull/54). It is enhanced to support multi-home installations
- Added configurable automatic schedule-change checks and a separate schedule polling interval (15 minutes to 24 hours; default one hour). Automatic checking defaults to enabled for Auto-Assist configurations and disabled otherwise, unless explicitly configured.
- Renamed the displayed **API usage** sensor to **API current usage** while retaining its existing entity identity.
- Replaced the fixed API reset-time assumption with an observed, account-response-based estimate. The reset-time and projected-usage sensors can remain `unknown` until sufficient observations are available.
- Updated the integration's translated service descriptions, labels, and options.

### Fixed

- Service registration and routing when more than one Tado home is configured. Routines that were incompatible with multi-home setups corrected (`set_climate_timer`, `set_temperature_offset`, `add_meter_reading`, `set_eiq_tariff`)
- Error messages warning about certain depreciated calls that would not be supported in future Home Assistant releases.

### Removed

- The previous fixed daily API reset-time assumption.

### Compatibility notes

- A HACS migration from Exabird's original integration to Enhanced was successfully tested in October 2026 on a two-home Home Assistant installation: 105 existing devices were retained, checked entity IDs were preserved, and the integration loaded without reported startup errors or warnings. The documented handover avoids deleting existing Home Assistant configuration entries. This is not a guarantee for every earlier version.

- The Home Assistant integration domain remains `tado_x`. This project **replaces** other installations using the same domain; it cannot run alongside the original integration in one Home Assistant instance.
- Back up Home Assistant before replacing an existing installation. Verify both home entries, entities, and stored schedule profiles after migration.
- Some functionality depends on the connected Tado devices, the account's subscription, and API responses. Cloud API quotas apply.
- API reset-time detection is observational rather than an exact server-announced reset timestamp. Estimated daily usage may exceed 100% and may initially be unavailable.



## Unreleased — DEV-001 (development build)
- Added home-level Holiday Mode switch, status and timestamp sensors, and refresh button.
- Added independent home-level holiday polling and start/end event callbacks.
- Switch-on preserves valid unexpired periods or starts a fresh seven-day holiday immediately.
- Holiday API updates now require a successful read of existing room settings.
- Holiday action writes refresh the holiday entity cache.
- Recognise `HOLIDAY_MODE_OFF` and `HOLIDAY_MODE_ON` in hot-water state and map these to Off / Schedule in the mode selector; refresh hot water after holiday switching, manual refresh and scheduled boundaries.
- Simplified Holiday Start and Holiday End to single absolute local date/time text sensors, removed duplicate (Local) entities, and provided datetime selectors for both action dates.
