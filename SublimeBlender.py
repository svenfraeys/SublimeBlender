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
import getpass
import subprocess
import json
import os
import sublime, sublime_plugin

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
        blenderCommunication = SublimeBlender()
        scriptpath = view.file_name()

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
    """
    restart a module in blender with this command
    
    Args :-
        
    
    Returns :-
        
        
    """

    def find_module_name(self):
        """
        return module name that needs to be restarted
        
        Args :-
            
        
        Returns :-
            modulename (str) :- name of the module to restart
                                    e.g. :- 'SublimeBlenderAddon'
            
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
        """
        run the restart module command
        
        Args :-
            
        
        Returns :-
            
            
        """
        modulename = self.find_module_name()
        print('modulename={0}'.format(modulename) )
        if modulename == None:
            print('no module found to restart')
            return False

        blenderCommunication = SublimeBlender()
        blenderCommunication.restart_module(modulename)

class SublimeBlenderCompletion(sublime_plugin.EventListener):
    """ auto complete manager
    """
    def on_query_completions(self, view, prefix, locations):
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
            returndata = (SublimeBlender().getConsoleCalltipComplete(importCommand+"."+ query,"bpy"))
            if returndata is None:
                return ([])

            log("returndata=")
            log(returndata)
            res = view.show_popup_menu( returndata, None )
            return ([],sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

        if beforestring.find("import") != -1:
            log("getConsoleImportComplete")
            importstring = beforestring.strip().replace(" ","%20")
            properties = SublimeBlender().getConsoleImportComplete(importstring)
            if properties is None:
                return ([])
        else:
            namespace = importCommand.split(".")[0]
            log("namespace=%s" % namespace)
            importstring = "" + importCommand + "." +query
            if namespace != "":
                properties = SublimeBlender().getConsoleNamespaceComplete(importstring,namespace)
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