# -*- coding: utf-8 -*-
"""
Doctest runner for 'valentine.linguaflow'
"""
__docformat__ = 'restructuredtext'

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Products.CMFCore.utils import getToolByName
import transaction

import doctest
optionflags =  (doctest.ELLIPSIS |
        doctest.NORMALIZE_WHITESPACE )

import unittest

@onsetup
def setup_eea_sitestructurediff():
    """ Setup EEA Sitestructurediff
    """

    fiveconfigure.debug_mode = True
    import Products.Five
    import eea.sitestructurediff
    import valentine.linguaflow
    zcml.load_config('meta.zcml', Products.Five)
    zcml.load_config('configure.zcml', eea.sitestructurediff)
    zcml.load_config('configure.zcml', valentine.linguaflow)
    fiveconfigure.debug_mode = False

    #ptc.installProduct('PloneLanguageTool')
    ptc.installProduct('LinguaPlone')


setup_eea_sitestructurediff()

ptc.setupPloneSite(products=['LinguaPlone', \
        'eea.sitestructurediff'], extension_profiles= \
        ['valentine.linguaflow:default', 'eea.sitestructurediff:default'])

CONTENT = { 'type' : 'Folder',
        'count' : 2,
        'languages' : ['sv','pl'],
        'children' : [ { 'type' : 'Folder',
            'count' : 2,
            'languages' : ['sv'],
            'children' : [ { 'type' : 'Folder',
                'count' : 2,
                'languages' : ['sv','pl'],
                'children' : [ { 'type' : 'Document',
                    'count' : 3,
                    'languages' : ['sv','pl'],},
                    ] },
                { 'type' : 'Document',
                    'count' : 1,
                    'languages' : ['pl'],}
                ] },
            { 'type' : 'Document',
                'count' : 3,
                'languages' : ['sv','pl'],},
            ]
        }


def setUpContent(root):
    """ Setup test folders
    """
    portal = root.portal
    root.setRoles(['Manager'])
    ourId = portal.invokeFactory('Folder', id='folder')
    folder = portal[ourId]

    def createContent(context, content):
        """ Create predefined set of folders
        """
        i = content['count']
        ids = []
        while i > 0:
            ourId = context.invokeFactory(content['type'], id='%s%s' \
                    % (content['type'], i))
            portal.portal_workflow.doActionFor(context[ourId], 'publish')
            for lang in content['languages']:
                context[ourId].addTranslation(lang)
            context[ourId].reindexObject()
            ids.append(ourId)
            i -= 1
        children = content.get('children', [])
        for child in  children:
            for item in ids:
                createContent(context[item], child)
    createContent(folder, CONTENT)
    transaction.savepoint()

def setUp(root):
    """ SetUp portal for tests
    """
    portal = root.portal
    lt = getToolByName(portal, 'portal_languages')
    # flags because HTML is broken when running browser tests
    lt.manage_setLanguageSettings('en', ['en', 'sv', 'pl'], displayFlags=True)
    setUpContent(root)

def test_suite():
    """ TestSuite
    """
    from unittest import TestSuite
    suite = TestSuite()
    from Testing.ZopeTestCase import FunctionalDocFileSuite
    suite.addTest(FunctionalDocFileSuite(
        'README.txt',
        setUp=setUp,
        #tearDown=tearDown,
        package="eea.sitestructurediff",
        test_class=ptc.FunctionalTestCase,
        optionflags=optionflags),
        )
    suite.addTest(FunctionalDocFileSuite(
        'sync.txt',
        setUp=setUp,
        #tearDown=tearDown,
        package="eea.sitestructurediff.browser",
        test_class=ptc.FunctionalTestCase,
        optionflags=optionflags),
        )
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
