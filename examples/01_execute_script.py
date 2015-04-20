import imp
import sys
import os
# add lib to sys paths
lib_folderpath = os.path.abspath(os.path.join(__file__, '..', '..', 'lib'))
if lib_folderpath not in sys.path:
    sys.path.append(lib_folderpath)

import blender_remote as br

remote = br.BlenderRemote('localhost', 8006)
print(remote)
result = remote.execfile('/home/sven.fr/grid_tools/gsnippets/python/01_hello_world.py')
print(result)
