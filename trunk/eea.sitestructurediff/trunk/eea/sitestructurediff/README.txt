
Js tree for plone

  >>> from eea.sitestructurediff.browser.sitemap import SitemapView
  >>> view = SitemapView(self.portal.folder, self.portal.REQUEST)

  >>> def getT(children):
  ...   t = []
  ...   for c in children:
  ...     t.append((c['attributes']['id'], (c['data']['title'].startswith('0') or c['data']['attributes']['title'] == 'missing: ') and c['data']['title'] or c['data']['attributes']['title']))
  ...     t.extend(getT(c.get('children',[])))
  ...   return t
  >>> getT(view.data())
  [('plone-folder-Folder2-0', 'Folder2'), ('plone-folder-Folder2-sv-0', 'missing: pl'), ('plone-folder-Folder2-pl-0', 'Folder2-pl'), ('plone-folder-Folder1-0', 'Folder1'), ('plone-folder-Folder1-sv-0', 'missing: pl'), ('plone-folder-Folder1-pl-0', 'Folder1-pl')]

  >>> getT(view.statusdata())
  [('plone-folder-Folder2-1', '0 (1/3)'), ('plone-folder-Folder2-sv-1', 'missing: pl'), ('plone-folder-Folder2-pl-1', '0 (0/3)'), ('plone-folder-Folder1-1', '0 (1/3)'), ('plone-folder-Folder1-sv-1', 'missing: pl'), ('plone-folder-Folder1-pl-1', '0 (0/3)')]

In a subpath we want to see only the folders that are missing a language

  >>> view = SitemapView(self.portal.folder, self.portal.REQUEST)
  >>> view.request['path'] = '/plone/folder/Folder2'
  >>> [ id for id, diff in getT(view.statusdata()) if diff.startswith('missing')]
  ['plone-folder-Folder2-Folder2-1', 'plone-folder-Folder2-Folder1-1']

  >>> folder22 = self.portal.folder.Folder2.Folder2
  >>> folder22.getTranslations().keys()
  ['en', 'sv']

We need a subscriber to listen for invalidate events since when we run tests we
don't setup memcache but still use it's invalidation event. This subscriber will
invalidate the default ram cache.

  >>> from lovely.memcached.event import IInvalidateCacheEvent
  >>> from zope.component import adapter, provideHandler
  >>> from plone.memoize.ram import global_cache
  >>> @adapter(IInvalidateCacheEvent)
  ... def invalidateCache(event):
  ...    try:
  ...     global_cache.invalidateAll()
  ...    except:
  ...     pass
  >>> provideHandler(invalidateCache)

Lets create the sync view and fix some diffs

  >>> from eea.sitestructurediff.browser.sync import SyncDiff
  >>> self.portal.REQUEST['path'] = '/plone/folder/Folder2/Folder2'
  >>> folder22.setTitle('Missing title')
  >>> sync = SyncDiff(self.portal.folder, self.portal.REQUEST)
  >>> sync.syncStructure()

Now we should only have two folders left that are not synchronized

  >>> view.request['path'] = '/plone/folder/Folder2'
  >>> [ id for id, diff in getT(view.statusdata()) if diff.startswith('missing')]
  ['plone-folder-Folder2-Folder2-1', 'plone-folder-Folder2-Folder1-1']
