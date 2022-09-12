"""Library init"""

from .aiochroma import AIOChroma
from .connection import Connection
from .dataclass import Color, Key
from .error import (
    ChromaError,
    ChromaResultError,
    ChromaUnknownLayout,
    ChromaUnknownTarget,
    ChromaWrongParameter,
)
