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

    ## The constructor
    # @param id         The cell ID as String
    # @param location   Cell location
    def __init__(self, id, location=(0,0,0)):
        self.id = id #+ str(Cell.count)
        Cell.count += 1
    #    if id not in Cell.generated_models:
        # Create some placeholder
        bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, size=0.05, location=location)
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

    ## Set location of the cell
    # @type location: Vector|tupple
    # @param location: Cell location
    def setLocation(self, location):
        self.blender_obj.location = location
        for axon in self.receivesFrom:
            axon.updateDestination(location)

    ## Get current cell location
    # @rtype: Vector|tupel
    # @return: Returns current location
    def getLocation(self):
        return self.blender_obj.location

    ## Draw axon between this cell and destination cell
    # @type weight: float
    # @param weight: The weight of a connection
    # @type destinationCell: Cell
    # @param destinationCell: Projection destionation cell
    # @rtype: Vector|tupel
    # @return: Returns current location
    def drawAxon(self, weight, destinationCell):
        projection = Projection(self.blender_obj)
        projection.makeSimpleProjection(weight, destinationCell.getLocation())
        self.projectsTo.append(projection)
        destinationCell.isProjectedTo(projection)
        return projection

    ## Add projections from which the input is received
    # @type projection: Projection
    # @param projection: Projection to be added
    def isProjectedTo(self, projection):
        self.receivesFrom.append(projection)

    ## Set color
    # @type color: tupple
    # @param color: Color
    def setColor(self, color=(0.0,0.0,0.0)):
        material = bpy.data.materials.new("CellColor")
        material.diffuse_color = color
        self.blender_obj.active_material = material

    def setSpikes(self, spikes):
        material = bpy.data.materials.new("CellColor")
        self.blender_obj.active_material = material
        for [time,intensity] in spikes:
            material.diffuse_color = Cell.getJetColor(0.0)
            material.keyframe_insert(data_path="diffuse_color", frame = time-8)
            self.blender_obj.scale = (1., 1., 1.)
            self.blender_obj.keyframe_insert(data_path="scale", frame = time-8)
            material.diffuse_color = Cell.getJetColor(intensity / 4)
            material.keyframe_insert(data_path="diffuse_color", frame = time-6)
            material.diffuse_color = Cell.getJetColor(intensity / 2)
            material.keyframe_insert(data_path="diffuse_color", frame = time-4)
            material.diffuse_color = Cell.getJetColor(intensity * 3 / 4)
            material.keyframe_insert(data_path="diffuse_color", frame = time-2)
            material.diffuse_color = Cell.getJetColor(intensity)
            material.keyframe_insert(data_path="diffuse_color", frame = time)
            self.blender_obj.scale = (1.0, 1.0, 1.0)
            self.blender_obj.keyframe_insert(data_path="scale", frame = time)
            material.diffuse_color = Cell.getJetColor(intensity * 3 / 4)
            material.keyframe_insert(data_path="diffuse_color", frame = time + 2)
            material.diffuse_color = Cell.getJetColor(intensity / 2)
            material.keyframe_insert(data_path="diffuse_color", frame = time + 4)
            material.diffuse_color = Cell.getJetColor(intensity / 4)
            material.keyframe_insert(data_path="diffuse_color", frame = time + 6)
            material.diffuse_color = Cell.getJetColor(0.0)
            material.keyframe_insert(data_path="diffuse_color", frame = time + 8)
            self.blender_obj.scale = (1., 1., 1.)
            self.blender_obj.keyframe_insert(data_path="scale", frame = time + 8)

    def getJetColor(intensity):
        red = green = blue = 1.0
        if intensity < 0.25:
          blue = 0.0
        elif intensity < 0.5:
          red = 0.0
          blue = 1 + 4 * ( 0.25 - intensity)
          #red = intensity / 0.5
          #blue = 0.3 + 1.6 * intensity
          #green = 0.3 + 0.3 * intensity
        elif intensity < 0.75:
          red = 4 * (intensity - 0.5)
          blue = 0.0
          #red = 1.0
          #green = 1.0 - ( intensity - 0.5 ) / 0.5
          #blue = 0.3 + 0.3 * ( 1.0 - intensity )
        else:
          green = 1 + 4 * (0.75 - intensity)
          blue = 0
          #green = 0.0
          #blue = 0.0
        return (red, green, blue)
