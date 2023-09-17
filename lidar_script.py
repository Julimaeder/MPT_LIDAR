import open3d as o3d
import numpy as np

# Load the LIDAR point cloud
print("load LIDAR point cloud")
lidar = o3d.io.read_point_cloud("ply_scan/Scan_20_24_51.ply") 

# Downsample the point cloud
print("Downsampling")
lidar_down = lidar.voxel_down_sample(voxel_size=0.02)

# Remove statistical outliers
cl, ind = lidar_down.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)

# Select the inlier points
inlier_cloud = lidar_down.select_by_index(ind)

# Surface reconstruction
poisson_mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(inlier_cloud, depth=9)

# Create a wireframe representation of the mesh
wireframe = o3d.geometry.LineSet.create_from_triangle_mesh(poisson_mesh)

# Set the color of the wireframe to red (RGB: [255, 0, 0])
wireframe.paint_uniform_color([1, 0.41, 0.71])  # RGB-color value for pink

# Visualize the reconstructed mesh and its wireframe
o3d.visualization.draw_geometries([poisson_mesh, wireframe])

# Save the reconstructed mesh as a glTF file
print("Save file as Graphics Library Transmission Format (.glTF)")
o3d.io.write_triangle_mesh("gltf_3d_mash/reconstructed_mesh.gltf", poisson_mesh)
