""" Translations module used for translating folder & topic titles
"""
from zope.i18n import translate as realTranslate

HAS_GTRANSLATE = True
try:
    from valentine.gtranslate import translate as gtranslate
except ImportError:
    HAS_GTRANSLATE = False


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
                # we have run gtranslate so now we just keep it untranslated
                translation = str(msgid)

                # google translate doesn't have all languages
                if target_language not in ['tr', 'mt', 'hu']:
                    if HAS_GTRANSLATE:
                        try:
                            translation = gtranslate(str(msgid), 
                                            langpair="en|%s" % target_language)
                        except Exception:
                            print "GTRANSLATE FAILED %s and msgid %s" % \
                                                    (target_language, msgid)

                untranslatedMessages.get(target_language)[msgid] = translation
        translation = untranslatedMessages.get(target_language).get(msgid)
    if type(translation) == type(''):
        return translation
    if type(translation) == type(u''):
        return translation.encode('utf8')
    # what do we have here?
    return str(translation)
