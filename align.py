import convert
import orientations
import open3d as o3d
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, shutil

def batch_align_stl(dummy_filepath, cad_in_dir, cad_out_dir, num_points=2000):
    tmp_path="./.tmp"
    os.makedirs(tmp_path)
    try:
        # convert dummy
        outname_dummy = tmp_path + dummy_filepath[dummy_filepath.rfind("/"):dummy_filepath.rfind(".")] + ".stl"
        convert.step2stl(dummy_filepath,outname_dummy)
        # dummy to point cloud
        mesh = o3d.io.read_triangle_mesh(outname_dummy)
        dummy_pcd = mesh.sample_points_poisson_disk(num_points) 
        for model in os.listdir(cad_in_dir):
            out_files = []
            try:
                out_files = orientations.get4orientations(cad_in_dir+model)
            except:
                print(f"failed getting possible orientations with model {model}. Skipping")
                continue
            stp_oriented = []
            for file in out_files:
                newpath = tmp_path + file[file.rfind("/"):]
                stp_oriented.append(newpath)
                shutil.move(file, newpath)
            cad_pcd = {}
            for stp in stp_oriented:
                # convert possible orientation models
                outname = stp[:stp.rfind(".")] + ".stl"
                convert.step2stl(stp, outname)
                # get point clouds
                mesh = o3d.io.read_triangle_mesh(outname)
                pcd = mesh.sample_points_poisson_disk(num_points)
                cad_pcd[outname[outname.rfind("/")+1:]] = pcd
            # get distance
            distances = []
            for name, cloud in cad_pcd.items():
                dist_np = np.asarray(dummy_pcd.compute_point_cloud_distance(cloud))
                distances.append(dist_np.mean())
                print(f"mean distance dummy <-> {name}: {distances[-1]}")
            index_min = np.argmin(distances)

            # get the best fitting step and move to out_dir
            best_file = list(cad_pcd.keys())[index_min]
            best_file = best_file[:best_file.rfind(".")]
            best_step = [s for s in stp_oriented if best_file in s][0]
            best_step_new = cad_out_dir + best_step[best_step.rfind("/")+1:]
            shutil.move(best_step, best_step_new) 
    except Exception as e:
         print(e)
    return shutil.rmtree(tmp_path)

def batch_align_ply(dummy_filepath, cad_in_dir, cad_out_dir):
    tmp_path="./.tmp"
    os.makedirs(tmp_path)
    try:
        # convert dummy
        outname_dummy = tmp_path + dummy_filepath[dummy_filepath.rfind("/"):dummy_filepath.rfind(".")] + ".ply"
        convert.step2ply(dummy_filepath,outname_dummy)
        # dummy to point cloud
        dummy_pcd = o3d.io.read_point_cloud(outname_dummy)
        for model in os.listdir(cad_in_dir):
            out_files = orientations.get4orientations(cad_in_dir+model)
            stp_oriented = []
            for file in out_files:
                newpath = tmp_path + file[file.rfind("/"):]
                stp_oriented.append(newpath)
                shutil.move(file, newpath)
            cad_pcd = {}
            for stp in stp_oriented:
                # convert possible orientation models
                outname = stp[:stp.rfind(".")] + ".ply"
                convert.step2ply(stp, outname)
                # get point clouds
                pcd = o3d.io.read_point_cloud(outname)
                cad_pcd[outname[outname.rfind("/")+1:]] = pcd
                # get distance
            distances = []
            for name, cloud in cad_pcd.items():
                dist_np = np.asarray(dummy_pcd.compute_point_cloud_distance(cloud))
                distances.append(dist_np.mean())
                print(f"mean distance dummy <-> {name}: {distances[-1]}")
            index_min = np.argmin(distances)

            # get the best fitting step and move to out_dir
            best_file = list(cad_pcd.keys())[index_min]
            best_file = best_file[:best_file.rfind(".")]
            best_step = [s for s in stp_oriented if best_file in s][0]
            best_step_new = cad_out_dir + best_step[best_step.rfind("/")+1:]
            shutil.move(best_step, best_step_new)
    except Exception as e:
        print(e)
    return shutil.rmtree(tmp_path)