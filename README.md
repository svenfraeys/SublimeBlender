SublimeBlender
==============
#### Execute scripts in Blender

![alt tag](https://dl.dropboxusercontent.com/u/1652825/code/sublime/sublimeBlender/sublimeBlender_autoComplete.png)
![alt tag](https://dl.dropboxusercontent.com/u/1652825/code/sublime/sublimeBlender/sublimeBlender_blenderCommand.png)
![alt tag](https://dl.dropboxusercontent.com/u/1652825/code/sublime/sublimeBlender/sublimeBlender_codeExecute.png)

## Intro
Develop with Sublime Text 3 as an external script editor in Blender.
Execute scripts directly from Sublime.
Receive autocomplete dropdowns from the blender modules

## Installation
download the package from [GitHub](https://github.com/svenfraeys/SublimeBlender "SublimeBlender") into your `Packages` folder

the Blender addon needs to be downloaded from [SublimeBlenderAddon](https://github.com/svenfraeys/SublimeBlenderAddon "SublimeBlenderAddon")

## How to use
1. Install [SublimeBlender](https://github.com/svenfraeys/SublimeBlender "SublimeBlender") (sublime package) and [SublimeBlenderAddon](https://github.com/svenfraeys/SublimeBlenderAddon "SublimeBlenderAddon") (blender addon)
2. Launch in Blender `SublimeBlender : Open Connection`
3. Execute a script by using `Alt+P` in Sublime Text

## Updates
march 2014
* bpy autocompletion : autocompletion when working on a bpy library
* bpy import autocompletion : when importing the bpy modules
* auto-save the file when executing your active script

february 2014
* Execute your script from Sublime directly in Blender
* Sublime Console shows the console output of Blender


## Key Bindings
* `Alt+P` : Execute open script in Blender

## Settings
In the settings you can change several parameters
* `host` : The host that will receive the signal (default : localhost)
* `port` : The port that will receive the signal (default : 8006)
 
## More Information
https://docs.google.com/document/d/1-hWEdp1Gz4zjyio7Hdc0ZnFXKNB6eusYITnuMI3n65M
