import open3d as o3d
#import trimesh
#import numpy as np

# Load a ply point cloud, print it, and render it
pcd = o3d.io.read_point_cloud("ply_scan/Scan_20_24_51.ply")
# print(np.asarray(pcd.points))
# o3d.visualization.draw_geometries([pcd],
#                                   zoom=0.3412,
#                                   front=[0.4257, -0.2125, -0.8795],
#                                   lookat=[2.6172, 2.0475, 1.532],
#                                   up=[-0.0694, -0.9768, 0.2024])

# Downsample the point cloud with a voxel of 0.05
print("Downsampling")
voxel_down_pcd = pcd.voxel_down_sample(voxel_size=0.02)
#uni_down_pcd = pcd.uniform_down_sample(every_k_points=2)
o3d.visualization.draw_geometries([voxel_down_pcd],
                                  zoom=0.3412,
                                  front=[0.4257, -0.2125, -0.8795],
                                  lookat=[2.6172, 2.0475, 1.532],
                                  up=[-0.0694, -0.9768, 0.2024])

voxel_down_pcd.estimate_normals()

# estimate radius to drop lose points
# distances = pcd.compute_nearest_neighbor_distance()
# avg_dist = np.mean(distances)
# radius = 1.5 * avg_dist   



# alpha = 0.05
# print(f"alpha={alpha:.3f}")
# mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(voxel_down_pcd, alpha)
# mesh.compute_vertex_normals()
# o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)

print("creating mesh with many alpha values")
radii = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5]
rec_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
    pcd, o3d.utility.DoubleVector(radii))
o3d.visualization.draw_geometries([voxel_down_pcd, rec_mesh])

o3d.io.write_triangle_mesh("mesh.stl", rec_mesh)