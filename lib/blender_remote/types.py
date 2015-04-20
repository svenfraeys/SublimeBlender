"""types used in remote
"""
from . import utils

class BlenderRemote(object):
    """remote system for blender
    """
    def __init__(self, host, port):
        """construct object
        """
        self.host = host
        self.port = port

    def execfile(self, script):
        """execute given script filepath

        Args:
            script (str): filepath to script
        """
        return utils.blender_remote_execfile(self, script)

    def exec_code(self, code):
        """eval given code in blender
        """
        return utils.blender_remote_exec(self, code)