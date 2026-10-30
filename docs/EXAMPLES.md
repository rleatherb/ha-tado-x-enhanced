# Usage Examples

[README](../README.md) · [Actions](ACTIONS.md) · [Schedules](SCHEDULES.md)

These examples use **Home Assistant action YAML**. Replace illustrative entity IDs and home device IDs with the IDs from your own installation. Some operations require supported hardware and Tado API access. For multi-home accounts, specify a Tado X **Home device** for home-level actions.

## 1. Timed room temperature override

```yaml
action: tado_x.set_climate_timer
data:
  entity_id: climate.living_room
  temperature: 21
  termination_type: TIMER
  duration: 60
```

The temperature remains overridden for 60 minutes. For an indefinite override, use `termination_type: MANUAL` and omit `duration`; to revert at the next scheduled block, use `NEXT_TIME_BLOCK` and omit `duration`.

## 2. Save the room's current schedule as Eco

First configure the desired Home schedule and Away settings in the Tado app, or use the corresponding schedule actions. Then save the live configuration:

```yaml
action: tado_x.save_schedule_profile
data:
  entity_id: climate.living_room
  profile: Eco
```

This changes the **saved room profile**, not the home-wide Eco default. The four built-in profile names are always available.

## 3. Restore a room profile

```yaml
action: tado_x.restore_schedule_profile
data:
  entity_id: climate.living_room
  profile: Normal
```

The room's saved Normal profile is applied, or the home-wide default if there is no room-specific copy. Restoration can perform multiple Tado API writes; see [ARCHITECTURE.md](ARCHITECTURE.md) for failure and rollback behaviour.

## 4. Create a new profile name for one home

```yaml
action: tado_x.create_schedule_profile
data:
  profile: Working from home
  device_id: YOUR_TADO_HOME_DEVICE_ID
```

The `device_id` is a **Home Assistant device ID** for the relevant Tado X Home, not the numerical Tado home ID. It is required when multiple Tado homes are configured. The new name becomes available in every room of that home. Its initial home default is copied from the effective Normal home default.

## 5. Save and apply a home-wide default

Save the current live schedule of a selected room as the home-wide Eco default:

```yaml
action: tado_x.save_schedule_profile_default
data:
  entity_id: climate.living_room
  profile: Eco
```

Apply that home-wide default to a different room:

```yaml
action: tado_x.restore_schedule_profile_default
data:
  entity_id: climate.office
  profile: Eco
```

These actions are in **Developer Tools → Actions**, not in the room's schedule-profile selectors. Saving a default does not immediately update other rooms.

## 6. Read a room's current schedule

```yaml
action: tado_x.get_schedule
data:
  entity_id: climate.office
```

The response is returned by the action. To set a schedule, supply a JSON **string** of contiguous blocks covering 00:00–24:00 for the selected day:

```yaml
action: tado_x.set_schedule
data:
  entity_id: climate.office
  day_type: MONDAY
  schedule: >-
    [{"dayType":"MONDAY","start":"00:00","end":"07:00","setting":{"power":"ON","temperature":{"value":18.0}}},
     {"dayType":"MONDAY","start":"07:00","end":"24:00","setting":{"power":"ON","temperature":{"value":20.0}}}]
```

## 7. Set Away heating behaviour

```yaml
action: tado_x.set_away_schedule
data:
  entity_id: climate.office
  mode: "ON"
  away_temperature: 16
  preheating_level: BALANCE
```

This updates the room's live Away configuration; it does **not** automatically overwrite saved schedule profiles.

## 8. Read holiday mode for a selected home

```yaml
action: tado_x.get_holiday_mode
data:
  device_id: YOUR_TADO_HOME_DEVICE_ID
```

For a single-home setup, `device_id` may be omitted. The action requires the corresponding Tado account capability.

## 9. Get a historical room report

```yaml
action: tado_x.get_day_report
data:
  entity_id: climate.living_room
  date: "2026-10-01"
```

Omit `date` to request the current day. The response may include temperature, humidity, heating demand and summary data, depending on Tado's API.

## 10. Inspect profile availability

```yaml
action: tado_x.list_schedule_profiles
data:
  entity_id: climate.living_room
```

The response includes `profiles`, `home_defaults`, `current`, `status` and `matching_profiles`. Use the room's **Refresh Schedule** button to update matching information when automatic schedule checks are disabled.

## Before using these examples

- Confirm the target room or home, especially with two homes containing overlapping numeric room IDs.
- Be aware that schedule writes and profile restores change **live Tado settings**.
- Monitor API quota sensors; repeated polling or bulk changes consume requests.
- Test with a noncritical room first and record its current settings.
