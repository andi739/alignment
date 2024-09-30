from pyntcloud import PyntCloud
import pandas as pd
import open3d as o3d
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.StlAPI import StlAPI_Writer
from OCC.Extend.DataExchange import write_ply_file
from utils import move_shape_to_center

# ply -> csv (normalized)
def ply2csv(filenameIN, filenameOUT, normalized=False):
    cloud = PyntCloud.from_file(filenameIN)
    df = cloud.points
    df = df[['x','y', 'z']]
    if normalized:
        df = (df-df.min())/(df.max()-df.min())
    df.to_csv(filenameOUT, sep=" ", header=0, index=False)

def stl2csv(filenameIN, filenameOUT, num_points=1000, normalized=False):
    mesh = o3d.io.read_triangle_mesh(filenameIN)
    pcd = mesh.sample_points_poisson_disk(num_points)
    cloud = PyntCloud.from_instance("open3d", pcd)
    df = cloud.points
    df = df[['x','y', 'z']]
    if normalized:
        df = (df-df.min())/(df.max()-df.min())
    df.to_csv(filenameOUT, sep=" ", header=0, index=False)

def step2ply(filenameIN, filenameOUT, moveToCenter=True):
    reader = STEPControl_Reader()
    reader.ReadFile(filenameIN)
    reader.TransferRoots()
    shape = reader.OneShape()
    if moveToCenter:
        shape = move_shape_to_center(shape)
    write_ply_file(shape, filenameOUT)
    return

def step2stl(filename, filenameOUT, moveToCenter=True):
    reader = STEPControl_Reader()
    reader.ReadFile(filename)
    reader.TransferRoots()
    shape = reader.OneShape()
    if moveToCenter:
        shape = move_shape_to_center(shape)
    mesher = BRepMesh_IncrementalMesh(shape, 0.01)
    mesher.Perform()
    if not mesher.IsDone():
        raise AssertionError("Mesh is not done")
    stlWriter = StlAPI_Writer()
    stlWriter.Write(shape,filenameOUT)
    return