import logging
from . import errors

import sys
import json
import os
import urllib
import urllib.request

class BlenderRemoteApi(object):
    """core functionality
    """
    def __init__(self, blender_remote):
        """construct

        Args:
            blender_remote (BlenderRemote): model of remote
        """
        self.blender_remote = blender_remote
        self.std_out = None
        self.logger = logging.getLogger(__name__)

    def create_url(self, argument):
        """generate the url with given arguments

        Args:
            argument (str): argument to add in the remote
        """
        urlpath = "http://%s:%s/?%s" % (self.blender_remote.host, self.blender_remote.port, argument)
        return urlpath

    def translate_results(self, results):
        """ translate the return result in to something understandable
        """
        if results == None:
            return

        return_dict = json.loads(results.strip() )
        self.std_out = return_dict['stdout']
        self.logger.info('----------')
        self.logger.info('results=%s' % results)
        self.logger.info('----------')
        return return_dict

    def communicate(self, arguments_dict):
        """ send given arguments
        """
        argument_str_list = []
        for key in arguments_dict:
            value = arguments_dict[key]
            argument_str_list.append('%s=%s' % (key, value) )
        argumentString = '&'.join(argument_str_list)

        urlString = self.create_url(argumentString)
        returnResultString = self.send_url(urlString)

        return self.translate_results(returnResultString)
        
    def send_url(self,urlpath):
        """send the url and retreive the results
        """
        self.logger.info('urlpath=%s' % urlpath)
        # handle = urllib.request.urlopen(urlpath,timeout=0.2)
        try:
            handle = urllib.request.urlopen(urlpath,timeout=0.2)
        except:
            raise errors.BlenderRemoteError("ERROR : No Connection was found with Blender")
            
        returnstring = handle.read()
        returnstring = returnstring.decode()
        
        if returnstring != "":
            return (returnstring.strip() )

        return None

def blender_remote_execfile(remote, script):
    """execute given script filepath

    Args:
        script (str): filepath to script
    """
    operator = BlenderRemoteApi(remote)
    data_dict = {'scriptpath' : urllib.parse.quote_plus(script) }
    results = operator.communicate(data_dict)

    if results:        
        if operator.std_out:
            print(str(operator.std_out))
        return results['result']

def blender_remote_exec(remote, code):
    """execute given script filepath

    Args:
        script (str): filepath to script
    """
    operator = BlenderRemoteApi(remote)
    data_dict = {'exec' : urllib.parse.quote_plus(code) }
    results = operator.communicate(data_dict)

    if results:        
        if operator.std_out:
            print(str(operator.std_out))
        return results['result']

def blender_remote_console_namespace_complete(remote, namespace, query):
    """return list of namespace completion

    Args:
        namespace (str): name of the namespace, e.g. 'bpy'
        query (str): what to query e.g. 'bpy.bl'
    
    """
    operator = BlenderRemoteApi(remote)
    data_dict = {'console_namespace_complete' : query, 'namespace' : namespace }
    results = operator.communicate(data_dict)
    
    if results == None:
        return None
    return results['result']