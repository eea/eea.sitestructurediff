from zope.interface import Interface

class ISiteSyncStructure(Interface):

    def syncStructure():
        """ create translations that are missing """

class ISyncMove(Interface):

    def sync():
        """ move translations when canonical is moved """

