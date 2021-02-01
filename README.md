# LED-Pi Custom Component for Home Assistant

[![](https://img.shields.io/github/license/muhlba91/ledpi-homeassistant-integration?style=for-the-badge)](LICENSE)
[![](https://img.shields.io/github/workflow/status/muhlba91/ledpi-homeassistant-integration/Python%20package?style=for-the-badge)](https://github.com/muhlba91/ledpi-homeassistant-integration/actions)
<a href="https://www.buymeacoffee.com/muhlba91" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="28" width="150"></a>

This component creates an integration that provides a **light entity and sensors** to control
the [LED-Pi Controller](https://github.com/muhlba91/ledpi-controller) exposed through a simple API found at
**[LED-Pi Controller Flask API](https://github.com/muhlba91/ledpi-controller-api)** via Home Assistant.

---

## Installation

I recommend installation through [HACS](https://hacs.xyz/):

- Ensure HACS is installed.
- Add this repository (`https://github.com/muhlba91/ledpi-homeassistant-integration.git`) as a custom repository with
  the category *Integration*.
- Search for and install the "LED-Pi - Raspberry Pi WS2801 LED Controller" integration.

## Configuration

Add it from the **Integrations menu**, set the desired configuration, and you're good to go.

Once configured, the integration **creates a light entity and sensors** for:

| Entity | Description |
|--------|-------------|
| Light | Manage the light (see *Services* below). |
| Sensor: Brightness | The current brightness of the light. |
| Sensor: LEDs | The number of LEDs on the strip. |
| Sensor: RGB Hex | The Hex representation of the current light color. |
| Sensor: RGB Name | The web color name of the current light color. |

Additionally, it makes **additional services** available to control the light:

- Service: **`rgb_color`**
    - Set's the RGB color (tuple).
    - Additional Fields:
        - `rgb_color`: the color to set in the RGB format
- Service: **`brightness`**
    - Set's the brightness of the LEDs.
    - Additional Fields:
        - `brightness`: the brightness to set between 0 and 1

---

## Development

The project uses [poetry](https://poetry.eustace.io/) and to install all dependencies and the build environment, run:

```bash
$ pip install poetry
$ poetry install
```

### Testing

1) Install all dependencies as shown above.
2) Run `pytest` by:

```bash
$ poetry run pytest
# or
$ pytest
```

### Linting and Code Style

The project uses [flakehell](https://github.com/life4/flakehell) as a wrapper for flake8,
and [black](https://github.com/psf/black) for automated code style fixing, also
using [pre-commit](https://pre-commit.com/).

1) Install all dependencies as shown above.
2) (Optional) Install pre-commit hooks:

```bash
$ poetry run pre-commit install
```

3) Run black:

```bash
$ poetry run black .
```

4) Run flakehell:

```bash
$ poetry run flakehell lint
```

### Commit Message

This project follows [Conventional Commits](https://www.conventionalcommits.org/), and your commit message must also
adhere to the additional rules outlined in `.conform.yaml`.

---

## Release

To draft a release, use [standard-version](https://github.com/conventional-changelog/standard-version):

```bash
$ standard-version
# alternatively
$ npx standard-version
```

Finally, push with tags:

```bash
$ git push --follow-tags
```

---

## Contributions

Please feel free to contribute, be it with Issues or Pull Requests! Please read
the [Contribution guidelines](CONTRIBUTING.md)

## Supporting

If you enjoy the application and want to support my efforts, please feel free to buy me a coffe. :)

<a href="https://www.buymeacoffee.com/muhlba91" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="75" width="300"></a>
