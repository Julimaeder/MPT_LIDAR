![GitHub](https://img.shields.io/github/license/till-teb/expenses-management-tool)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/till-teb/expenses-management-tool/main.yml)

# MPT_LIDAR

Hello we are students from Dusseldorf University of Applied Sciences and this is our 4th semester project in the field of MPT (Machine Perception and Tracking).

The MPT LIDAR Python project deals with the processing of a point cloud mesh and its implementation in a VR Meta Quest environment.

## Description
The lidar_script.py allows to load a LIDAR point cloud scan and convert it into a 3D mesh. 
The mesh is then displayed in a window where it is possible to take a closer look at the 3D model. 
In the view mode you can move around in the 3D space and switch the wireframe on and off as needed. 
After finishing the view mode a copy of the 3d model is saved in the folder "gltf_3d_mesh" as a .glTF file for further processing in the VR Meta Quest.

#### controlls in renderer:
```
    W to show/hide wireframe on mesh
    R to reset camera
    Q, Esc to exit renderer
    H for help message (in console)
    left mouse to rotate
    middle mouse / strg + left mouse for height + side movement
    shift + left mouse to roll
```

## Contribution
Feel free to open a pull request or an issue if you have any suggestions for improvements.

## Installation and run
please note that a LIDAR scan is required as a ".ply" file and must be placed in the "ply_scan" or other folder of your choice.
A sample scan is available under the download link:  
https://drive.google.com/file/d/1L25GpNh-8fGvyawtEdPPwsrVR8pkgTfv/view?usp=sharing 

Download and install:   
```
git clone https://github.com/Julimaeder/MPT_LIDAR.git  
cd MPT_LIDAR  
pip install -r requirements.txt    
```


Then:   
- run:   
```
python lidar_script
```


## Final Data:
https://drive.google.com/drive/folders/1M6tTGkDTPXaTPsOWzqo6xvJ2llFN9bHv?usp=sharing
