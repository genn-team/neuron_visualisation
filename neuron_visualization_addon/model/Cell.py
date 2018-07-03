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

    def __init__(self, id, location=(0,0,0)):
        self.id = id #+ str(Cell.count)
        Cell.count += 1
    #    if id not in Cell.generated_models:
        # Create some placeholder
        bpy.ops.mesh.primitive_uv_sphere_add( segments=64, ring_count=32, size=0.1, location=location)
        # Name the object as the cell
        bpy.context.object.name = self.id
        # Save the referrence
        self.blender_obj = bpy.context.object
        self.blender_obj.select = False
        self.projectsTo = []
        self.receivesFrom = []
    #    else:
    #        Cell.generated_models[id].duplicate()
    #        self.blender_obj = bpy.context.object

    def setLocation(self, location):
        self.blender_obj.location = location
        for axon in self.receivesFrom:
            axon.updateDestination(location)

    def getLocation(self):
        return self.blender_obj.location

    def drawAxon(self, weight, destinationCell):
        projection = Projection(self.blender_obj)
        projection.makeSimpleProjection(weight, destinationCell.getLocation())
        self.projectsTo.append(projection)
        destinationCell.projectTo(projection)
        return projection

    def projectTo(self, projection):
        self.receivesFrom.append(projection)

    def setColor(self, color=(0.0,0.0,0.0)):
        material = bpy.data.materials.new("CellColor")
        material.diffuse_color = color
        self.blender_obj.active_material = material

    def spike(self, time):
        material = bpy.data.materials.new("CellColor")
        self.blender_obj.active_material = material
        print(self.blender_obj.active_material)
        material.diffuse_color = (0.0,0.0,0.0)
        material.keyframe_insert(data_path="diffuse_color", frame = 0)
        material.diffuse_color = (0.0,0.0,0.0)
        material.keyframe_insert(data_path="diffuse_color", frame = time-1)
        material.diffuse_color = (1.0,1.0,1.0)
        material.keyframe_insert(data_path="diffuse_color", frame = time)
        material.diffuse_color = (0.0,0.0,0.0)
        material.keyframe_insert(data_path="diffuse_color", frame = time+1)
