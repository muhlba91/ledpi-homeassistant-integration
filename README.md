# LED-Pi Custom Component for Home Assistant

[![](https://img.shields.io/github/license/muhlba91/ledpi-homeassistant-integration?style=for-the-badge)](LICENSE)
[![](https://img.shields.io/github/workflow/status/muhlba91/ledpi-homeassistant-integration/Python%20package?style=for-the-badge)](https://github.com/muhlba91/ledpi-homeassistant-integration/actions)

This component creates an integration that provides a **light entity and sensors** to control
the [LED-Pi Controller](https://github.com/muhlba91/ledpi-controller) via Home Assistant.

---

## Installation

I recommend installation through [HACS](https://hacs.xyz/):

- Ensure HACS is installed.
- Add this repository (`https://github.com/muhlba91/ledpi-homeassistant-integration.git`) as a custom repository with
  the category *Integration*.
- Search for and install the "Raspberry Pi WS2801 LED Controller" integration.

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

## Running Tests

To run the test suite create a virtualenv (I recommend checking out [pyenv](https://github.com/pyenv/pyenv)
and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) for this) and install the test requirements.

```bash
$ pip install -r requirements.test.txt
```

After the test dependencies are installed you can simply invoke `pytest` to run the test suite.

```bash
$ pytest
```

---

## Contributions

Please feel free to contribute, be it with Issues or Pull Requests! Please read the [Contribution guidelines](CONTRIBUTING.md)
