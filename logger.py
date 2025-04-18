"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(C) Andirz Object Tuning Replacement Script for Sims 4
Homepage: https://andirz.itch.io/
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Licensed under CC-BY-NC-ND 4.0
Do not copy or use this code without the author's permission.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import os

class Logger:

    def __init__(self, filename='ErrorLog.log', title=None, force_simple_log=False, debug=False):
        self._log_file = filename
        self._log_title = title
        self._header = None
        self._debug = debug
        self._logger = None
        self._initialized = False
        self._default_path = self.get_log_path()
        self._use_smart_logger = self._check_smart_logger() if self._smartcore_compatible() and not force_simple_log else False

    def _check_smart_logger(self):
        try:
            from andirz_corescript import logging_mode_on
            return logging_mode_on()
        except Exception:
            return False

    def _smartcore_compatible(self):
        error_text = "Smart Core logger could not be initialized. Falling back to simple text logging."
        try:
            from andirz_corescript import CORESCRIPT_VERSION
            from andirz_corescript.utils.version import version_string_to_tuple
            compatible = version_string_to_tuple(CORESCRIPT_VERSION) >= (1, 16, 0)
            if not compatible:
                self._header = error_text
            return compatible
        except Exception:
            self._header = error_text
            return False

    def get_log_path(self):
        default_path = os.path.join(os.path.expanduser("~"), "Documents", "Electronic Arts", "The Sims 4", self._log_file)
        try:
            from andirz_corescript.utils.system import get_full_path
            return get_full_path(self._log_file)
        except Exception:
            pass
        try:
            from lot51_core.utils.paths import get_game_dir
            root = get_game_dir()
            return os.path.join(root, self._log_file)
        except Exception:
            pass
        return default_path

    def _start(self):
        if self._initialized:
            return
        self._initialized = True
        if self._use_smart_logger:
            from andirz_corescript.utils.logger import Logger as SmartLogger
            self._header = "Smart Core Script was detected and its logger was successfully initialized."
            self._logger = SmartLogger(path=self._log_file, title=f"{self._log_title}\n{self._header}")
            self._logger.dashline()
        else:
            os.makedirs(os.path.dirname(self._default_path), exist_ok=True)
            with open(self._default_path, "w", encoding="utf-8") as f:
                f.write(f"{self._log_title}\n\n")
                if self._header:
                    f.write(f"[INFO] {self._header}\n\n")

    def _log(self, text, level="INFO"):
        if level != "ERROR" and not self._debug:
            return
        self._start()
        if self._use_smart_logger and self._logger:
            getattr(self._logger, level.lower())(text)
        else:
            with open(self._default_path, "a", encoding="utf-8") as f:
                f.write(f"[{level}] {text}\n")

    def info(self, text): self._log(text, level="INFO")
    def debug(self, text): self._log(text, level="DEBUG")
    def error(self, text): self._log(text, level="ERROR")

    def empty(self):
        if not self._debug:
            return
        self._start()
        if self._use_smart_logger and self._logger:
            self._logger.emptyline()
        else:
            with open(self._default_path, "a", encoding="utf-8") as f:
                f.write("\n")

    def line(self):
        if not self._debug:
            return
        self._start()
        if self._use_smart_logger and self._logger:
            self._logger.dashline()
        else:
            with open(self._default_path, "a", encoding="utf-8") as f:
                f.write("-" * 80 + "\n")
