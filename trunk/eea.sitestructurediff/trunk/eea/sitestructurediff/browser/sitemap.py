from zope.component import getMultiAdapter
from zope.interface import implements

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from Products.CMFPlone.browser.navtree import buildFolderTree, SitemapNavtreeStrategy
from Products.CMFPlone.browser.interfaces import INavtreeStrategy
from Products.CMFPlone.browser.interfaces import ISiteMap
from plone.memoize.ram import cache

def cacheKey(method, self, st=0):
    request = self.request
    path = request.get('path', '0')
    if path == 0:
        path = '%s' % self.context.absolute_url(1)
    return (path, st)

class SitemapView(BrowserView):
    implements(ISiteMap)
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @cache(cacheKey)
    def data(self, st=0):
        context = self.context

        path = '/'.join(context.getPhysicalPath())
        if self.request.get('path', '0') != '0':
            path = self.request.get('path', path)

        obj = context.unrestrictedTraverse(path)
        query =  {'path' : { 'query' : path,
                             'depth' : 4},
                  'portal_type' : ['Folder', 'Topic', 'RichTopic'],
                  }
        strategy = getMultiAdapter((obj, self), INavtreeStrategy)
        data = buildFolderTree(context, obj=obj, query=query, strategy=FullStrategy(obj, self))
        properties = getToolByName(context, 'portal_properties')
        navtree_properties = getattr(properties, 'navtree_properties')
        bottomLevel = navtree_properties.getProperty('bottomLevel', 0)
        # XXX: The recursion should probably be done in python code
        portal_url = getToolByName(context, 'portal_url').getPortalObject().absolute_url()
        try:
            siteLangView = context.unrestrictedTraverse('@@translatedSitesLanguages')
        except:
            siteLangView = None

        lt = getToolByName(context, 'portal_languages')
        languages = lt.getSupportedLanguages()
        if siteLangView is not None:
            languages = [ lang for lang, foo in siteLangView() ]
        totalLang = len(languages)

        def getNodes(children):
            nodes = []
            tdiff = 0
            for c in children:
                translations = c['item'].getTranslationLanguages
                diff = [ lang for lang in languages
                              if lang not in  translations ]
                title = c['Title']
                children, cdiff = getNodes(c['children'])
                tdiff = max([tdiff, cdiff,len(diff)])

                if st==1:
                    title = '%s (%s/%s)' % (len(diff), cdiff, totalLang)

                node = { 'attributes': { 'id' : '%s-%s' % (c['path'].replace('/','-')[1:], st),
                                         'class' : 'state-%s' % c['review_state'],
                                         'path' : c['path']},
                         'state': c['currentItem'] and "open" or "closed",
                         'data': {  'title' : '%s' % title,
                                    'icon' :  '%s/%s' % (portal_url, c['icon']) ,
                                    'attributes' : { 'href' : c['getURL'],
                                                     'rel' : c['portal_type'],
                                                     'title' : 'missing: %s' % ','.join(diff)},
                                    },
                         }

                if self.request.get('path', '0') != '0':
                    if children:
                        node['children'] = children
                    else:
                        node['state'] = 'leaf'
                    
                nodes.append(node)
                
            return nodes, tdiff

        result, foo  = getNodes(data['children'])
        if not result:
            result ={ 'attributes': { 'id' : 'empty'},
                      'state': "closed",
                      'data': {  'title' : 'no folders or topics' },
                      }
        return result


    def statusdata(self):
        return self.data(st=1)

class FullStrategy(SitemapNavtreeStrategy):

    def __init__(self, context, view=None):
        SitemapNavtreeStrategy.__init__(self, context, view)

        self.rootPath = '/'.join(context.getPhysicalPath())
        self.excludeIds = {}
        
    def nodeFilter(self, node):
        return True

    
