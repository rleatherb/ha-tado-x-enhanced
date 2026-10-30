# Schedules and Schedule Profiles

**[Readme](../README.md)** · [Report an issue](https://github.com/rleatherb/ha-tado-x-enhanced/issues) · [Releases](https://github.com/rleatherb/ha-tado-x-enhanced/releases)

The Tado app allows per-room heating schedules to be defined, and also the heating behaviour specified when Away mode is active. Configuration of these settings is a major task that all Tado users need to undertake, and once set up the temperature control is automatically managed by the Tado system. The app allows a single schedule to be set for each room, which is defined for each day of the week separately.

- **Schedules may be created and edited in the Tado app, then saved and restored in Home Assistant.** The integration also exposes `get_schedule` and `set_schedule` actions for direct Home schedule reads and writes. The latter requires a complete, validated 24-hour day schedule.

## Why a single schedule is not enough

In use, a schedule that is appropriate for certain times and applications is frequently found to be unsuitable for others. While it is possible to edit the Tado heating schedule via their app, this is time consuming and there is no way to revert to previous settings once the requirements change.

Some of the situations that frequently arise and would benefit from having multiple schedules are given below:

- **Change in season.** The heating requirements in summer differ from those in winter (and possibly spring and autumn). In winter you are likely to want rooms to be heated each day, perhaps set to 18°C overnight and 21°C during the day. However, for heating in summer you probably only want to heat the rooms if there was an exceptional cold spell. One way of doing this would be to create a new schedule, perhaps setting a fallback of 17°C overnight and 18°C during the day, but of course the choices will depend on your situation.

- **Rooms used occasionally.** A spare bedroom does not need to be heated when not occupied, but some background level of heat is beneficial to prevent damp. Switching the room off via the Tado app results in a threshold of 5°C, which is not recommended for extended periods. A better solution is a separate schedule that can be applied when the room is not being used, but switching to a different schedule when that room is occupied. This also means that you are free to select a temperature that appropriate to the room in question.

- **Variable working patterns.** It is often the case that there are times when certain rooms are used during the day, perhaps when working at home or on when on leave, but other times when there is no need to heat during the day. If your working pattern is not regular, this is hard to achieve with a single fixed schedule. Having a schedule for "working from home" rather than "working at the office" would allow this situation to be catered for.

## How is heating schedule support supplied via this integration?

The schedules set up via the Tado app are used as the primary source for this integration. The Tado app remains a convenient schedule editor, but Home Assistant also provides direct schedule actions. The integration allows schedules to be saved and reloaded, meaning that you can replace the currently active schedules with ones that you define yourself. Unlimited named profiles are allowed, but there are pre-built scenarios that set up to address the main example use cases that were given above. In all cases, the schedules are defined for each room individually.

### Pre-defined schedule profile names

The following 4 schedule profiles are already known about within this implementation. Remember that these profiles exist separately for each room in your Tado home.

- **Normal.** This is the standard heating schedule that you are probably currently using already. The main use of this is to provide heating that is appropriate under normal circumstances. The Normal profile is a special case for the integration, and when you first start up Home Assistant after installing **Tado X Enhanced**, the integration will read your schedules for each room and store them for you as **Normal**; this will only be done once for any room that does not have a stored Normal schedule. What this means is that any further schedule changes you make using the Tado app can then be easily reverted back to your stored Normal settings. Also, if you want to update your Normal schedule then that is also easily done.

- **Not in use.** This is a profile that is provided for rooms that are not being actively used, such as a spare bedroom. Select this profile when the room is out of regular use, then restore one of the others when you need it back in use.

- **Eco.** This profile is recommended when you need reduced heating, perhaps because of occasional use or because you want to have lower settings during summer.

- **Alternative.** This profile can be used to define a further heating schedule, with the application being up to you. Possible uses might be when working from home, when guests visit, or for an additional schedule to deal with changes of season.

### How are these schedule profiles used?

Profiles are saved and restored on a per-room basis. On the room device page, under Configuration, you will see the selectors **Restore schedule profile** and **Save schedule profile**.

- **Restore schedule profile.** Use this to load one of the named profiles that are available. This loads just the profile that is associated with that room.

- **Save schedule profile.** Use this to save the current heating schedule, as set up in the Tado app, to one of the named profiles that are listed.

Each of these selectors will show how the current schedule, set via the Tado app, matches the named schedule profiles. If one of the named schedule profiles matches the current settings in the app, that named profile is shown. If the schedule set via the Tado app differs from any of your saved profiles, this is shown as **Custom** to indicate that it is different. Restoring one of the named profiles will update this, or alternatively you can save the current settings to update a stored profile.

**Please note:** To avoid using too many API calls, this integration only polls the Tado app to read its schedules periodically (the frequency of this can be configured for each Tado home). However, each room has a **Refresh Schedule** button that can be used to force the schedule information to be re-synchronised at any time.

### What settings are used if you load a profile that has not been explicitly stored?

When you first run this integration, your current heating schedules as set up in the Tado app will be stored as the default Normal profile for each room. However, you will still be able to select one of the other pre-defined profile names, even though there is no stored setting as yet. What happens in this situation is that a default profile will be loaded.

Unlike the standard profiles, which are room specific, these defaults are for the entire home.

| Profile | Home schedule defaults ("factory setting") | Away defaults |
| :--- | :--- | :--- |
| Normal | Every day: 00:00–07:30 18°C; 07:30–22:00 20°C; 22:00–24:00 18°C | ON, 17°C, BALANCE |
| Alternative | Mon–Fri: 00:00–06:30 18°C; 06:30–08:30 20°C; 08:30–16:30 18°C; 16:30–22:00 20°C; 22:00–24:00 18°C. Weekend same as Normal | ON, 17°C, BALANCE |
| Eco | Every day: 00:00–07:30 17°C; 07:30–22:00 18°C; 22:00–24:00 17°C | ON, 16°C, BALANCE |
| Not in use | Every day: 00:00–24:00 14°C | ON, 14°C, BALANCE |

### Customising the profile defaults

The default profile settings can be changed from the ones shown above. This is useful if, for example, you would prefer that the "Not in use" profile was set to 12°C rather than 14°C. For example, to do this would involve the following steps:

1. Edit the schedule for a room on the Tado app so that it fits your requirements. For example, you might wish to change the temperature to 12°C both for the Home schedule and the Away settings.

2. Navigate to **Developer Tools → Actions** in Home Assistant.

3. Select the action `tado_x.save_schedule_profile_default`

4. Choose the climate entity for the room that holds the settings you want to save, and enter the name of the profile that you wish to set the defaults for.

5. Click **Perform action**. This will save the room’s current Home/Away settings as the selected **home-wide default**; it will not change any other room’s live schedule.

Please note that changing one of the defaults does not alter the settings for any room that already uses these. In this situation you would need to reload the schedule for any other rooms that are using it.

#### Restoring the "factory setting" defaults

If you have customised the default profile settings and wish to revert to the standard "factory setting" for one of the 4 standard profile defaults, as set out above, this can be done using the `tado_x.reset_schedule_default` action.

### Resetting a room to a default schedule profile

It is possible to load the default schedule profile for a specific room. For example, if you have customised the Eco profile for the 'office' room, you can reset this to the Eco profile default as follows.

1. Navigate to **Developer Tools → Actions** in Home Assistant.


2. Select the action `tado_x.restore_schedule_profile_default`

3. Choose the climate entity for the **room to receive the default schedule**, and enter the profile name. This applies the home-wide default to the live room schedule; it does not change the stored home-wide default.

4. Click **Perform action**. This will apply the selected home-wide default to the room.

### What if 4 different profiles are not enough?

The four pre-defined profiles may cover many requirements, but the **Tado X Enhanced** implementation allows further extension, and (in principle) any number of profile names are allowed.

The `tado_x.create_schedule_profile` action is used to create a new home-specific profile. For example, to create a new profile called "Extra":

```yaml
action: tado_x.create_schedule_profile
data:
  profile: Extra
  # device_id: YOUR_TADO_HOME_DEVICE_ID  # required for multiple homes
```

The new name is scoped to the selected home, and "Extra" will now appear within the **Restore schedule profile** and **Save schedule profile** selectors.

You can discover what profiles are saved for any room using the `tado_x.list_schedule_profiles` action. For example:

```yaml
action: tado_x.list_schedule_profiles
data:
  entity_id: climate.utility
```

An illustrative response (actual saved/customised states will vary):

```yaml
profiles:
  - name: Normal
    saved: true
  - name: Alternative
    saved: false
  - name: Eco
    saved: true
  - name: Not in use
    saved: true
  - name: Extra
    saved: true
home_defaults:
  - name: Normal
    customized: true
  - name: Alternative
    customized: false
  - name: Eco
    customized: false
  - name: Not in use
    customized: true
  - name: Extra
    customized: true
current: Extra
status: Matched
matching_profiles:
  - Extra

```

It is also possible to delete a **custom home-wide profile name** using `tado_x.delete_schedule_profile`. This removes that profile class and its stored room/default data for the selected home, not just one room. This command will not allow you to delete one of the predefined profiles (Normal, Alternative, Eco, Not in use).

```yaml
action: tado_x.delete_schedule_profile
data:
  profile: Extra
  # device_id: YOUR_TADO_HOME_DEVICE_ID  # required for multiple homes
```

When you create a new schedule profile, the current defaults for the Normal profile are used as the defaults for the new profile name. If you wish to update the defaults for the newly created profile, this can be done using the `tado_x.save_schedule_profile_default` action.

By using custom profiles it is possible to have any number of heating schedules that can be saved or restored as needed for your particular application.

## Getting more information about the Tado heating schedules

Although saving and restoring schedule profiles is the easiest way to modify the heating schedules, it is also possible to read and write schedules direct, with actions that will do this. You can test these actions, and view the responses, in **Developer Tools → Actions**.

#### Get schedule

To get the schedule for a specific room, select that room, for example:

```yaml
action: tado_x.get_schedule
data:
  entity_id: climate.office
```

The response contains the schedule information returned by the Tado API for that room. Exact response fields depend on the API.

#### Set schedule

To set the schedule for a specific room using the `set_schedule` action, select that room, choose the Day type, and provide JSON string for the schedule field.

The schedule field must be a JSON-formatted string containing schedule blocks, each specifying `dayType`, `start`, `end`, `setting`, `power` and `temperature`. For example:

```json
[
  {
    "dayType": "MONDAY",
    "start": "00:00",
    "end": "07:00",
    "setting": {
      "power": "ON",
      "temperature": {"value": 18.0}
    }
  },
  {
    "dayType": "MONDAY",
    "start": "07:00",
    "end": "24:00",
    "setting": {
      "power": "ON",
      "temperature": {"value": 21.0}
    }
  }
]
```

Select `day_type: MONDAY` in the action as well. Every block must match that day type; blocks must cover 00:00–24:00 contiguously without gaps or overlaps. An `ON` block requires a numeric `setting.temperature.value`. The schedule input is a **JSON string**, not a YAML list.

#### Get away schedule

Specify the Tado X room to query. For example:

```yaml
action: tado_x.get_away_schedule
data:
  entity_id: climate.office
```

The response then provides information about the settings:

```
mode: 'ON'
awayTemperatureCelsius: 14
preheatingLevel: BALANCE
```

#### Set away schedule

Specify the Tado X room, the away mode (On or Off), and when away mode is On, the away temperature. It is also possible to specify the Tado preheating level (Off, Eco, Balance, Comfort). For example:

```yaml
action: tado_x.set_away_schedule
data:
  entity_id: climate.office
  mode: 'ON'
  away_temperature: 12
  preheating_level: BALANCE
```

#### Get holiday mode

The holiday mode is specific to each Tado X home. If you have more than one it is necessary to specify which home you need the information for; if there is only one home then you do not need to set the home to use.

```yaml
action: tado_x.get_holiday_mode
data: {}
```

#### Set holiday mode

The holiday mode is specific to each Tado X home. If you have more than one it is necessary to specify which home you need the information for; if there is only one home then you do not need to set the home to use.

Set whether holiday mode is on or off, the start date-time (optional), and the end date-time (optional). For example:

```yaml
action: tado_x.set_holiday_mode
data:
  enabled: true
  start_date: '2026-12-20T08:00:00Z'
  end_date: '2026-12-30T08:00:00Z'
```

## Getting historical information about heating within a room

Home Assistant provides historical information about sensors, but in addition, Tado retains a significant wealth of information about the heating that was applied. You can query this via `get_day_report` action. This can either, if no date is specified, return data about the current day, or can be set to retrieve detailed information about any day in the past for which data is available.

Select the room that you require information for, optionally give a date, and the response returns a comprehensive analysis. The easiest way to test this is using the Home Assistant Developer Tools → Actions, and fill in the required settings. For example:

```yaml
action: tado_x.get_day_report
data:
  entity_id: climate.office
```

Data returned includes temperature, humidity, stripes (which are heating data), callfForHeat (the times associated with different heat settings), weather, and a summary of average/min/max temperatures, average humidity, and the number of heating hours.


## Profile actions and home targeting

The room device provides **Restore schedule profile**, **Save schedule profile** and **Refresh Schedule**. The device-page selectors for saving/restoring **home-wide defaults** were removed; use `tado_x.save_schedule_profile_default` and `tado_x.restore_schedule_profile_default` in Developer Tools → Actions instead.

Room-specific actions require a room `entity_id` (a Tado X climate entity). Home-wide actions (`create_schedule_profile`, `delete_schedule_profile`, `reset_schedule_default`) accept an optional **Tado X Home** `device_id`; supply it when multiple homes are configured. Profile names are entered as free text and must already exist before saving or restoring. The four built-in names cannot be deleted. `reset_schedule_default` accepts only a built-in profile name.

The room profile's current selection can display **Custom** when its live Home/Away schedule matches no stored effective profile. It can also be unavailable if schedule reads fail; **Custom** is not a profile that can be restored. For details of validation and partial-write recovery, see [ARCHITECTURE.md](ARCHITECTURE.md).
