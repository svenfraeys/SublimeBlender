################################################################################
#
# SublimeBlender.py
#
# Version: 1.10
# Author: Sven Fraeys
#
# Description: 
# Blende addon, it will process the incoming url request that is launched by sublime
# 
# Free for non-commercial use
#
################################################################################

import threading
import http.server
import socketserver

import time, traceback
import bpy

PORT = 8006   # port number, needs to be identical as the Sublime Plugin
IP_ADDRESS = "localhost" # ip address, needs to be identical as the Sublime Plugin


#IP_ADDRESS = "192.168.254.1"
# global running
# running = 1


class RequestHandler(http.server.BaseHTTPRequestHandler):
  ''' RequestHandler will process the incoming data

  '''

  def _writeheaders(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html; charset=UTF-8')
    self.end_headers()

  def do_HEAD(self):
    self._writeheaders()
      
  def do_GET(self):
    # add cube to test behaviour
    # bpy.ops.mesh.primitive_cube_add()

    # global running  
    DEBUG = True
    SUBLIME_STDOUT = True

    originalStdOut = None
    newStdOut = None

    import urllib
    from urllib.parse import urlparse
    import sys, io, traceback

    parsed_path = urlparse(self.path)
    # print(parsed_path)
    
    try:
      params = dict([p.split('=') for p in parsed_path[4].split('&')])
    except:
      params = {}
      
    for key in params:
      parsedkey = urllib.parse.unquote_plus(params[key])
      if DEBUG: print(parsedkey)
      params[key] = parsedkey

    retstr = ""

    if "stdout" in params:
      if params["stdout"] == "True":
          SUBLIME_STDOUT = True
      elif params["stdout"] == "False":
          SUBLIME_STDOUT = False


    if SUBLIME_STDOUT:
      originalStdOut = sys.stdout
      newStdOut = io.StringIO()
      sys.stdout = newStdOut

    if "scriptpath" in params:
      scriptpath = params["scriptpath"]
      
      if DEBUG: print('#' + scriptpath)
      # print(params)
      scriptpath = scriptpath.strip()
      if scriptpath != None:
        try:
          pass
          # launch incoming script
          exec(compile(open(scriptpath).read(), scriptpath, 'exec'), globals(), locals() )
          
        except:
          print(str(traceback.format_exc()))

    if "eval" in params:
      try:
        eval(params["eval"])
      except:
        print(traceback.format_exc())

      if DEBUG : print(retstr)

    if "print" in params:
      print(params["print"])

    if "console_namespace_complete" in params:
      variableObject = None
      query = params["console_namespace_complete"]
      nameOfObjectToDir = (params["namespace"])
      import importlib
      if nameOfObjectToDir in globals():
        variableObject = eval(nameOfObjectToDir)
      else:
        variableObject = importlib.import_module(nameOfObjectToDir)
      if variableObject:
        import console.complete_namespace
        completinglist = console.complete_namespace.complete(query, {nameOfObjectToDir : variableObject})
        if DEBUG: print("nameOfObjectToDir=%s" % nameOfObjectToDir)
        if DEBUG: print("variableObject=%s" % variableObject)
        if DEBUG: print(completinglist)
        listOfAttributes = ""
        for attr in completinglist:
          listOfAttributes += attr + ";"
        retstr=listOfAttributes
      else:
        print("could not find namespace : %s" % namespace )

    if "console_import_complete" in params:
      

      nameOfObjectToDir = (params["console_import_complete"])
      import console.complete_import
      completinglist = console.complete_import.complete(nameOfObjectToDir)
      listOfAttributes = ""
      for attr in completinglist:
        listOfAttributes += attr + ";"
      retstr=listOfAttributes

    if "dir" in params:

      nameOfObjectToDir = (params["dir"])
      if DEBUG : print("dir=%s" % nameOfObjectToDir)
      listOfAttributes = ""
      variableObject = None
      found = False
      if nameOfObjectToDir in globals():
        found = True
        variableObject = eval(nameOfObjectToDir)
      else:
        try:
          import importlib
          variableObject = importlib.import_module(nameOfObjectToDir)
          found = True
        except:
          pass
        
      if found:
          # variableObject = eval(nameOfObjectToDir)
          attrs = dir(variableObject)
          for attr in attrs:
            listOfAttributes += attr + ";"
          retstr=listOfAttributes
      else:
        print("not found : %s" % nameOfObjectToDir)
      
#     retstr="finished"
#     retstr = """<HTML>
# <HEAD><TITLE>Dummy response</TITLE></HEAD>
# <BODY>dummy response</BODY>
# </HTML>"""
    if SUBLIME_STDOUT:
      sys.stdout = originalStdOut
      retstr = (newStdOut.getvalue())

    self._writeheaders()
    self.wfile.write(str(retstr).encode('latin'))

    return
    


class HttpThread(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.httpd = None

  def run(self):
    DEBUG = False
    if DEBUG: print("HTTP Server THREAD: started")
    if DEBUG: print("serving at port", PORT)
    self.httpd.serve_forever()
    if DEBUG: print ("HTTP Server THREAD: finished")
      
class ControlThread(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.httpd = None
  def run(self):
    DEBUG = False
    if DEBUG : print("Control THREAD: started")
    runcontrol = 1    
    while runcontrol >0:
      # if running < 1:
      if False:
        if DEBUG: print("try server shutdown")
        self.httpd.shutdown()
        self.httpd.socket.close() 
        if DEBUG: print("shutdown finished")
        runcontrol = 0
      time.sleep(1)                
        
    if DEBUG: print ("Control THREAD: finished")
            
import bpy
bl_info = {
        "name" : "SublimeBlender",
        "description": "Develop with Sublime Text 3 as an external script editor",
        "category" : "Development",
        "author" : "Sven Fraeys",
        "wiki_url": "https://docs.google.com/document/d/1-hWEdp1Gz4zjyio7Hdc0ZnFXKNB6eusYITnuMI3n65M",
        "version": (1, 1, 0)
}

class SublimeBlenderOpenConnection(bpy.types.Operator):
    bl_idname = "wm.sublimeblenderopenconnection"
    bl_label = "SublimeBlender Open Connection..."
    http_thread = None
    control_thread = None
    def execute(self, context):
        DEBUG = False
        httpd = None

        

        try:
          httpd = socketserver.TCPServer((IP_ADDRESS, PORT), RequestHandler)
        except:
          pass
          return {'FINISHED'}
        
        if DEBUG: print ("SCRIPT: started")
        if DEBUG: print ("httpd: %s" % httpd)

        self.http_thread = HttpThread()
        self.http_thread.httpd = httpd
        self.http_thread.start()
        

        self.control_thread = ControlThread()
        self.control_thread.httpd = httpd
        self.control_thread.start()
        
        if DEBUG: print ("SCRIPT: finished") 

        return {'FINISHED'}

def register():
    bpy.utils.register_class(SublimeBlenderOpenConnection)

def unregister():
    bpy.utils.unregister_class(SublimeBlenderOpenConnection)
    
if __name__ == "__main__":
    register()


'''
WIP
import xml.etree.cElementTree.
import xml.etree.cElementTree as ET

root = ET.Element("root")

doc = ET.SubElement(root, "doc")

field1 = ET.SubElement(doc, "field1")
field1.set("name", "blah")
field1.text = "some value1"

field2 = ET.SubElement(doc, "field2")
field2.set("name", "asdfasd")
field2.text = "some vlaue2"

tree = ET.ElementTree(root)
xml = ET.tostring(root, encoding='utf8', method='xml')
print(xml)
'''
