import bpy
import mathutils
from neuron_visualization_addon.model.Cell import Cell

class Population(object):
    '''
    This class represents a population of brain cells in the network
    '''
    def __init__(self, id, size, cell_type):
        self.id = id
        self.size = size
        self.cell_type = cell_type
        self.cells = {}
        print("Population " + self.id + " is created")

    def setLocation(self, location):
        # TODO
        self.blender_obj.location = location

    def getLocation(self):
        location_sum = mathutils.Vector((0,0,0))
        for cell in self.cells:
            location_sum += cell.getLocation()
        return location_sum / len(self.cells)

    def pullTogether(self):
        centerOfMass = self.getLocation()
        for cell in self.cells:
            cellLocation = cell.getLocation()
            cell.setLocation(cellLocation + 1/10 * (centerOfMass - cellLocation))

    def setColor(self, color=(0.0,0.0,0.0)):
        material = bpy.data.materials.new("PopulationColor_"+self.id)
        material.diffuse_color = color
        for key,cell in self.cells.items():
            print(cell)
            cell.blender_obj.active_material = material

    def removeColor(self):
        for cell in self.cells:
            cell.blender_obj.active_material = None
