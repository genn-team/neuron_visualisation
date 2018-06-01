import bpy
from neuron_visualization_addon.model.Cell import Cell

class Population(object):
    '''
    This class represents a population of brain cells in the network
    '''
    def __init__(self, id, size, cell_type):
        self.id = id
        self.size = size
        self.cell_type = cell_type
        self.cells = []
        for i in range(self.size):
            self.cells.append(Cell(self.cell_type))
        print("Population " + self.id + " is created")

    def setLocation(self, location):
        self.blender_obj.location = location

    def getLocation(self):
        return self.blender_obj.location
