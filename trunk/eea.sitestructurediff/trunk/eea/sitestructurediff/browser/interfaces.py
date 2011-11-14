""" Ea.sitestructurediff interfaces
"""
from zope.interface import Interface

class ISiteSyncStructure(Interface):
    """ ISiteSyncStructure
    """

    def syncStructure(): 
        """ Create translations that are missing 
        """

class ISyncMove(Interface):
    """ ISyncMove
    """

    def sync(): 
        """ Move translations when canonical is moved 
        """

