################################################################################
#
# SublimeBlender.py
#
# Version: 1.0
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
    # global running  
    DEBUG = False
    SUBLIME_STDOUT = True

    originalStdOut = None
    newStdOut = None

    import urllib
    from urllib.parse import urlparse
    import sys, io, traceback

    if SUBLIME_STDOUT:
      originalStdOut = sys.stdout
      newStdOut = io.StringIO()
      sys.stdout = newStdOut

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

    if "scriptpath" in params:
      scriptpath = params["scriptpath"]
      
      if DEBUG: print('#' + scriptpath)
      # print(params)
      scriptpath = scriptpath.strip()
      if scriptpath != None:
        try:
          exec(compile(open(scriptpath).read(), scriptpath, 'exec'))
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
        "version": (1, 0)
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
    self.http_thread.shutdown()
    self.http_thread.socket.close()
    self.control_thread.shutdown()
    self.control_thread.socket.close()
    bpy.utils.unregister_class(SublimeBlenderOpenConnection)
    
if __name__ == "__main__":
    register()

