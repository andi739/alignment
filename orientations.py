from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.StlAPI import StlAPI_Writer
from OCC.Core.StepRepr import StepRepr_RepresentationItem
from OCC.Display.SimpleGui import init_display
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Core.AIS import AIS_ColoredShape
from OCC.Core.Quantity import Quantity_Color, Quantity_NameOfColor
from OCC.Core.Bnd import Bnd_OBB
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.gp import gp_Trsf, gp, gp_Ax3, gp_Ax2, gp_XYZ, gp_Pnt, gp_Dir, gp_Vec
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_VERTEX
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.GeomAbs import GeomAbs_Plane
from OCC.Core.BRep import BRep_Tool
from OCC.Core.Geom import Geom_Plane
from OCC.Extend.DataExchange import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.STEPConstruct import stepconstruct_FindEntity
from OCC.Core.TCollection import TCollection_HAsciiString
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from utils import bnd_to_shape

# 4 möglichkeiten mit regel : Höhe <= Breite <= Länge
def get4orientations(filename):
    # get file
    reader = STEPControl_Reader()
    reader.ReadFile(filename)
    reader.TransferRoots()
    shape = reader.OneShape()
    # get bounding box
    bnd_box = Bnd_OBB()
    brepbndlib.AddOBB(shape, bnd_box)
    box = bnd_to_shape(bnd_box).Solid()
    # get 3 unique edges
    edgeLen = {}
    expE = TopExp_Explorer(box, TopAbs_EDGE)
    while expE.More():
        edge = expE.Current()
        shellProps = GProp_GProps()
        brepgprop.LinearProperties(edge, shellProps)
        length = shellProps.Mass()
        edgeLen[round(length, 5)] = edge
        expE.Next()
    if len(edgeLen) > 3:
        raise AssertionError("Error, more than 3 unique edges!")
    edgeLen = dict(sorted(edgeLen.items()))
    # I only need two for ax3
    gp_Dirlist = []
    for edge in edgeLen.values():
        expV = TopExp_Explorer(edge, TopAbs_VERTEX)
        vert0 = expV.Current(); expV.Next()
        vert1 = expV.Current()
        pnt0 = BRep_Tool.Pnt(vert0)
        pnt1 = BRep_Tool.Pnt(vert1)
        gp_Dirlist.append(gp_Dir(gp_Vec(pnt0, pnt1)))
    axBox1 = gp_Ax3(gp.Origin(), gp_Dirlist[0], gp_Dirlist[2])
    axBox2 = gp_Ax3(gp.Origin(), gp_Dirlist[0], gp_Dirlist[2]); axBox2.XReverse()
    axBox3 = gp_Ax3(gp.Origin(), gp_Dirlist[0], gp_Dirlist[2]); axBox3.ZReverse()
    axBox4 = gp_Ax3(gp.Origin(), gp_Dirlist[0], gp_Dirlist[2]); axBox4.ZReverse(); axBox4.XReverse()
    filenames_saves = []
    for i, axBox in enumerate([axBox1, axBox2, axBox3, axBox4]):
        trsf = gp_Trsf()
        trsf.SetTransformation(axBox)
        transform = BRepBuilderAPI_Transform(shape, trsf)
        shapeAligned = transform.Shape() 
        # write files
        writer = STEPControl_Writer()
        writer.Transfer(shapeAligned, STEPControl_AsIs) 
        filenameOut = filename[:filename.rfind(".")] + "_a" + str(i) + ".stp"
        writer.Write(filenameOut) 
        filenames_saves.append(filenameOut)
    return filenames_saves