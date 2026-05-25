"""Compatibility shim for legacy `import config` statements.

Re-export settings from the stock prediction package so modules can be
executed from the repository root without import errors.
"""

from stock_prediction_project.config import *  # noqa: F403
