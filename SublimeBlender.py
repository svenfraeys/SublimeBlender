################################################################################
#
# SublimeBlender.py
#
# Version: 1.10
# Author: Sven Fraeys
#
# Description: 
# Sends a html signal, Blender will receive the signal once it has opened it's connection
# 
# Free for non-commercial use
#
################################################################################
import sys
import socket
import urllib
import http.client
import urllib.request
import subprocess
import json
import os
import sublime, sublime_plugin
import textwrap
# add lib to sys paths
lib_folderpath = os.path.abspath(os.path.join(__file__, '..', 'lib'))
if lib_folderpath not in sys.path:
    sys.path.append(lib_folderpath)

import blender_remote as br

VERBOSITY = 0
def log(message,verbosity=1):
    """print out message depending on verbosity
    """
    if verbosity <= VERBOSITY:
        print (message)

class SublimeBlenderAbstract(object):
    """Main class for communicating with blender
    """
    def __init__(self):
        self._stdOut = ''
        self._returnDictionary = ''

    def getData(self):
        dataDict = {
            'console_namespace_complete' : '',
            'stdout' : '',
        }
        return dataDict

    def executeScriptFie(self, filepath):
        """ execute the given filepath
        """

    def getStdOut(self):
        """ get self._stdOut
        """
        return self._stdOut
    
    def setStdOut(self, value):
        """ set self._stdOut
        """
        self._stdOut = value

    def communicate(self):
        return

class SublimeBlender(SublimeBlenderAbstract):
    """ socket system to connect with blender
    """
    def __init__(self):
        super(SublimeBlender, self).__init__()
        settings = sublime.load_settings("SublimeBlender.sublime-settings")
        host = settings.get('host')
        port = settings.get('port')
        self._host = host
        self._port = port

    def getHost(self):
        """ get self._host
        """
        return self._host
    
    def setHost(self, value):
        """ set self._host
        """
        return self._host

    def getPort(self):
        """ get self._port
        """
        return self._port
    
    def setPort(self, value):
        """ set self._port
        """
        return self._port

    def sendUrl(self,urlpath,quiet=False):
        """ send the url and retreive the results
        """
        log('urlpath=%s' % urlpath)
        # handle = urllib.request.urlopen(urlpath,timeout=0.2)
        try:
            handle = urllib.request.urlopen(urlpath,timeout=0.2)
            pass
        except:
            log("ERROR : No Connection was found with Blender")
            if not quiet:
                sublime.error_message("ERROR : No Connection was found with Blender")
            return None
        returnstring = handle.read()
        returnstring = returnstring.decode()
        
        if returnstring != "":
            return (returnstring.strip() )

        return None

    def executeScriptFie(self, scriptFile):
        """ execute the given script path
        """
        log('scriptFile=%s' % scriptFile)
        results = self.communicate({'scriptpath' : urllib.parse.quote_plus(scriptFile) })

        if results is None:
            return None
            
        stdOut = self.getStdOut()
        if stdOut != '':
            print('%s' % stdOut)
        return results['result']

    def restart_module(self,module_name):
        """
        send signal to blender to restart a module
        
        Args :-
            module_name (str) :- name of the module to restart
                                    e.g. :- 'SublimeBlenderAddon'
  
        """
        print( 'restaring module : {0}'.format(module_name) )
        results = self.communicate({'restart_module' : module_name })

        if results is None:
            return None
            
        stdOut = self.getStdOut()
        if stdOut != '':
            print('%s' % stdOut)
        return None
        # return results['result']
    
    def getConsoleNamespaceComplete(self,query,namespace):
        results = self.communicate({'console_namespace_complete' : query, 'namespace' : namespace },quiet=True)
        if results == None:
            return None
        return results['result']
        
    def getConsoleCalltipComplete(self,query,namespace):
        results = self.communicate({'console_calltip_complete' : query, 'namespace' : namespace },quiet=True)
        results = results['result']
        # results = 'tempdebuscript calltip'

        # results = results.split("\n")
        # returnResults = []
        for result in results:
            if len(result) > 201:
                returnResults.append(result[:200])
                returnResults.append(result[200:])
            else:
                returnResults.append(result)
        return returnResults

    def getConsoleImportComplete(self,line):
        results = self.communicate({'console_import_complete' : line },quiet=True)
        return results['result']

        results = 'test;result'
        return results.split(";")

    def getProperties(self,objectname):
        urlpath = self.createUrl("dir=%s&stdout=False" % objectname)
        results = self.sendUrl(urlpath,quiet=True)
        return results.split(";")

    def createUrl(self, argument):
        """ generate the url with given arguments
        """
        urlpath = "http://%s:%s/?%s" % (self.getHost(), self.getPort(), argument)
        return urlpath

    def translateResults(self, results):
        """ translate the return result in to something understandable
        """
        if results == None:
            return

        returnJson = json.loads(results.strip() )
        self.setStdOut(returnJson['stdout'])
        log('----------')
        log('results=%s' % results)
        log('----------')
        return returnJson

    def communicate(self, argumentsDict,quiet=False):
        """ send given arguments
        """
        argumentStringList = []
        for key in argumentsDict:
            value = argumentsDict[key]
            argumentStringList.append('%s=%s' % (key, value) )
        argumentString = '&'.join(argumentStringList)

        urlString = self.createUrl(argumentString)
        returnResultString = self.sendUrl(urlString,quiet)

        return self.translateResults(returnResultString)
        pass

class SublimeBlenderLaunch(sublime_plugin.WindowCommand):
    def run(self):
        subprocess.Popen([r'C:\Program Files\Blender Foundation\Blender\blender.exe'])

class SublimeBlenderExecuteCommand(sublime_plugin.WindowCommand):
    """execute a scriptFile
    """
    def run(self):
        """run command
        """
        print('running sublime blender')
        window = sublime.active_window()

        if not window:
            return

        view = window.active_view()

        if not view:
            return

        if view.file_name() is None:
            return

        # for a in dir(self.view):
            # print(a)
        
        if view.is_dirty():
            view.run_command("save")

        # communicate

        scriptpath = view.file_name()

        if not scriptpath:
            return

        blender_remote = create_blender_remote()
        blender_remote.execfile(scriptpath)
        return

        blenderCommunication = SublimeBlender()

        # scriptpath = r'C:\Users\sven\Dropbox\WG_Code\sfr\blender\scripts\helloWorld.py'

        if scriptpath == None:
            return

        log(scriptpath)
        result = blenderCommunication.executeScriptFie(scriptpath)
        if result :
            pass
            # run_command
            # sublime.active_window().run_command('show_panel',{'panel':'console','toggle':False})
            # sublime.active_window().show_panel(panel='console', toggle=True)

class SublimeBlenderRestartModuleCommand(sublime_plugin.WindowCommand):
    """restart a module in blender with this command
    """
    def find_module_name(self):
        """return module name that needs to be restarted

        Returns:
            modulename (str): name of the module to restart, e.g.: 'SublimeBlenderAddon'
        """
        window = sublime.active_window()

        if not window:
            return None

        view = window.active_view()

        if not view:
            return None

        if view.file_name() is None:
            return None

        # for a in dir(self.view):
            # print(a)
        
        # communicate
        blenderCommunication = SublimeBlender()
        scriptpath = view.file_name()
        dirname = os.path.dirname(scriptpath)
        modulename = os.path.split(dirname)[-1]
        return modulename

    def run(self):
        """run the restart module command
        """
        modulename = self.find_module_name()
        print('modulename={0}'.format(modulename) )
        if modulename == None:
            print('no module found to restart')
            return False

        blender_remote = create_blender_remote()
        restart_module(blender_remote, modulename)

        # blenderCommunication = SublimeBlender()
        # blenderCommunication.restart_module(modulename)

RESTART_MODULE_CODE = """
    module_name = "{module_name}"
    print("disable addon " + module_name)
    bpy.ops.wm.addon_disable(module=module_name)
    print("enable addon " + module_name)
    bpy.ops.wm.addon_enable(module=module_name)
    """

COMPLETE_NAMESPACE_CODE = """
    global blender_remote_exec_result
    import console.complete_namespace
    object_to_dir = None

    name_to_dir = "{object_name}"

    if name_to_dir in globals():
        object_to_dir = eval(name_to_dir)
    else:
        object_to_dir = importlib.import_module(name_to_dir)
    if object_to_dir:
        completinglist = console.complete_namespace.complete("{query}", {name_to_dir : object_to_dir})
        
        # if len(completinglist) > 101:
            # completinglist = completinglist[:100]

    # return completinglist 
    # print(blender_remote_exec_result)
    # print(completinglist)
    blender_remote_exec_result = completinglist 
    # print(blender_remote_exec_result)
    """

COMPLETE_IMPORT_CODE = """
    global blender_remote_exec_result

    import console.complete_import
    completinglist = console.complete_import.complete("{import_line}")
    print("{import_line}")
    print(completinglist)
    blender_remote_exec_result = completinglist
    """

COMPLETE_CALLTIP_CODE = """
    global blender_remote_exec_result

    nameOfObjectToDir = "{object_name}"
    if nameOfObjectToDir in globals():
        variableObject = eval(nameOfObjectToDir)
    else:
        variableObject = importlib.import_module(nameOfObjectToDir)

    if variableObject:
        import console.complete_calltip
        completinglist = console.complete_calltip.complete("{query}", 999, {nameOfObjectToDir : variableObject})
        sb_output("nameOfObjectToDir=%s" % nameOfObjectToDir)
        sb_output("variableObject=%s" % variableObject)
        sb_output(completinglist)
        retstr = str(completinglist[-1])
        # return retstr
    else:
        sb_output("could not find namespace : %s" % namespace )

    blender_remote_exec_result = retstr
    """

def restart_module(blender_remote, module_name):
    """restart module
    """
    blender_code = textwrap.dedent(RESTART_MODULE_CODE)
    blender_code = blender_code.format(module_name=module_name)
    return blender_remote.exec_code(blender_code)

def console_complete_import(blender_remote, import_str):
    """return list of complete suggestions

    Args:
        import_str (str): line of import (e.g. 'import bpy.o')

    """
    blender_code = textwrap.dedent(COMPLETE_IMPORT_CODE)
    blender_code = blender_code.format(import_line=import_str)
    return blender_remote.exec_code(blender_code)
    
def console_complete_namespace(blender_remote, object_name, query):
    """return list of completions

    Args:
        blender_remote (str): blender remote object
        object_name (str): name of object to query, e.g. 'bpy'
        query (str): what to query from this object, e.g. : 'bpy.bla'
    """
    blender_code = textwrap.dedent(COMPLETE_NAMESPACE_CODE)
    blender_code = blender_code.replace('{object_name}', object_name)
    blender_code = blender_code.replace('{query}', query)
    result = blender_remote.exec_code(blender_code)
    return result

def console_complete_calltip(blender_remote, object_name, query):
    """return list of completions

    Args:
        blender_remote (str): blender remote object
        object_name (str): name of object to query, e.g. 'bpy'
        query (str): what to query from this object, e.g. : 'bpy.bla'
    """
    blender_code = textwrap.dedent(COMPLETE_CALLTIP_CODE)
    blender_code = blender_code.replace('{object_name}', object_name)
    blender_code = blender_code.replace('{query}', query)
    result = blender_remote.exec_code(blender_code)
    return result

def create_blender_remote():
    """return a BlenderRemote instance
    """
    settings = sublime.load_settings("SublimeBlender.sublime-settings")
    host = settings.get('host')
    port = settings.get('port')
    blender_remote = br.BlenderRemote(host, port)
    return blender_remote

class SublimeBlenderCompletion(sublime_plugin.EventListener):
    """ auto complete manager
    """
    def on_query_completions(self, view, prefix, locations):
        # create the remote
        blender_remote = create_blender_remote()
        
        

        log('query bpy completions...')
        
        linestring, beforestring, afterstring = self.getLineFullBeforeAfter(view)
        log('beforestring=%s' % beforestring)
        log('afterstring=%s' % afterstring)
        log( (linestring, beforestring, afterstring) )
        
        # linestring = 'bpy.'
        # beforestring = 'bpy.'
        # afterstring = ''

        if linestring.find("import") == -1 and linestring.find("bpy") == -1:
            log('nothing found')
            return ([])

        currentword = (beforestring.strip().split(' ')[-1])
        log("currentword=%s" % currentword)

        if currentword.find("bpy") == -1:
            return ([],sublime.INHIBIT_EXPLICIT_COMPLETIONS)

        log('getLineFullBeforeAfter')
        
        
        commandlist, query = self.getCommandList(beforestring)
        log('commandlist=%s' % commandlist)

        
        importCommand = '.'.join(commandlist)
        properties = []
        
        if beforestring[-1] == "(":
            returndata = console_complete_calltip(blender_remote, "bpy", importCommand+"."+ query)
            # returndata = (SublimeBlender().getConsoleCalltipComplete(importCommand+"."+ query,"bpy"))
            if returndata is None:
                return ([])
            returndata = [returndata]

            log("returndata=")
            log(returndata)
            res = view.show_popup_menu( returndata, None )
            return ([],sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

        if beforestring.find("import") != -1:
            log("getConsoleImportComplete")
            importstring = beforestring.strip()
            # importstring = beforestring.strip().replace(" ","%20")

            properties = console_complete_import(blender_remote, importstring)
            # properties = SublimeBlender().getConsoleImportComplete(importstring)
            if properties is None:
                return ([])
        else:
            namespace = importCommand.split(".")[0]
            log("namespace=%s" % namespace)
            importstring = "" + importCommand + "." +query
            if namespace != "":
                properties = console_complete_namespace(blender_remote, namespace, importstring)
                # properties = SublimeBlender().getConsoleNamespaceComplete(importstring,namespace)
                if properties is None:
                    return ([])

                propertiesnew = []
                for prop in properties:
                    newprop = prop.replace(importCommand,"")
                    if newprop == "":
                        continue
                    if newprop[0] == ".":
                        newprop = newprop[1:]
                    propertiesnew.append(newprop)
                    
                properties = propertiesnew
            
        filteredproperties = []

        for propertyName in properties:
            if propertyName != "" and propertyName.find("__") == -1:
                if query == '' or propertyName.find(query) != -1:
                    filteredproperties.append(propertyName)
                else:
                    log( 'skip:%s' % propertyName)

        # res = self.view.show_popup_menu( filteredproperties, None )
        # print(properties[res])

        completions = [ (prop,prop) for prop in filteredproperties ]
        return (completions,sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

    def getCommandList(self,beforestring):
        currentword = (beforestring.strip().split(' ')[-1])
        log("currentword=%s" % currentword)
        
        if currentword.find("bpy") == -1:
            log('nno bpy Foundation')
            return (None, None)

        keycommandList = (currentword.split('.'))
        keycommandList[0] = keycommandList[0].split("(")[-1]
        log("keycommandList=%s" % keycommandList)
        importCommand = '.'.join ( (keycommandList[:-1]) )
        query = keycommandList[-1]
        log("query='%s'" % query)
        log("importCommand=%s" % importCommand)

        return (keycommandList[:-1], query)


    def getLineFullBeforeAfter(self, view):
        
        log("-")
        log("collect")
        for region in ( view.sel()):
            selectedRegion = region

        lineregion = (view.line(selectedRegion))
        differenceregion = sublime.Region((selectedRegion.a - lineregion.a), (selectedRegion.b - lineregion.b) )
        log(lineregion)
        log(selectedRegion)
        log(differenceregion)

        linestring = view.substr( (lineregion) )
        beforestring= linestring[:differenceregion.a]
        afterstring = linestring[differenceregion.a:]

        return (linestring, beforestring, afterstring)


# blenderCommunication = SublimeBlender()
# scriptpath = sublime.active_window().active_view().file_name()