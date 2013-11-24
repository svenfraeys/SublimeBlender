
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
 
import socket
import sys
import sublime, sublime_plugin
import urllib, sys
import urllib.request
import http.client

class SublimeBlender(object):
	'''
		Main class for communicating with blender
	'''
	HOST = "localhost"		# host, needs to be identical as the one in Blender
	PORT = 8006				# port number, needs to be identical as the one in Blender
	DEBUG = True			# debug, to show prints

	def sendUrl(self,urlpath,quiet=False):
		if self.DEBUG : print(urlpath)
		try:
			handle = urllib.request.urlopen(urlpath,timeout=0.2)
		except:
			print("ERROR : No Connection was found with Blender")
			if not quiet:
				sublime.error_message("ERROR : No Connection was found with Blender")
			return ""

		returnstring = handle.read()
		returnstring = returnstring.decode()
		
		if returnstring != "":
			return (returnstring.strip() )

		return ""

	def createUrl(self, argument):
		urlpath = "http://%s:%s/?%s" % (self.HOST, self.PORT, argument)
		return urlpath

	def executeFile(self, filepath):
		# url to send
		urlpath = self.createUrl("scriptpath=%s" % filepath)
		results = self.sendUrl(urlpath)
		print(results)
	
	def getConsoleNamespaceComplete(self,query,namespace):
		urlpath = self.createUrl("console_namespace_complete=%s&namespace=%s&stdout=False" % (query, namespace) )
		results = self.sendUrl(urlpath,quiet=True)
		return results.split(";")
	def getConsoleImportComplete(self,line):
		urlpath = self.createUrl("console_import_complete=%s&stdout=False" % line)
		results = self.sendUrl(urlpath,quiet=True)
		return results.split(";")

	def getProperties(self,objectname):
		
		urlpath = self.createUrl("dir=%s&stdout=False" % objectname)
		results = self.sendUrl(urlpath,quiet=True)
		return results.split(";")

	def printOut(self,printmessage):
		urlpath = self.createUrl("print=%s" % printmessage)
		results = self.sendUrl(urlpath)
		print(results)
		
		pass

class SublimeBlenderExecuteCommand(SublimeBlender, sublime_plugin.TextCommand):
	def run(self, edit):
		# for a in dir(self.view):
			# print(a)
		if self.view.is_dirty():
			self.view.run_command("save")

		
		# get current open scene
		scriptpath = (self.view.file_name())
		scriptpath = scriptpath.replace(" ","+")
		
		self.executeFile(scriptpath)

class SublimeBlenderCollector(SublimeBlender, sublime_plugin.EventListener):
	def on_query_completions(self, view, prefix, locations):
		DEBUG = False
		# if prefix == "":
			# return ([],sublime.INHIBIT_EXPLICIT_COMPLETIONS)

		# if prefix[-1] != ".":
			# prefix = prefix + "."

		if DEBUG : print("-")
			
		if DEBUG : print("prefix:%s" % prefix)
		if DEBUG : print("locations:%s" % locations)
		if DEBUG : print("collect")
		for region in ( view.sel()):
			selectedRegion = region

		lineregion = (view.line(selectedRegion))
		differenceregion = sublime.Region((selectedRegion.a - lineregion.a), (selectedRegion.b - lineregion.b) )
		if DEBUG : print (lineregion)
		if DEBUG : print (selectedRegion)
		if DEBUG : print (differenceregion)

		linestring = view.substr( (lineregion) )

		if linestring.find("import") == -1 and linestring.find("bpy") == -1:
			return ([])
		
		beforestring= linestring[:differenceregion.a]
		afterstring = linestring[differenceregion.a:]
		
		if DEBUG : print ('beforestring=%s' % beforestring)
		if DEBUG : print ('afterstring=%s' % afterstring)
		currentword = (beforestring.strip().split(' ')[-1])
		if DEBUG: print("currentword=%s" % currentword)
		if currentword.find("bpy") == -1:
			return ([],sublime.INHIBIT_EXPLICIT_COMPLETIONS)
		keycommandList = (currentword.split('.'))
		if DEBUG : print("keycommandList=%s" % keycommandList)
		importCommand = '.'.join ( (keycommandList[:-1]) )
		query = keycommandList[-1]
		if DEBUG : print ("query='%s'" % query)
		if DEBUG : print ("importCommand=%s" % importCommand)

		sb = SublimeBlender()
		properties = []
		
		if beforestring.find("import") != -1:
			if DEBUG : print("getConsoleImportComplete")
			importstring = beforestring.strip().replace(" ","%20")
			properties = sb.getConsoleImportComplete(importstring)
		else:
			namespace = importCommand.split(".")[0]
			if DEBUG : print("namespace=%s" % namespace)
			importstring = "" + importCommand + "." +query
			if namespace != "":
				properties = sb.getConsoleNamespaceComplete(importstring,namespace)
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
					if DEBUG : print( 'skip:%s' % propertyName)

		# res = self.view.show_popup_menu( filteredproperties, None )
		# print(properties[res])

		completions = [ (prop,prop) for prop in filteredproperties ]
		return (completions,sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)
