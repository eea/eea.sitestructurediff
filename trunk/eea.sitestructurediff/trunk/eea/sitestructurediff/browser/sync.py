from zope.interface import implements
from zope.event import notify
import md5

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView

from lovely.memcached.event import InvalidateCacheEvent
from eea.sitestructurediff.browser.interfaces import ISiteSyncStructure
from Products.EEAPloneAdmin.exportimport.localsite import translate

class SyncDiff(BrowserView):
    implements(ISiteSyncStructure)
    
    def __init__(self, context, request):
        self.request = request
        self.context = context

    def syncStructure(self):
        synccontext = context = self.context
        path = self.request.get('path', '0')
        if path != '0':
            synccontext = context.restrictedTraverse(path)

        lt = getToolByName(context, 'portal_languages')
        languages = lt.getSupportedLanguages()
        translations = synccontext.getTranslationLanguages()
        title = synccontext.Title()
        for lang in languages:
            if lang not in  translations:
                synccontext.addTranslation(lang)
                translation = synccontext.getTranslation(lang)
                translation.setTitle(translate(title, lang))
                translation.reindexObject()
        synccontext.reindexObject()

        currentPath = path
        path = path.split('/')
        p = 0
        while p < len(path):
            keystring = "eea.sitestructurediff.browser.sitemap.data:(['eea.sitestructurediff'], '%s', %s)"
            key = md5.new(keystring  % (currentPath, 0)).hexdigest()
            notify(InvalidateCacheEvent(key=key, raw=True))
            key = md5.new(keystring % (currentPath, 1)).hexdigest()
            notify(InvalidateCacheEvent(key=key, raw=True))
            currentPath = '/'.join(path[:-p])
            p += 1
            
