import bpy
import mathutils
from neuron_visualization_addon.model.Cell import Cell

class Population(object):
    """
    This class represents a population of brain cells in the network
    """

    def __init__(self, id, size, cell_type):
        """The constructor.

        :param id: The population ID.
        :type id: string
        :param size: Population size
        :type size: int
        :param cell_type: Cell type of the population
        :type cell_type: string
        """
        self.id = id
        self.size = size
        self.cell_type = cell_type
        self.cells = {}
        print("Population " + self.id + " is created")

    @property
    def location(self):
        """Location of the center of mass.

        :type location: Vector
        """
        location_sum = mathutils.Vector((0,0,0))
        for _, cell in self.cells.items():
            location_sum += cell.location
        return location_sum / len(self.cells)

    @location.setter
    def location(self, location):
        self.blender_obj.location = location

    def pullTogether(self):
        """Pull cells towards the center of mass."""
        centerOfMass = self.location
        for cell in self.cells:
            cell.location = cell.location + 1/10 * (centerOfMass - cell.location)

    def setColor(self, color=(0.0,0.0,0.0)):
        """Set RGB color to the whole population

        :param color: RGB color
        :type color: tuple

        """
        material = bpy.data.materials.new("PopulationColor_"+self.id)
        material.diffuse_color = color
        for key,cell in self.cells.items():
            cell.blender_obj.active_material = material

    def removeColor(self):
        """Remove coloring from the population."""
        for _,cell in self.cells.items():
            cell.blender_obj.active_material = None
