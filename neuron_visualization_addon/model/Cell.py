import bpy

class Cell():
    '''
    This class represents a brain cell in the network
    '''
    # Declaring static dictionary of generated models
    #generated_models = {}
    def __init__(self, id):
        self.id = id
    #    if id not in Cell.generated_models:
        # Create some placeholder
        bpy.ops.mesh.primitive_uv_sphere_add( segments=64, ring_count=32, size=0.2, location=(0,0,0))
        # Name the object as the cell
        bpy.context.object.name = self.id
        # Save the referrence
        self.blender_obj = bpy.context.object
    #    else:
    #        Cell.generated_models[id].duplicate()
    #        self.blender_obj = bpy.context.object
        print("Cell " + self.id + " is created")

    def setLocation(self, location):
        self.blender_obj.location = location

    def getLocation(self):
        return self.blender_obj.location
