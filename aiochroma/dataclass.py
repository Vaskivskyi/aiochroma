"""Dataclass module for AIOChroma"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Key:
    """Key class"""

    row: int
    column: int


@dataclass
class Color:
    """Color class"""

    r: int = 0
    g: int = 0
    b: int = 0

    def as_int(self):
        """Return single-int number"""

        return self.r + self.g * 256 + self.b * 65536

    def brigtness(self) -> int:
        """Return maximum brightness in single channel"""

        return max(self.r, self.g, self.b)

    def scale(self, scale: float | int) -> Color:
        """Return scaled color"""

        if type(scale) == float:
            return Color(
                round(self.r * scale), round(self.g * scale), round(self.b * scale)
            )
        elif type(scale) == int:
            return self.scale(scale / 255)
        else:
            raise ValueError(f"Unknown scale: `{scale}`")
