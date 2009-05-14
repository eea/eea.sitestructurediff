from zope.interface import Interface

class ISiteSyncStructure(Interface):

    def syncStructure():
        """ create translations that are missing """


