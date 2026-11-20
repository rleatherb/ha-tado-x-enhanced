# Actions Reference

[README](../README.md) · [Schedules](SCHEDULES.md) · [Examples](EXAMPLES.md) · [Architecture](ARCHITECTURE.md)

Tado X Enhanced v1.4.0 registers **31 actions** under `tado_x`, available in **Developer Tools → Actions**. The following parameters were checked against the service schemas in `custom_components/tado_x/__init__.py` and descriptions in `services.yaml`.

**Targeting:** `entity_id` identifies a room climate entity and resolves its home. For home-level actions, `device_id` identifies the **Tado X Home** device; it may be omitted only when a single home is configured. `set_temperature_offset` requires the physical device's `device_id`. Profile names are free-text strings (up to 80 characters), validated against the names defined for the selected home.

| Action (`tado_x.` prefix) | Purpose | Inputs | Version |
|---|---|---|---|
| `refresh_schedule` | Read room schedule and update profile comparison | `entity_id` (required climate) | 1.4.0 |
| `refresh_schedule_home` | Refresh eligible rooms in a home | `device_id` (optional for single home) | 1.4.0 |
| `identify_device` | Flash a supported physical Tado X device | `device_id` (required physical device) | 1.4.0 |
| `get_running_times` / `get_room_running_time` / `get_home_running_time` | Read heating running-time data on demand | See Running Times documentation | 1.4.0 |
| `set_temperature_offset` | Physical-device temperature offset | `device_id` (required), `offset` (required; −9.9 to +9.9 °C) | Inherited; updated 1.0.0 |
| `add_meter_reading` | Submit Energy IQ meter reading | `reading` (required nonnegative integer), `date` (optional YYYY-MM-DD), `device_id` (optional home device) | Inherited; updated 1.0.0 |
| `set_eiq_tariff` | Set Energy IQ tariff | `tariff` (required nonnegative number), `unit` (`m3` or `kWh`), `start_date`, `end_date` (optional), `device_id` (optional home device) | Inherited; updated 1.0.0 |
| `set_climate_timer` | Room temperature override | `entity_id` (required climate), `temperature` (5–30 °C; required for a change), `termination_type` (`TIMER`, `MANUAL`, `NEXT_TIME_BLOCK`; defaults to `TIMER`), `duration` (1–1440 minutes; required for `TIMER`) | Inherited; updated 1.0.0, 1.3.0 |
| `get_schedule` | Read room Home schedule | `entity_id` (required climate) | 1.0.0 |
| `set_schedule` | Write a complete selected Home day schedule | `entity_id`, `day_type`, `schedule` (all required; `schedule` is a JSON **string** of blocks) | 1.0.0 |
| `get_away_schedule` | Read room Away configuration | `entity_id` (required climate) | 1.0.0 |
| `set_away_schedule` | Write room Away configuration | `entity_id` and `mode` (`ON`/`OFF`) required; `away_temperature` (0.1–49.9 °C) and `preheating_level` (`OFF`/`ECO`/`BALANCE`/`COMFORT`) optional | 1.0.0; updated 1.3.0 |
| `get_day_report` | Read room historical report | `entity_id` (required climate), `date` (optional) | 1.0.0 |
| `get_holiday_mode` | Read home holiday mode | `device_id` (optional home device) | 1.0.0 |
| `set_holiday_mode` | Set home holiday mode | `enabled` (required boolean), `start_date`, `end_date` (optional), `device_id` (optional home device) | 1.0.0; updated 1.1.0, 1.1.1 |
| `save_schedule_profile` | Save live room Home/Away schedule under an existing profile name | `entity_id`, `profile` (both required) | 1.0.0 |
| `restore_schedule_profile` | Apply saved room profile or home default fallback | `entity_id`, `profile` (both required) | 1.0.0 |
| `list_schedule_profiles` | Return profile names, saved/default state and current matching status | `entity_id` (required); returns response data | 1.0.0 |
| `save_schedule_profile_default` | Save live room Home/Away schedule as a home-wide default | `entity_id`, `profile` (both required) | 1.0.0 |
| `restore_schedule_profile_default` | Apply home-wide default to selected room | `entity_id`, `profile` (both required) | 1.0.0 |
| `create_schedule_profile` | Create a custom home-wide profile class | `profile` (required), `device_id` (optional home device) | 1.0.0 |
| `delete_schedule_profile` | Delete a custom home-wide profile class and its saved data | `profile` (required), `device_id` (optional home device); built-ins prohibited | 1.0.0 |
| `set_polling_options` | Change per-home polling settings without restarting | `device_id` (optional for single home); any subset of supported polling fields listed below | 1.2.0 |
| `reset_schedule_default` | Reset a built-in home-wide default to factory fallback | `profile` (required built-in name), `device_id` (optional home device) | 1.0.0 |

Version identifies the introduction or documented interface update in Tado X Enhanced; inherited actions are marked separately. Internal refresh-monitoring changes are not treated as new action interfaces.

## Climate override example

```yaml
action: tado_x.set_climate_timer
data:
  entity_id: climate.living_room
  temperature: 21
  termination_type: TIMER
  duration: 60
```

For `MANUAL` and `NEXT_TIME_BLOCK`, omit `duration`. The entity ID is illustrative.

## Set schedule: input format

`day_type` must be one of the supported day/group options in the action selector. Each JSON block's `dayType` must match the selected value. The first block must begin at `00:00`, adjacent blocks must meet exactly, and the last must end at `24:00`. `ON` requires numeric `setting.temperature.value`. The action field `schedule` must be a **string containing JSON**, not a YAML array.

```yaml
action: tado_x.set_schedule
data:
  entity_id: climate.living_room
  day_type: MONDAY
  schedule: >-
    [{"dayType":"MONDAY","start":"00:00","end":"07:00","setting":{"power":"ON","temperature":{"value":18.0}}},
     {"dayType":"MONDAY","start":"07:00","end":"24:00","setting":{"power":"ON","temperature":{"value":21.0}}}]
```

## Profile scope and defaults

The built-in names are **Normal**, **Alternative**, **Eco** and **Not in use**. Additional names are created per home using `create_schedule_profile`. `save_schedule_profile` and `restore_schedule_profile` work with a room-specific saved profile (falling back to a home default on restore); `save_schedule_profile_default` and `restore_schedule_profile_default` explicitly manage/apply the **home-wide default**. `delete_schedule_profile` deletes a custom profile **across the selected home**, not merely a room's copy. `reset_schedule_default` resets only built-in home defaults.

`list_schedule_profiles` returns profile availability and matching status for the requested room. Its response keys include `profiles`, `home_defaults`, `current`, `status` and `matching_profiles`.

## API and testing notes

Read and write operations require Tado cloud access and are subject to API quotas. Some actions require hardware, subscription or account capabilities. Schedule restoration may involve multiple remote writes; it is not an atomic transaction. See [SCHEDULES.md](SCHEDULES.md) for workflows and [ARCHITECTURE.md](ARCHITECTURE.md) for validation and recovery behaviour.


### Holiday Mode and the home switch
`set_holiday_mode` offers local date/time pickers for optional start and end dates. YAML also accepts timezone-aware ISO-8601 timestamps. Both start and end times must be on a **30-minute boundary (HH:00 or HH:30)**. Supplying one date preserves the other existing boundary; date updates are checked against Tado after submission and raise an error if the dates are not retained. Explicit past start dates are accepted. The Holiday Mode switch provides automatic seven-day rescheduling only when the stored period has expired.

## Programmatic polling configuration

`tado_x.set_polling_options` accepts an optional Tado X Home `device_id` and any subset of polling options. The device is inferred when exactly one Tado X home is configured; with multiple homes, select the Tado X Home device. Unspecified options remain unchanged. All settings are validated before being saved and applied immediately, without a Home Assistant restart. Changes persist after restart.

```yaml
action: tado_x.set_polling_options
data:
  device_id: YOUR_TADO_X_HOME_DEVICE_ID
  scan_interval: 300
  supplementary_poll_multiplier: 10
  enable_schedule_polling: false
  enable_holiday_polling: true
```

The `device_id` line may be omitted for a single-home installation.

Supported optional fields: `scan_interval` (30–3600), `supplementary_poll_multiplier` (1, 2, 5, 10), `schedule_poll_interval` (900–86400), `enable_schedule_polling`, `enable_holiday_polling`, `enable_weather`, `enable_air_comfort`, `enable_running_times`, `enable_flow_temp`, `enable_mobile_devices` and `enable_hot_water`. All `enable_*` fields are booleans. A day/night automation should also run at Home Assistant startup to restore the appropriate current setting after a restart.


## Whole-home actions

The home-wide profile operations are `save_schedule_profile_home` and `restore_schedule_profile_home`; `set_hvac_mode_home` applies HVAC mode to eligible rooms.

| Action | Version |
|---|---|
| `tado_x.set_hvac_mode_home` | 1.3.0 |
| `tado_x.set_climate_timer_home` | 1.3.0 |
| `tado_x.set_away_schedule_home` | 1.3.0 |
| `tado_x.save_schedule_profile_home` | 1.3.0 |
| `tado_x.restore_schedule_profile_home` | 1.3.0 |

The following actions target the selected **Tado X Home** device (`device_id`). The device is optional when only one Tado X home is configured, but mandatory for multiple homes. A room device is not accepted. All actions process rooms **sequentially** and independently, continue after a room fails, and report all failures together with the count and names of successful rooms. There is no whole-home rollback. A successful call is logged; partial failures raise a Home Assistant action error that lists successes and failures.

- `tado_x.set_hvac_mode_home`: `hvac_mode` (`auto`, `heat`, `off`). `auto` resumes each room’s existing Tado schedule; `heat` applies each room’s current target temperature (or 21 °C fallback) as a manual override; `off` switches each room off manually. Like the other whole-home actions, rooms are processed sequentially with aggregated failures and a single final coordinator refresh.
- `tado_x.set_climate_timer_home`: `temperature` (5–30 °C), optional `termination_type` (`TIMER`, `MANUAL`, `NEXT_TIME_BLOCK`; defaults to `TIMER`), and `duration` (1–1440 minutes; required for `TIMER`). Applies identical settings to all eligible rooms.
- `tado_x.set_away_schedule_home`: `mode` (`ON` or `OFF`), optional `away_temperature` and `preheating_level`. As with the room action, omitted values preserve each room's current settings when available; `away_temperature` is needed when turning ON from a room with no existing Away temperature. Does not modify saved profiles.
- `tado_x.save_schedule_profile_home`: `profile` must be an existing home-wide name. Saves each room's current Home and Away schedules into its own version of the profile; does not change active schedules or home defaults.
- `tado_x.restore_schedule_profile_home`: `profile` must be an existing home-wide name. Restores each room's own profile or the home default/factory fallback, preserving existing per-room rollback behaviour. One coordinator refresh is requested after the batch.

For both profile actions, an unknown profile name is rejected **before** processing any rooms. Create custom names using `tado_x.create_schedule_profile` first. Names are scoped to the selected home.

**Temperature controls:** Tools > Actions sliders for `set_climate_timer`, `set_climate_timer_home`, `set_away_schedule` and `set_away_schedule_home` accept 0.1 °C increments. The Away sliders show 5–30 °C for convenience; the existing underlying Away action validation remains 0.1–49.9 °C for YAML calls.

**Room discovery limitation:** Only rooms successfully configured during the integration's setup and possessing an initial saved `Normal` profile are eligible for these actions. If Tado adds a room during normal polling, it is reported as skipped until **Tado X Enhanced is reloaded**. A failed initial `Normal` capture likewise excludes that room until corrected/reloaded. This prevents whole-home actions from changing an uninitialised room. No dynamic entity registration is attempted.

Example:

```yaml
action: tado_x.restore_schedule_profile_home
data:
  device_id: YOUR_TADO_X_HOME_DEVICE_ID
  profile: Winter
```

The `device_id` line can be omitted when only one home is configured.

## Historical heating running times

All three actions are read-only, require one Minder API request per invocation and have no scheduled polling. Home actions accept a Tado X Home `device_id` (required with multiple homes); room actions accept a native room climate `entity_id` to resolve the home safely. Dates use `YYYY-MM-DD` and default to today. The detailed range action supports up to 31 days. These are response-producing actions: use `response_variable` in Home Assistant automations/scripts to populate helpers or template-based displays.

| Action | Inputs | Response | Version |
| :--- | :--- | :--- | :--- |
| `tado_x.get_running_times` | `device_id`, `from_date`, `to_date` | Original Minder `runningTimes` (zones annotated with `name`), `summary`, and `lastUpdated` | 1.4.0 |
| `tado_x.get_room_running_time` | `entity_id`, `date` | `running_time_seconds`, room/home IDs and names, `last_updated` | 1.4.0 |
| `tado_x.get_home_running_time` | `device_id`, `date` | `running_time_seconds`, home ID/name, `last_updated` | 1.4.0 |

Example room query:

```yaml
action: tado_x.get_room_running_time
data:
  entity_id: climate.example_room
  date: "2026-11-18"
response_variable: room_duration
```

Use `room_duration.running_time_seconds` in subsequent automation steps. The example entity ID must be replaced with an existing native Tado X climate entity. Missing room/day information raises an error rather than being silently interpreted as zero. The detailed response retains the original Minder data for diagnostics. Completed-day Minder values can be higher than the maximum historical `Heating Time Today` reading.

## Identify a physical device

`tado_x.identify_device` requires `device_id` identifying a **physical** Tado X device, not a room or Home device. The device must advertise `supportsIdentify`. The action issues one on-demand identification request, returns `success`, `device_type`, `home_id`, and does not trigger coordinator polling. Supported devices also expose a **Blink Display** button.

```yaml
action: tado_x.identify_device
data:
  device_id: YOUR_PHYSICAL_TADO_DEVICE_ID
```
