ble_code = """
global blender_remote_exec_result

import console.complete_import
completinglist = console.complete_import.complete("{import_line}")
print(completinglist)
blender_remote_exec_result = completinglist
""".format(import_line='import bpy.')

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