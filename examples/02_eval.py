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
print(remote)
result = remote.exec_code('import bpy')
print(result)
