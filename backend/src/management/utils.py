from transliterate import translit
from transliterate.base import registry, TranslitLanguagePack
from transliterate.discover import autodiscover


def transliterate(text: str) -> str:
    autodiscover()

    class BelarusianLanguagePack(TranslitLanguagePack):
        language_code = "by"
        language_name = "Belarusian"
        mapping = (
            u"ўЎіІ",
            u"yYiI",
        )

    registry.register(cls=BelarusianLanguagePack, force=True)
    print(translit(value=text, language_code='by'))
    return translit(value=text, language_code='by')
