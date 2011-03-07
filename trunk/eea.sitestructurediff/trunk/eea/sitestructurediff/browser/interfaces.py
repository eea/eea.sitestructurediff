from zope.interface import Interface

class ISiteSyncStructure(Interface):

    def syncStructure(): #pyflakes, #pylint: disable-msg = E0211

        """ create translations that are missing """

class ISyncMove(Interface):

    def sync(): #pyflakes, #pylint: disable-msg = E0211

        """ move translations when canonical is moved """

