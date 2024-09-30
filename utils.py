from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.StepRepr import StepRepr_RepresentationItem
from OCC.Display.SimpleGui import init_display
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Core.AIS import AIS_ColoredShape
from OCC.Core.Quantity import Quantity_Color, Quantity_NameOfColor
from OCC.Core.Bnd import Bnd_OBB
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.gp import gp_Trsf, gp, gp_Ax3, gp_Ax2, gp_XYZ, gp_Pnt, gp_Dir
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop_SurfaceProperties
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.GeomAbs import GeomAbs_Plane
from OCC.Core.BRep import BRep_Tool
from OCC.Core.Geom import Geom_Plane
from OCC.Extend.DataExchange import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.STEPConstruct import stepconstruct_FindEntity
from OCC.Core.TCollection import TCollection_HAsciiString

def bnd_to_shape(bnd_obb : Bnd_OBB):
    gpCenter = gp_Pnt(bnd_obb.Center())
    xDir = (bnd_obb.XDirection())
    yDir = (bnd_obb.YDirection())
    zDir = (bnd_obb.ZDirection())
    hX = bnd_obb.XHSize()
    hY = bnd_obb.YHSize()
    hZ = bnd_obb.ZHSize()
    axes = gp_Ax2(gpCenter, gp_Dir(zDir), gp_Dir(xDir))
    xDir.Multiply(hX), yDir.Multiply(hY), zDir.Multiply(hZ)
    
    gpCenterXYZ = gpCenter.XYZ()
    gpCenterXYZ.Subtract(xDir)
    gpCenterXYZ.Subtract(yDir)
    gpCenterXYZ.Subtract(zDir)
    axes.SetLocation(gp_Pnt(gpCenterXYZ))
    return BRepPrimAPI_MakeBox(axes, 2*hX, 2*hY, 2*hZ)

def move_shape_to_center(shape):
        # Move model center to coord 0,0,0
        bnd_box = Bnd_OBB()
        brepbndlib.AddOBB(shape, bnd_box)
        bb_center = gp_Pnt(bnd_box.Center())
        trsf = gp_Trsf()
        trsf.SetTranslation(bb_center, gp.Origin())
        transform = BRepBuilderAPI_Transform(shape, trsf)
        return transform.Shape() 