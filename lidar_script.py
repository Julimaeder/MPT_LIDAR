import open3d as o3d
import asyncio
import os


def load_data(path="ply_scan/Scan_20_24_51.ply"):
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
    # Create a wireframe representation of the mesh and color the wireframe
    print("creating wireframe")
    wireframe = o3d.geometry.LineSet.create_from_triangle_mesh(poisson_mesh)
    wireframe.paint_uniform_color([1, 0.41, 0.71])  # RGB-color value for pink
    
    return poisson_mesh, wireframe

async def show_model(poisson_mesh, wireframe):
    # Visualize the reconstructed mesh and its wireframe
    print("visualizing...")
    await asyncio.sleep(0) # bug in asyncio that blocks the loop unless asyncio.sleep() is used
    o3d.visualization.draw_geometries([poisson_mesh], mesh_show_wireframe=True)

async def save_data_gltf(poisson_mesh, save_path="gltf_3d_mesh/reconstructed_mesh.gltf"):
    # Save the reconstructed mesh as a glTF file
    print("Save file as Graphics Library Transmission Format (.glTF)")
    # create empty directory to save file in if not existing
    if os.path.exists("gltf_3d_mesh"==False):
        os.makedirs("gltf_3d_mesh")
    o3d.io.write_triangle_mesh("gltf_3d_mesh/reconstructed_mesh.gltf", poisson_mesh)
    print(f"your glTF file has been saved to '/{save_path}'")

async def main():
    path = "a"
    while (len(path) < 4) ^ (path == "n"): # prevent user from keeping empty and giving impossible path
        path = input("path to your ply-data (n for default): ")
    if path == "n":
        model = load_data()
    else:
        model = load_data(path)
    poisson_mesh, wireframe = edit_data(model)
    # run show_model() and save_data_gltf() concurrently
    await asyncio.gather(show_model(poisson_mesh, wireframe),
                         save_data_gltf(poisson_mesh))

if __name__ == '__main__':
    asyncio.run(main())
