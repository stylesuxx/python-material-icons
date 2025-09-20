# Python Material Icons

> Use Google's Material Icons in your Python applications.

This library provides access to the full set of [Material Icons](https://fonts.google.com/icons) in three distinct styles: **outlined**, **round**, and **sharp**.
Icons are converted from SVG to PNG at runtime using [CairoSVG](https://cairosvg.org/), with automatic caching based on icon name, size, color, and style.

When loading an icon, it will return a PNG **byte stream** that you can use in any way you see fit.

## Installation

```bash
pip install material-icons
```

## Usage

With Pillow:
```python
from material_icons import MaterialIcons, IconStyle
from PIL import Image
import io

# Load an icon as PNG bytes
icons = MaterialIcons()
png_bytes = icons.get("cancel", size=48, color="#ff0000", style=IconStyle.ROUND)

# Use with Pillow
image = Image.open(io.BytesIO(png_bytes))
image.show()
```

With pygame:
```python
import pygame
from material_icons import MaterialIcons, IconStyle

icons = MaterialIcons()

# Load an icon as PNG bytes
png_bytes = icons.get("cancel", size=48, color="#ff0000", style=IconStyle.SHARP)

# Use with pygame
surface = pygame.image.load(io.BytesIO(png_bytes))
```

### Parameters
- **name** *(str)*: The Material icon name, e.g. `"cancel"`, `"check_box"`, `"signal_cellular_4_bar"`.
- **size** *(int, default=24)*: The output icon size in pixels (square).
- **color** *(str, default="#000000")*: The icon color as a hex string.
- **style** *(IconStyle, default=IconStyle.OUTLINED)*: The icon style - `IconStyle.OUTLINED`, `IconStyle.ROUND`, or `IconStyle.SHARP`.

### Icon Styles

Material Icons come in three distinct styles:

- **Outlined** (`IconStyle.OUTLINED`): Clean, minimal outlined icons (default)
- **Round** (`IconStyle.ROUND`): Rounded corners and edges for a softer look
- **Sharp** (`IconStyle.SHARP`): Angular, sharp-edged icons for a more geometric feel

```python
# Get the same icon in different styles
outlined = icons.get("home", style=IconStyle.OUTLINED)
round_icon = icons.get("home", style=IconStyle.ROUND)
sharp = icons.get("home", style=IconStyle.SHARP)
```

### Caching
Icons are cached automatically based on `(name, size, color, style)`.
Subsequent calls with the same parameters return instantly without re-rendering.

## Examples
A pygame icon gallery example is available in the examples directory, install pygame and run it like so:

```bash
python examples/pygame-gallery.py
```

## Contribution

We welcome contributions!

- Open issues for bugs or feature requests
- Submit pull requests to improve the code, documentation, or packaging.
- The icon set is fetched automatically in the build pipeline, so you don't need to commit icons to the repository.


## Distribution
To build and upload to pypi, first update version `pyproject.toml` then run run:

```
python -m build
python -m twine upload --repository testpypi dist/*
python -m twine upload dist/*
```