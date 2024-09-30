from align import batch_align_stl
from benchmark import compare_point_clouds_stl

if __name__ == "__main__":
    
    # 0. read stp
    # 1. move_shape_to_center
    # 2. mkdir .tmp save shape as ply in .tmp
    # 3. o3d -> read ply as point-cloud
    # 4. try registration with o3d, pcl or fls
    # last. rm .tmp
    
    dummy_filepath = "C:/Users/schwarza/Documents/Multivac/STEP_CAM/_CAM/Dummy_Stempel_TZW_CAM_0.stp"
    cad_in_dir = "C:/Users/schwarza/Documents/Multivac/STEP_CAM/unlabeled/"
    cad_out_dir = "./aligned/"
    #batch_align_stl(dummy_filepath, cad_in_dir, cad_out_dir, num_points=2000)
    #compare_point_clouds_stl("./aligned/", "C:/Users/schwarza/Documents/Multivac/STEP_CAM/_CAM/")