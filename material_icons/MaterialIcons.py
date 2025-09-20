import os
from enum import Enum
from typing import Dict, Tuple

from cairosvg import svg2png


class IconStyle(Enum):
    OUTLINED = "outlined"
    ROUND = "round"
    SHARP = "sharp"


class MaterialIcons:
    def __init__(self):
        self.cache: Dict[Tuple[str, int, str, str], bytes] = {}
        self.icon_dir = os.path.join(os.path.dirname(__file__), "icons")

    def get(
        self,
        name: str,
        size: int = 24,
        color: str = "#000000",
        style: IconStyle = IconStyle.OUTLINED
    ) -> bytes:
        """
        Load a Material Design icon as PNG bytes.

        Args:
            name:  Icon filename without .svg (e.g. "close", "check_box").
            size:  Target size in pixels (width & height).
            color: Fill color, replaces "currentColor" in the SVG (default black).
            style: IconStyle enum (OUTLINED, ROUND, or SHARP).

        Returns:
            PNG image as raw bytes.
        """
        key = (name, size, color, style.value)
        if key in self.cache:
            return self.cache[key]

        path = os.path.join(self.icon_dir, style.value, f"{name}.svg")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Icon '{name}' with style '{style.value}' not found at {path}")

        with open(path, "r", encoding="utf-8") as f:
            svg = f.read()

        svg = svg.replace("currentColor", color)
        png_bytes = svg2png(
            bytestring=svg.encode("utf-8"),
            output_width=size,
            output_height=size
        )

        self.cache[key] = png_bytes

        return png_bytes
