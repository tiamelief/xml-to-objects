import sys
import clr
import re
# clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

import xml.etree.ElementTree as ET

tree = ET.parse(IN[0].FullPath)
root = tree.getroot()

scale = 1

pipe_networks = root.find("PipeNetworks").findall("PipeNetwork")

#PLAN

# separate rectangle from circular pipes
# find the coordinate and other attributes
# render the pipes


def struct_to_coord(struct):
    elev = struct.find("Invert").attrib["elev"]
    coord = struct.find("Center").text
    coord = coord.split()
    
    coord = {
        "x": float(coord[0]),
        "y": float(coord[1]),
        "z": float(elev)
    }
    return coord
    
circ_pipes = []
rect_pipes = []

for pipe_network in pipe_networks:
    structs = pipe_network.find("Structs").findall("Struct")

    for pipe in pipe_network.find("Pipes").findall("Pipe"):
        attrs = pipe.attrib
        start_ref = attrs["refStart"]
        end_ref = attrs["refEnd"]
        
        start_struct = next((s for s in structs if s.attrib["name"] == start_ref))
        end_struct = next((s for s in structs if s.attrib["name"] == end_ref))
        start_coord = struct_to_coord(start_struct)
        end_coord = struct_to_coord(end_struct)
        
        id = pipe.attrib["name"]
        slope = float(pipe.attrib["slope"])
        length = float(pipe.attrib["length"])
        pipe_dict = ({
            "start": start_coord,
            "end": end_coord,
            "id": id,
            "slope": slope,
            "length": length,
        })
        if pipe.find("CircPipe") is not None:
            diameter = float(pipe.find("CircPipe").attrib["diameter"])
            pipe_dict["diameter"] = diameter
            material_circ = pipe.find("CircPipe").attrib["material"]
            pipe_dict["material"] = material_circ
            thickness_circ = float(pipe.find("CircPipe").attrib["thickness"])
            pipe_dict["thickness"] = thickness_circ
            circ_pipes.append(pipe_dict)
            
        elif pipe.find("RectPipe") is not None:
            rect_pipe = pipe.find("RectPipe")
            height = float(rect_pipe.attrib["height"])
            width = float(rect_pipe.attrib["width"])
            pipe_dict["height"] = height
            pipe_dict["width"] = width
            material_rect = rect_pipe.attrib["material"]
            pipe_dict["material"] = material_rect
            thickness_rect = float(rect_pipe.attrib["thickness"])
            pipe_dict["thickness"] = thickness_rect
            rect_pipes.append(pipe_dict)
  

#circ_pipes_as_list = []
#for key in circ_pipes[0].keys():
#    circ_pipes_as_lists[key] = [pipe[key] for pipe in circ_pipes])


OUT = circ_pipes, rect_pipes
