# Contributing to Tado X Enhanced

Thank you for your interest in improving **Tado X Enhanced**, an independently maintained Home Assistant integration derived from [exabird/ha-tado-x](https://github.com/exabird/ha-tado-x).

This guide describes how to report issues, suggest enhancements, and contribute code. The integration retains the Home Assistant domain `tado_x`.

## Reporting bugs and requesting features

Before opening an issue, search [existing issues](https://github.com/rleatherb/ha-tado-x-enhanced/issues) for a similar report. For bugs, please include:

- The installed Tado X Enhanced release and Home Assistant version.
- Whether one or multiple Tado homes are configured.
- The affected device or entity type, action name, and the steps needed to reproduce the problem.
- Expected versus actual behaviour, and relevant Home Assistant log messages.
- Whether the problem persists after restarting Home Assistant, if relevant.

For feature requests, describe the use case and how the proposed behaviour should work. Please open an issue before starting a substantial change to the integration's architecture, API handling, or stored data format.

> **Protect private information:** Never post passwords, access or refresh tokens, account identifiers, personal addresses, or unredacted API responses. Review logs and screenshots carefully before sharing them.

## Proposing code changes

1. Fork [rleatherb/ha-tado-x-enhanced](https://github.com/rleatherb/ha-tado-x-enhanced).
2. Create a dedicated branch for the change.
3. Keep the changes focused, with descriptive commits.
4. Test the change and describe the tests performed (and any tests you could not perform).
5. Open a pull request against the repository's main branch, explaining the problem, solution, and any compatibility implications.

GitHub Desktop can be used for cloning, branching, committing and publishing changes; command-line Git is not required.

## Development environment

You will need a Home Assistant test installation, a suitable Python development environment, and, for live integration tests, access to Tado X hardware and an account. Install the integration under:

```text
config/custom_components/tado_x/
```

Restart Home Assistant after changing integration Python files or its manifest. For diagnostics, you can temporarily enable:

```yaml
logger:
  default: warning
  logs:
    custom_components.tado_x: debug
```

Turn off verbose logging when no longer needed. Do not submit unredacted logs.

## Code and documentation conventions

- Follow Python's PEP 8 conventions and use type hints where appropriate.
- Keep asynchronous Home Assistant operations non-blocking.
- Preserve existing entity unique IDs, service/action names, and the `tado_x` domain unless a breaking change has been explicitly agreed.
- Keep API calls and error handling consistent with the existing client and coordinator patterns; avoid unnecessary polling or additional API usage.
- Update `services.yaml`, `strings.json`, and relevant `translations/*.json` entries when changing actions or user-visible text. Avoid unescaped curly braces in translated descriptions because Home Assistant may interpret them as formatting placeholders.
- Update the README, implementation documentation, and `CHANGELOG.md` when user-facing behaviour changes.
- Preserve the MIT licence and copyright notices, including `Copyright (c) 2026 Robin Leatherbarrow` and  `Copyright (c) 2025 Exabird`.

## Architecture and areas requiring particular care

The integration is built around `custom_components/tado_x/`. Relevant modules include:

| File | Responsibility |
| :--- | :--- |
| `__init__.py` | Integration setup and action registration |
| `api.py` | Tado X API requests |
| `coordinator.py` | Home and room data updates |
| `config_flow.py` | Configuration and options flows |
| `climate.py` | Room climate entities |
| `sensor.py`, `binary_sensor.py`, `select.py`, `button.py` | Home Assistant entities |
| `schedule_profiles.py` | Named room schedules and home-wide defaults |
| `services.yaml` | Action definitions and input selectors |
| `strings.json`, `translations/` | Localised user-facing text |

When applicable, test the following:

- **Multiple homes:** correct routing by home ID, including overlapping room IDs and home-specific options.
- **Schedules:** read/write operations, 24-hour coverage, Away configuration, profile saving/restoring, home-wide defaults, and custom profile creation/deletion.
- **Climate control:** manual overrides, timer termination, and return to scheduled control.
- **Hot water:** scheduled operation, Off, Away settings, and boosts.
- **Entities:** unique IDs, names, availability, restored entity IDs, and device association.
- **API usage:** polling frequency, quota reporting, authentication failures, rate limits, and transient network failures.
- **Compatibility:** existing Home Assistant installations and unchanged public action names.

Tests requiring real hardware should be identified as such. Do not claim that an untested change has been verified against the Tado service.

## Pull request checklist

- [ ] The change addresses a documented bug or clearly explained enhancement.
- [ ] Python syntax and relevant JSON/YAML files have been checked.
- [ ] Affected behaviour has been tested, or testing limitations are clearly stated.
- [ ] Multi-home behaviour and backward compatibility have been considered.
- [ ] Translations and documentation have been updated where needed.
- [ ] No credentials, private data, generated caches, or debug artefacts are included.

## Licence and attribution

Contributions are submitted under the repository's [MIT License](LICENSE). This project is derived from the original Tado X integration by Exabird. Please retain existing copyright and licence notices.

For questions or proposals, use the [GitHub issue tracker](https://github.com/rleatherb/ha-tado-x-enhanced/issues).

