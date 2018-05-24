import bpy
from neuron_visualization_addon.model.Population import Population

class Network():
    '''
    This class represents a network
    '''
    def __init__(self, id):
        self.id = id
