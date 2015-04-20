

ble_code = """
global blender_remote_exec_result

nameOfObjectToDir = "<object_name>"
if nameOfObjectToDir in globals():
    variableObject = eval(nameOfObjectToDir)
else:
    variableObject = importlib.import_module(nameOfObjectToDir)

if variableObject:
    import console.complete_calltip
    completinglist = console.complete_calltip.complete("<query>", 999, {nameOfObjectToDir : variableObject})
    sb_output("nameOfObjectToDir=%s" % nameOfObjectToDir)
    sb_output("variableObject=%s" % variableObject)
    sb_output(completinglist)
    retstr = str(completinglist[-1])
    # return retstr
else:
    sb_output("could not find namespace : %s" % namespace )

blender_remote_exec_result = retstr
"""
ble_code = ble_code.replace('<object_name>', 'bpy')
ble_code = ble_code.replace('<query>', 'bpy')

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
print(result)
# for item in result:
    # print (item)

# for item in br.utils.blender_remote_console_namespace_complete(remote, 'bpy', 'bpy.'):
    # print (item)