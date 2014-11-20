## Controller Python Script "folder_paste"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Paste objects into a folder
##

from Products.CMFPlone import PloneMessageFactory as _
from AccessControl import Unauthorized
from ZODB.POSException import ConflictError

msg=_(u'Copy or cut one or more items to paste.')

if context.cb_dataValid:
    try:
        res = context.manage_pasteObjects(context.REQUEST['__cp'])
        from Products.CMFPlone.utils import transaction_note
        transaction_note('Pasted content to %s' % (context.absolute_url()))
        paste = context.restrictedTraverse('@@paste-translations')
        paste(res)
        context.plone_utils.addPortalMessage('Item(s) pasted.' )
        return state
    except ConflictError:
        raise
    except ValueError:
        msg=_(u'Disallowed to paste item(s).')
    except (Unauthorized, 'Unauthorized'):
        msg=_(u'Unauthorized to paste item(s).')
    except: # fallback
        msg=_(u'Paste could not find clipboard content.')

context.plone_utils.addPortalMessage(msg)
return state.set(status='failure')

