"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(C) Andirz Object Tuning Replacement Script for Sims 4
Homepage: https://andirz.itch.io/
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Licensed under CC-BY-NC-ND 4.0
Do not copy or use this code without the author's permission.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

class EmptyLogger:

    def emptyline(self): pass
    def dashline(self): pass
    def debug(self, text): pass
    def info(self, text): pass
    def warn(self, text): pass

    def error(self, message):
        raise RuntimeError(f"[ERROR] Object Tuning Replacement Script: {message}")


class SmartCoreIntegration:

    def __init__(self, data):
        self.data = data
        self.valid = self._validate_metadata()

    def _validate_metadata(self):
        if not getattr(self.data, "SCRIPT_CREATOR", None):
            return False
        if not getattr(self.data, "SCRIPT_NAME", None):
            return False
        if not getattr(self.data, "SCRIPT_VERSION", None):
            return False
        if not getattr(self.data, "REQUIRED_CORE_SCRIPT_VERSION", None):
            return False
        return True

    def is_logger_compatible(self):
        if not self.valid:
            return False

        try:
            from andirz_corescript.data import CORESCRIPT_VERSION
            from andirz_corescript.utils.version import version_string_to_tuple
            from andirz_corescript.utils.blocker import is_core_blocked
        except ImportError:
            return False

        try:
            installed_core_version = version_string_to_tuple(CORESCRIPT_VERSION)
        except Exception:
            return False

        if not isinstance(installed_core_version, tuple):
            return False

        if is_core_blocked():
            return False

        required_version_tuple = version_string_to_tuple(self.data.REQUIRED_CORE_SCRIPT_VERSION)
        if installed_core_version < required_version_tuple:
            return False

        return True


    def get_logger(self):
        if not self.is_logger_compatible():
            return EmptyLogger()
        try:
            from andirz_corescript.utils.logger import Logger
            return Logger(
                path=f"{self.data.SCRIPT_CREATOR}_{self.data.SCRIPT_NAME.replace(' ', '')}.log",
                title=f"{self.data.SCRIPT_CREATOR} {self.data.SCRIPT_NAME} Log v.{self.data.SCRIPT_VERSION}",
                mute=getattr(self.data, "LOG_ERRORS_ONLY", False)
            )
        except Exception as e:
            fallback_logger = EmptyLogger()
            fallback_logger.error(f"[{self.data.SCRIPT_NAME}] Failed to initialize the logger: {e}")
            return EmptyLogger()

