""" Translations module used for translating folder & topic titles
"""
from zope.i18n import translate as realTranslate
untranslatedMessages = {}

def translate(msgid, target_language, output=False):
    """ Translation method from EEAPloneAdmin
    """
    translation = realTranslate(msgid, target_language=target_language)
    if translation == str(msgid):
        if msgid not in untranslatedMessages.get(target_language, {}).keys():
            if untranslatedMessages.get(target_language) is None:
                untranslatedMessages[target_language] = {}

            translation = untranslatedMessages.get(target_language).get(msgid)
            if translation is None:
                translation = str(msgid)
                untranslatedMessages.get(target_language)[msgid] = translation
        translation = untranslatedMessages.get(target_language).get(msgid)
    if type(translation) == type(''):
        return translation
    if type(translation) == type(u''):
        return translation.encode('utf8')
    # what do we have here?
    return str(translation)
