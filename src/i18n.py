import ctypes
import gettext
import locale
import platform
from typing import Callable

DASH = "-"
UNDERLINE = "_"

global_shared_i18n = None


def get_locale_from_win_registry() -> str:
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\International") as key:
            return winreg.QueryValueEx(key, "LocaleName")[0].replace(DASH, UNDERLINE)
    except FileNotFoundError:
        return "en_US"


def get_system_locale() -> str:
    if platform.system() == "Windows":
        buffer = ctypes.create_unicode_buffer(85)
        if ctypes.windll.kernel32.GetUserDefaultLocaleName(buffer, ctypes.sizeof(buffer)) == 0:
            return get_locale_from_win_registry()
        return buffer.value.replace(DASH, UNDERLINE)
    else:
        return locale.getlocale()[0] or locale.getdefaultlocale()[0] or "en_US"


def i18n(message: str = None) -> Callable[[str], str]:
    global global_shared_i18n
    if global_shared_i18n is None:
        global_shared_i18n = I18n()
    return global_shared_i18n.init_language()


class I18n:

    def __init__(self):
        self.lang = None

    def init_language(self) -> Callable[[str], str]:
        if self.lang is not None:
            return self.lang.gettext

        language = get_system_locale()
        self.lang = gettext.translation(domain="messages", localedir="i18n", languages=[language])
        self.lang.install()
        return self.lang.gettext
