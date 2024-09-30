import convert
import orientations
import open3d as o3d
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, shutil

def compare_point_clouds_stl(src_dir, tgt_dir, threshold=0.1):
    tmp_path = "./.tmp/"
    num_compares = 0
    num_errors = 0
    try:
        os.makedirs(tmp_path)
        for src_file in os.listdir(src_dir):
            src_path = src_dir + src_file 
            tgt_path = tgt_dir + src_file[:src_file.rfind("_0")] + "_CAM_0.stp"

            stl_src = tmp_path + src_file[:src_file.rfind(".")] + ".stl"
            stl_tgt = tmp_path + src_file[:src_file.rfind("_0")] + "_CAM_0.stl"
            
            convert.step2stl(src_path,stl_src, moveToCenter=True)
            convert.step2stl(tgt_path, stl_tgt, moveToCenter=True)

            # TODO downsample! for better performance
            mesh_src = o3d.io.read_triangle_mesh(stl_src)
            pcd_src = o3d.geometry.PointCloud()
            pcd_src.points = mesh_src.vertices
            mesh_tgt = o3d.io.read_triangle_mesh(stl_tgt)
            pcd_tgt = o3d.geometry.PointCloud()
            pcd_tgt.points = mesh_tgt.vertices
            mean_dist = np.asarray(pcd_src.compute_point_cloud_distance(pcd_tgt)).mean()
            print(src_path)
            print(tgt_path)
            print(f"mean distance: {mean_dist}")
            print("------------------------------")
            num_compares += 1
            if mean_dist > threshold:
                num_errors += 1
        print("------------------------------")
        print(f"Accuracy: {(num_compares-num_errors)/num_compares}. {num_errors} Errors for {num_compares} Compares.")
    except Exception as e:  
        print(e)
    return shutil.rmtree(tmp_path)