import gettext
from typing import Callable


class I18n:

    def __init__(self):
        self.lang = None
        self.translations = {}

    def init_language(self, domain: str, localedir: str, languages: list[str]) -> Callable[[str], str]:
        self.lang = gettext.translation(domain=domain, localedir=localedir, languages=languages)
        self.lang.install()
        return self.lang.gettext


_global_shared_i18n = None


def i18n(message: str = None) -> Callable[[str], str]:
    global _global_shared_i18n
    if _global_shared_i18n is None:
        _global_shared_i18n = I18n()
    return _global_shared_i18n.init_language(domain="messages", localedir="i18n", languages=["zh_CN"])
