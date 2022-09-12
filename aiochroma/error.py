"""Error module"""

from __future__ import annotations

from typing import Any, Optional


class ChromaError(Exception):
    """Base class for errors in AIOChroma library"""

    def __init__(
        self, *args: Any, message: Optional[str] = None, **_kwargs: Any
    ) -> None:
        """Initialise base error"""

        super().__init__(*args, message)


class ChromaUnknownLayout(ChromaError):
    """Unknown layout"""


class ChromaResultError(ChromaError):
    """Result error on the request"""


class ChromaUnknownTarget(ChromaError):
    """Unknown target"""


class ChromaWrongParameter(ChromaError):
    """Wrong parameter"""
