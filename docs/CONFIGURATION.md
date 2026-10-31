# Configuration

Each Tado home is configured as a separate Home Assistant integration entry. Use **Add integration** or **Add entry**, depending on the Home Assistant interface, and select the appropriate Tado home during setup.

Each configured Tado home has its own options under **Settings → Devices & services → Tado X → Configure**.

| Setting | Purpose | Version |
| :--- | :--- | :---: |
| Auto-Assist subscription | Sets subscription-related defaults and feature availability assumptions. |  |
| Main update interval | General integration polling, in seconds (configuration range: 30–3600). |  |
| Automatically check for schedule changes | Enable periodic Home/Away schedule comparisons. Defaults to on for Auto-Assist and off otherwise, unless explicitly set. | 1.0.0 |
| Schedule check interval | Separate schedule polling interval: 900–86400 seconds (15 minutes–24 hours); default 3600 seconds. | 1.0.0 |
| Weather | Enable weather data where available. |  |
| Mobile devices | Enable mobile presence/tracker data. |  |
| Air comfort | Enable air-comfort data. |  |
| Running times | Enable heating running-time data. |  |
| Flow temperature | Enable supported flow-temperature controls/data. |  |
| Hot water | Enable domestic hot-water functionality where supported. | 1.0.0 |


### API usage

It is important to ensure that usage does not exceed your allowance. There are several sensors associated with each Tado home that can be used to monitor this. If you have an Auto-Assist subscription, which is highly recommended in order to make best use of this integration, the default settings should allow you to keep within these limits, but if your system results in higher numbers of calls than are allowed it is possible to reduce this by removing access to calls that are less necessary, and/or **increasing** the main update interval (polling less frequently).

**API usage for schedules:** A complete automatic schedule check uses approximately **two API calls per room** (one Home schedule and one Away settings read). For 10 rooms, automatic hourly checks would use approximately **480 requests per day** for this feature alone. Automatic checks can therefore be disabled if required; updates per room can still be done manually if required by using the **Refresh Schedule** button that is enabled for each room separately.



## Polling and quotas

The main coordinator interval and the independent schedule-check interval are configured **per home**. Main polling supports 30–3,600 seconds; schedule checking supports 900–86,400 seconds and defaults to 3,600 seconds. Automatic schedule checking defaults to enabled with Auto-Assist and disabled without it, unless explicitly configured. Increasing an interval reduces polling frequency.

Schedule checking requires approximately two API reads per room per check. For 10 rooms checked hourly, that is about 480 requests/day, **in addition to** normal polling and other operations. For accounts with multiple homes, do not assume separate per-home quotas: inspect the server-reported API quota sensors. Schedule profiles and the room **Refresh Schedule** button can still be used with automatic schedule checking disabled.

## Multiple homes and compatibility

Each home has its own coordinator, configuration options and schedule-profile storage. Home-level actions require a **Tado X Home device** target when more than one home is configured; room actions resolve the home from the climate entity. The integration uses domain `tado_x` and cannot coexist with another integration using the same domain. See [README.md](../README.md) for the replacement-installation precautions.

## Troubleshooting

If a feature is unavailable, confirm that the corresponding optional dataset is enabled and supported by your Tado equipment/account. Check Home Assistant logs for authentication, rate-limit and API errors. Before sharing diagnostics, redact tokens, account details, addresses and other personal information. A successful YAML configuration check alone does not verify Tado cloud functionality.
