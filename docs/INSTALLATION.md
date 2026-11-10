# Installation and migration

Tado X Enhanced is an independently maintained replacement for [Exabird's Tado X integration](https://github.com/exabird/ha-tado-x). Both use the Home Assistant integration domain `tado_x` and install under `/config/custom_components/tado_x`. **They cannot be installed as two separate integrations at the same time.**

## Read this before replacing an existing integration

> **WARNING — POSSIBLE PERMANENT LOSS OF CONFIGURATION, DEVICES AND ENTITIES**
>
> **Create a complete Home Assistant backup before beginning. Verify that the backup includes your configuration, `.storage` and custom integrations, and that you know how to restore it.** A virtual-machine snapshot alone is not a substitute for a Home Assistant backup on a real installation. Record important entity IDs, renamed entities, device IDs, home configuration and automation dependencies. Stop if you cannot restore the system.
>
> In Home Assistant 2026.11, Marketplace **explicitly warns** that removing the original integration deletes its entry, devices and entities and cannot be undone. **Take these warnings literally. Do not assume that identities will survive.**

The maintainer repeated a migration twice on a **disposable VirtualBox Home Assistant 2026.11 installation**, starting with the original Tado X and then installing Enhanced. In those tests **four recorded device IDs and five deliberately renamed entity IDs survived**, despite Marketplace's deletion warnings. The original integration required **new setup and Tado authorisation** after replacement. Some old French-style entity IDs (`sensor.vanne_...`) remained, which is desirable for existing references. **These observations are limited test evidence, not a promise that Marketplace preserves registries or configuration on other systems.** The original configuration entry should be regarded as deleted, not preserved. The tests did not establish compatibility with every older version, multi-home migration or every Home Assistant release.

If the integration manages important heating automations, arrange a safe time for replacement and confirm heating operation afterwards. If you are unwilling to risk registry loss, **do not perform the Marketplace uninstall**; retain the working integration until a safe alternative has been established.

## A. Fresh installation — Home Assistant 2026.11 and later (Marketplace)

1. Open **Settings → Marketplace**. Open the top-right **⋮** menu and choose **Custom repositories**.
2. Select **Add from link** and enter `https://github.com/rleatherb/ha-tado-x-enhanced`.
3. Return to Marketplace, open **Tado X Enhanced** and select **Install**; confirm installation.
4. Follow the restart/setup prompts displayed by your Home Assistant version. Open **Tado X Enhanced → Set up** (or **Settings → Devices & services → Add integration**) and complete Tado authentication and home selection.
5. Configure subscription status and polling options, then check devices, room entities and Tado API quota sensors.

These are the steps for a **fresh installation only**, not for replacing the original integration.

## B. Replacing original Tado X — Home Assistant 2026.11 and later (Marketplace)

**Only proceed after the backup and recovery precautions above. This procedure intentionally removes the original integration and requires reconfiguration.** The two destructive confirmation dialogs below are expected; their wording must not be dismissed as harmless.

1. Take and verify a **complete Home Assistant backup**. Record important entity and device IDs, Tado homes and existing options. If using a test VM, take a snapshot **as well as** the Home Assistant backup.
2. In **Settings → Marketplace → ⋮ → Custom repositories → Add from link**, add `https://github.com/rleatherb/ha-tado-x-enhanced`. Return to Marketplace. The original **Tado X** should show as installed and **Tado X Enhanced** as available.
3. Open the **⋮** menu on the **original Tado X** entry and choose **Uninstall**.
4. Marketplace displays **“Tado X is in use”** and warns that the installed files are needed for its configured entries. It offers **Cancel**, **View integration** and **Delete and uninstall**. **This is a genuine deletion warning.** Stop here if you are not prepared to restore your backup or recreate entries.
5. If proceeding, select **Delete and uninstall**. A second dialog, **“Delete and uninstall Tado X?”**, states that the entry, devices and entities will be deleted and that this cannot be undone. **This is a second explicit destructive confirmation, not a harmless repository switch.** Only select **Delete and uninstall** if you accept that loss may occur.
6. Back in Marketplace, open **Tado X Enhanced → Install**, confirm, then select **Restart Home Assistant** and complete the restart.
7. After restart, open **Marketplace → Tado X Enhanced → Set up**. Select **Submit** to begin authentication, authorise Tado X and select **Submit** to complete setup. Recreate/configure any necessary home entries.
8. **Verify before relying on the installation:** compare the recorded device IDs and entity IDs; check user-renamed entities, automations, dashboards, all configured homes, climate operation, schedules, hot water (where available), logs and quota/polling settings. Check that Marketplace now manages Enhanced, not the original repository.
9. **If important identities or configuration are missing, stop and restore your backup** rather than assuming that the deleted entries can be recovered by reinstalling files. Keep the backup until all checks pass.

**Observed result, not guarantee:** in two disposable VirtualBox trials, the four checked device IDs and five checked renamed entity IDs survived, and old French-style IDs remained. These results **do not contradict the Marketplace warning**: registry survival is not guaranteed, and a fresh integration setup and authorisation were required.

## C. Fresh installation — Home Assistant 2026.10 or earlier (HACS)

1. Install [HACS](https://www.hacs.xyz/) if necessary.
2. In HACS, open **Custom repositories**, add `https://github.com/rleatherb/ha-tado-x-enhanced`, and select type **Integration**.
3. Open **Tado X Enhanced** in HACS and select **Download**.
4. Restart Home Assistant, then use **Settings → Devices & services → Add integration** to configure Tado X Enhanced and authenticate.
5. Review the subscription, polling and API quota settings.

This legacy procedure applies to older Home Assistant/HACS installations; exact labels may differ.

## D. Replacing original Tado X — Home Assistant 2026.10 or earlier (HACS)

**Back up and verify recovery first.** The earlier HACS handover was tested on a separate installation but cannot guarantee identity preservation on every system. It differs materially from the Marketplace procedure.

1. Register the Enhanced repository in HACS as a custom **Integration** repository.
2. In the original **Tado X** HACS repository entry, choose **Remove**. For the **Integration is configured** warning, the previously tested HACS workflow used **IGNORE** followed by **REMOVE**. **Do not navigate to Settings → Devices & services and delete the configured Tado homes as part of this HACS procedure.**
3. Before restarting, download **Tado X Enhanced** from HACS and confirm it installs to `/config/custom_components/tado_x` and shows **Pending restart**. If the download fails, restore the previous working files or your backup before restarting.
4. Restart Home Assistant and verify all configured homes, entity IDs, devices, options and automations. Confirm Enhanced is the repository managing updates.

**Do not use the HACS IGNORE/REMOVE instructions for Marketplace.** Marketplace has a different, explicitly destructive deletion flow.

## E. Manual installation and recovery

For advanced users, the integration files live under `/config/custom_components/tado_x`. Manual file replacement may be useful for recovery, but **does not establish correct Marketplace/HACS repository ownership**; the old repository could subsequently overwrite the replacement. Preserve a verified backup and do not assume that replacing files restores deleted Home Assistant configuration entries or entity registry records. Prefer restoring the complete Home Assistant backup when migration has removed important configuration.

## After installation: subscription and schedule-profile status

The default main update interval without Auto-Assist is **2700 seconds (45 minutes)**. Holiday Mode periodic polling defaults to **off without Auto-Assist** and **on with Auto-Assist** when no preference has been saved; an existing explicit preference is preserved. Initial/manual Holiday Mode reads and relevant boundary refreshes remain available regardless of this option.

Schedule-profile comparison polling is independent and defaults to **off without Auto-Assist**, **on with Auto-Assist**, unless explicitly configured. When automatic schedule checking is off, newly captured `Normal` profiles may initially show **Custom** until a room's **Refresh schedule** button is pressed. Automatic initial comparison occurs when schedule polling is enabled. Manual refresh can use additional Tado API requests; consider the account quota before refreshing many rooms.

If a new Tado room is added while Home Assistant is running, **reload the integration** to register the room and initialise its `Normal` profile. Dynamic room/entity registration is not supported.

## Reporting migration problems

If you encounter a different outcome, include the Home Assistant version, original Tado X version, installation method, which identities were retained or lost, and redacted logs in a [GitHub issue](https://github.com/rleatherb/ha-tado-x-enhanced/issues). **Never share access tokens, authentication codes, addresses or unredacted backups.**
