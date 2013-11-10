
################################################################################
#
# SublimeBlender.py
#
# Version: 1.0
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

class SublimeBlenderCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# html = urllib2.urlopen(url, timeout=25).read();

		# settings
		HOST = "localhost"		# host, needs to be identical as the one in Blender
		PORT = 8006				# port number, needs to be identical as the one in Blender
		DEBUG = False			# debug, to show prints

		# get current open scene
		scriptpath = (self.view.file_name())
		scriptpath = scriptpath.replace(" ","+")

		# url to send
		
		urlpath = "http://%s:%s/?scriptpath=%s" % (HOST, PORT, scriptpath)
		# urlpath = "http://localhost:8007/?print=hello"
		# urlpath = "http://google.com"
		if DEBUG : print(urlpath)

		handle = urllib.request.urlopen(urlpath,timeout=100)

		returnstring = handle.read()

		returnstring = returnstring.decode()
		if returnstring != "":
			print(returnstring.strip() )


		# send the url request
		# conn = http.client.HTTPConnection(urlpath)
		
