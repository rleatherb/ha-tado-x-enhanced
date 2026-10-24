# Tado X Enhanced for Home Assistant

An independently maintained custom integration for controlling and monitoring **Tado X** systems in [Home Assistant](https://www.home-assistant.io/).

Tado X Enhanced builds on the original [Tado X integration by exabird](https://github.com/exabird/ha-tado-x), adding multi-home support, Home and Away schedule management, reusable schedule profiles, domestic hot-water controls, richer room diagnostics and API quota forecasting.

> **Project status:** Preparing the first independent release (`1.0.0`). Some features depend on your Tado hardware, subscription and API responses. This is a cloud-based integration and is subject to Tado API limits.

**[Changelog](CHANGELOG.md)** · [Report an issue](https://github.com/rleatherb/ha-tado-x-enhanced/issues) · [Releases](https://github.com/rleatherb/ha-tado-x-enhanced/releases)

## Highlights

- **Multiple homes:** Configure more than one Tado home, with separate coordinators, home-scoped operations and profile storage. Rooms with the same numerical ID in different homes remain distinct.
- **Heating control:** Room thermostats, manual overrides, termination modes, open-window detection and home-wide heating quick actions.
- **Schedules:** Read and change Home schedules and Away settings; inspect next schedule changes, target temperatures and power states.
- **Schedule profiles:** Save and restore **Normal**, **Alternative**, **Eco** and **Not in use** profiles per room, with separate home-wide defaults and factory fallbacks. A **Custom** state identifies schedules that do not match a saved profile.
- **Hot water:** Where supported, view hot-water state, choose Schedule/Off/Boost and inspect boost or schedule-change timing.
- **API monitoring:** Track quota limit, remaining calls, current usage and estimated daily usage. Learn the approximate reset time from server-reported quota observations rather than assuming a fixed clock time.
- **Additional data:** Heating running time, weather, air comfort, mobile presence, historical day reports and Energy IQ actions where supported and enabled.
- **Five languages:** English, German, French, Italian and Spanish.

## Installation through HACS

Once this repository is **public** and a release has been published:

1. Install [HACS](https://www.hacs.xyz/) if it is not already installed.
2. In Home Assistant, open **HACS → Custom repositories**.
3. Add `https://github.com/rleatherb/ha-tado-x-enhanced` and select **Integration**.
4. Open the repository entry in HACS and select **Download**.
5. Restart Home Assistant.
6. Go to **Settings → Devices & services → Add integration**, search for **Tado X Enhanced**, and complete authentication and home selection.

This is a **custom repository** installation; inclusion in the default HACS catalogue is not required. Exact HACS menu labels can vary by version.

### Existing Tado X installations

**Back up Home Assistant before switching.** This integration intentionally retains the Home Assistant domain `tado_x` to preserve compatibility with existing configuration entries and entity identifiers where possible. Consequently, **it cannot be installed alongside another integration using the `tado_x` domain**.

If you currently use the original integration or a development build:

1. Back up your Home Assistant configuration and the integration's saved data.
2. Remove the old integration's installed **code** or old HACS repository association as appropriate; **do not delete your configured Tado homes** merely to change the source repository.
3. Install this repository through HACS, then restart Home Assistant.
4. Confirm that your homes, entities, actions, hot-water controls and saved schedule profiles remain available.

Migration should be tested carefully; preserving the domain does not guarantee compatibility with every older version or installation method.

## Configuration

Each configured Tado home has its own options under **Settings → Devices & services → Tado X → Configure**.

| Setting | Purpose |
| --- | --- |
| Auto-Assist subscription | Sets subscription-related defaults and feature availability assumptions. |
| Main update interval | General integration polling, in seconds (configuration range: 30–3600). |
| Automatically check for schedule changes | Enable periodic Home/Away schedule comparisons. Defaults to on for Auto-Assist and off otherwise, unless explicitly set. |
| Schedule check interval | Separate schedule polling interval: 900–86400 seconds (15 minutes–24 hours); default 3600 seconds. |
| Weather | Enable weather data where available. |
| Mobile devices | Enable mobile presence/tracker data. |
| Air comfort | Enable air-comfort data. |
| Running times | Enable heating running-time data. |
| Flow temperature | Enable supported flow-temperature controls/data. |
| Hot water | Enable domestic hot-water functionality where supported. |

**API usage matters:** A complete automatic schedule check uses approximately **two API calls per room** (one Home schedule and one Away settings read). For 33 rooms, hourly checks would use approximately **1,584 requests per day** for this feature alone. Manual profile operations and the **Refresh Schedule** button remain available when automatic schedule checking is disabled.

## Devices and entities

Available entities vary with hardware, account capabilities and configuration.

| Device type | Main entities and controls |
| --- | --- |
| **Tado X Home** | Home ID; presence sensors/select; API quota, calls, current usage, estimated daily usage and reset time; home-wide heating buttons; supported hot-water sensors, mode selector and buttons; flow-temperature controls. |
| **Tado X Room** | Climate thermostat; temperature, humidity, heating power and running time; next schedule change, temperature and power; open-window/heating/override status; termination settings; save/restore profile selectors; **Refresh Schedule** button. |
| **Physical Tado X device** | Battery, device temperature, temperature offset, connection state, low-battery status and child lock where supported. |
| **Weather / air comfort / mobile** | Optional weather, comfort and presence entities. |

### Room schedule profiles

The four named profiles are **Normal**, **Alternative**, **Eco** and **Not in use**. Each profile can store the room's full Home weekly schedule **and** Away configuration (including Away temperature and preheating where supported).

A room-specific profile takes precedence over its matching home-wide default on ordinary restore. Selecting an explicit `… default` option restores the home-wide template instead. If no custom home default is saved, the integration has a predefined factory fallback. Saving or resetting a default does **not** immediately alter active room schedules.

The integration initially captures the current room schedule as **Normal** if that room profile is missing. The **Custom** indication is based on the most recent comparison; when automatic checks are off, use **Refresh Schedule** to detect changes made outside Home Assistant.

## Actions

The integration exposes **16 actions** in **Developer Tools → Actions**, all under `tado_x`:

| Action | Purpose |
| --- | --- |
| `tado_x.set_temperature_offset` | Calibrate a physical Tado X device. |
| `tado_x.add_meter_reading` | Submit an Energy IQ meter reading. |
| `tado_x.set_eiq_tariff` | Set an Energy IQ tariff. |
| `tado_x.set_climate_timer` | Set a timed, manual or next-time-block room temperature override. |
| `tado_x.get_schedule` | Retrieve a room's Home schedule. |
| `tado_x.set_schedule` | Replace a selected day of a room's Home schedule. |
| `tado_x.get_away_schedule` | Retrieve a room's Away configuration. |
| `tado_x.set_away_schedule` | Update a room's Away configuration. |
| `tado_x.get_day_report` | Retrieve a room's historical day report. |
| `tado_x.get_holiday_mode` | Read home holiday-mode settings. |
| `tado_x.set_holiday_mode` | Update home holiday-mode settings where supported. |
| `tado_x.save_schedule_profile` | Save a room profile or home-wide default. |
| `tado_x.restore_schedule_profile` | Restore a room profile or home-wide default. |
| `tado_x.list_schedule_profiles` | List profile availability for a room. |
| `tado_x.delete_schedule_profile` | Delete a saved room profile. |
| `tado_x.reset_schedule_default` | Revert a home-wide default to the factory template. |

Example — set a temperature for 60 minutes:

```yaml
action: tado_x.set_climate_timer
data:
  entity_id: climate.living_room
  temperature: 21
  termination_type: TIMER
  duration: 60
```

For `MANUAL` and `NEXT_TIME_BLOCK`, specify the desired temperature and omit `duration`. The `entity_id` above is an example and must match your installation.

When more than one Tado home is configured, home-level actions require selecting the appropriate **Tado X Home device**; room actions are routed through their room climate entity.

## Climate attributes and diagnostics

Room climate entities may expose `manual_control_active`, `manual_control_type`, `manual_control_remaining_minutes`, `heating_power`, `next_schedule_change`, `next_schedule_temperature`, `open_window_detected`, `open_window_ends_at` and `open_window_remaining_minutes`, where data is available. The next scheduled power state is available as a separate sensor. `hvac_action` is a standard Home Assistant climate property and depends on available heating-state data.

The Restore schedule profile selector also exposes match information such as `match_status`, `matching_profiles`, `last_applied_profile` and `saved_profiles`.

### API usage estimates

- **API current usage** reports the proportion of the daily quota consumed.
- **API reset time** is estimated from a substantial drop in server-reported calls used. It can remain `unknown` until a reset has been observed.
- **API estimated daily usage** extrapolates consumption from elapsed time since the observed reset; it can exceed **100%**. It is deliberately unavailable during the first hour after a reset.

These calculations do not require additional API calls. They are estimates, not guarantees of Tado's future quota behaviour. Do not assume separate home sensors represent separate quota pools without verifying account-level reporting.

## Compatibility and limitations

- This is a **cloud-polling** integration; a working Tado account and internet connection are required.
- Some functionality requires compatible hardware, enabled options, or Tado Auto-Assist/API access.
- Tado's API is not controlled by this project and may change or impose request limits.
- Multiple homes are supported, but verify service targeting and quota reporting when configuring more than one home.
- The minimum supported Home Assistant release has **not yet been established by testing**. Do not infer compatibility solely from the manifest version.
- The first independent release should be validated on a test Home Assistant installation before wider distribution.

## Releases and changes

See **[CHANGELOG.md](CHANGELOG.md)** for the initial feature set, compatibility notes and all future release changes. Versioning follows [Semantic Versioning](https://semver.org/).

## Issues and contributions

Please use [GitHub Issues](https://github.com/rleatherb/ha-tado-x-enhanced/issues) for reproducible bugs and feature requests. Include your Home Assistant version, integration version, relevant entity type and redacted debug logs. **Never post access tokens, refresh tokens or other account credentials.**

## Credits and licence

Tado X Enhanced is an **independently maintained derivative** of the original [ha-tado-x project by Exabird](https://github.com/exabird/ha-tado-x). The original integration and its contributors are acknowledged with thanks. This project is independently maintained and is not affiliated with or endorsed by Tado or the original maintainer.

This project is distributed under the **[MIT License](LICENSE)**. The licence file preserves the original copyright notice and identifies the subsequent enhancements:

- **Copyright (c) 2025 Exabird** — original integration.
- **Copyright (c) 2026 Robin Leatherbarrow** — subsequent modifications and enhancements.

The MIT licence permits use, modification and redistribution subject to retention of the required copyright and permission notices. See the complete [LICENSE](LICENSE) file for its terms and warranty disclaimer.

Project maintenance and GitHub code ownership: [@rleatherb](https://github.com/rleatherb).
