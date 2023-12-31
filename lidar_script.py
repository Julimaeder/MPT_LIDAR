import open3d as o3d
import asyncio
import os
import screeninfo as sc
import re


def load_data(path):
    # Load the LIDAR point cloud
    print("loading LIDAR point cloud")
    return o3d.io.read_point_cloud(path) 

def edit_data(model):
    # Downsample the point cloud
    print("Downsampling")
    lidar_down = model.voxel_down_sample(voxel_size=0.02)
    # Remove statistical outliers
    print("removing statistical outliers from the point cloud")
    cl, ind = lidar_down.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
    # Select the inlier points
    inlier_cloud = lidar_down.select_by_index(ind)
    # Surface reconstruction
    print("reconstructing surface")
    poisson_mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(inlier_cloud, depth=9)
    
    return poisson_mesh

def ply_path_selection():
    model = None
    while model == None:
        path = input("path to your ply-data (n for default): ")   
        if path == "n":
            model = load_data("ply_scan/Scan_20_24_51.ply")
            window_name = os.path.basename("ply_scan/Scan_20_24_51.ply")[:-4]  
        else:
            if os.path.isfile(path):
                model = load_data(path)
                window_name = os.path.basename(path)[:-4]
            elif os.path.exists(os.path.dirname(path)):
                basepath = os.path.dirname(path)
                for filename in os.listdir(basepath):
                    if filename.endswith('.ply'):
                        model = load_data(os.path.join(basepath,filename))
                        window_name = filename[:-4]
                        break
        if model == None: print("No .ply files were found. Please check spelling and special characters and try again")
    return model, window_name

async def show_model(poisson_mesh, window_name):
    # Visualize the reconstructed mesh
    print("visualizing...")
    monitors = sc.get_monitors()
    screenheight = int(re.findall("(?<=height=)[0-9]+(?=,)", str(monitors[0]))[0])
    screenwidth = int(re.findall("(?<=width=)[0-9]+(?=,)", str(monitors[0]))[0])
    await asyncio.sleep(0) # bug in asyncio that blocks the loop unless asyncio.sleep() is used
    o3d.visualization.draw_geometries([poisson_mesh], window_name=str(window_name[0]), width=screenwidth,
                                      height=screenheight, left=0, top=0, mesh_show_wireframe=True,
                                      mesh_show_back_face=True)
    """
    controlls in renderer
    W to show/hide wireframe on mesh
    R to reset camera
    Q, Esc to exit renderer
    H for help message (in console)
    left mouse to rotate
    middle mouse / strg + left mouse for height + side movement
    shift + left mouse to roll
    """

async def save_data_gltf(poisson_mesh, save_path="gltf_3d_mesh/reconstructed_mesh.gltf"):
    # Save the reconstructed mesh as a glTF file
    print("Save file as Graphics Library Transmission Format (.glTF)")
    # create empty directory to save file in if not existing
    if os.path.exists("gltf_3d_mesh")==False:
        os.makedirs("gltf_3d_mesh")
    o3d.io.write_triangle_mesh("gltf_3d_mesh/reconstructed_mesh.gltf", poisson_mesh)
    print(f"your glTF file has been saved to '/{save_path}'")

async def main():
    model, window_name = ply_path_selection()
    poisson_mesh = edit_data(model)
    # run show_model() and save_data_gltf() concurrently
    await asyncio.gather(show_model(poisson_mesh, window_name),
                         save_data_gltf(poisson_mesh))


if __name__ == '__main__':
    asyncio.run(main())
