import bpy
from neuron_visualization_addon.model.Projection import Projection

class Cell(object):
    '''
    This class represents a brain cell in the network
    '''
    # ------------------------------------------------------------------------
    # Declaring static variables
    # ------------------------------------------------------------------------
    # --- Dictionary of generated models ---
    # generated_models = {}
    # --- ID for the cell ---
    count = 0

    def __init__(self, id):
        self.id = id + str(Cell.count)
        Cell.count += 1
    #    if id not in Cell.generated_models:
        # Create some placeholder
        bpy.ops.mesh.primitive_uv_sphere_add( segments=64, ring_count=32, size=0.2, location=(0,0,0))
        # Name the object as the cell
        bpy.context.object.name = self.id
        # Save the referrence
        self.blender_obj = bpy.context.object
        self.blender_obj.select = False
    #    else:
    #        Cell.generated_models[id].duplicate()
    #        self.blender_obj = bpy.context.object
        print("Cell " + self.id + " is created")

    def setLocation(self, location):
        self.blender_obj.location = location

    def getLocation(self):
        return self.blender_obj.location

    def drawAxon(self, weight, destination):
        projection = Projection(self.blender_obj)
        projection.makeSimpleProjection(weight, destination)
