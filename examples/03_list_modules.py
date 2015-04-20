ble_code = """
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
ble_code = ble_code.replace('{object_name}', 'bpy')
ble_code = ble_code.replace('{query}', 'bpy.')

import imp
import sys
import os
# add lib to sys paths
lib_folderpath = os.path.abspath(os.path.join(__file__, '..', '..', 'lib'))
if lib_folderpath not in sys.path:
    sys.path.append(lib_folderpath)

import blender_remote as br
imp.reload(br)

remote = br.BlenderRemote('localhost', 8006)
# print(remote)
result = remote.exec_code(ble_code)
for item in result:
    print (item)

# for item in br.utils.blender_remote_console_namespace_complete(remote, 'bpy', 'bpy.'):
    # print (item)