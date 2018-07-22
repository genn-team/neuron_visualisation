import bpy
from neuron_visualization_addon.model.Projection import Projection
from neuron_visualization_addon.model.JetColorMap import JetColorMap

class Cell(object):
    """
    This class represents a brain cell in the network
    """

    # --- Dictionary of generated models ---
    # generated_models = {}

    def __init__(self, id, location=(0,0,0)):
        """The constructor.

        :param id: The cell ID
        :type id: String
        :param location: Cell location
        :type location: Vector|tuple
        """
        self.id = id
    #    if id not in Cell.generated_models:
        # Create some placeholder
        bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, size=0.05, location=location)
        # Name the object as the cell
        bpy.context.object.name = self.id
        # Save the referrence
        self.blender_obj = bpy.context.object
        self.blender_obj.select = False
        # Initialization
        self.projectsTo = []
        self.receivesFrom = []
    #    else:
    #        Cell.generated_models[id].duplicate()
    #        self.blender_obj = bpy.context.object

    @property
    def location(self):
        """Location of the cell.

        :type location: Vector

        """
        return self.blender_obj.location

    @location.setter
    def location(self, location):
        """Location setter"""
        self.blender_obj.location = location
        for axon in self.receivesFrom:
            axon.updateDestination(location)

    def drawAxon(self, weight, destinationCell):
        """Draw an axon between this cell and destination cell.

        :param weight: The weight of a connection.
        :type weight: float
        :param destinationCell: Projection destionation cell.
        :type destinationCell: Cell

        :returns: Projection -- Created projection
        """
        # Create projection
        projection = Projection(self.blender_obj)
        projection.makeSimpleProjection(weight, destinationCell.location)
        # Save it
        self.projectsTo.append(projection)
        destinationCell.isProjectedTo(projection)

        return projection

    def isProjectedTo(self, projection):
        """Add projections from which the input is received.

        :param projection: Projection to be added
        :type projection: Projection

        """
        self.receivesFrom.append(projection)

    def setColor(self, color=(0.0,0.0,0.0)):
        """Set color

        :param color: RGB color
        :type color: tuple

        """
        material = bpy.data.materials.new("CellColor")
        material.diffuse_color = color
        self.blender_obj.active_material = material

    def setSpikes(self, spikes):
        # TODO: Clean up
        material = bpy.data.materials.new("CellColor")
        self.blender_obj.active_material = material
        for [time,intensity] in spikes:
            material.diffuse_color = JetColorMap.getColor(0.0)
            material.keyframe_insert(data_path="diffuse_color", frame = time-8)
            self.blender_obj.scale = (1., 1., 1.)
            self.blender_obj.keyframe_insert(data_path="scale", frame = time-8)
            material.diffuse_color = JetColorMap.getColor(intensity / 4)
            material.keyframe_insert(data_path="diffuse_color", frame = time-6)
            material.diffuse_color = JetColorMap.getColor(intensity / 2)
            material.keyframe_insert(data_path="diffuse_color", frame = time-4)
            material.diffuse_color = JetColorMap.getColor(intensity * 3 / 4)
            material.keyframe_insert(data_path="diffuse_color", frame = time-2)
            material.diffuse_color = JetColorMap.getColor(intensity)
            material.keyframe_insert(data_path="diffuse_color", frame = time)
            self.blender_obj.scale = (1.0, 1.0, 1.0)
            self.blender_obj.keyframe_insert(data_path="scale", frame = time)
            material.diffuse_color = JetColorMap.getColor(intensity * 3 / 4)
            material.keyframe_insert(data_path="diffuse_color", frame = time + 2)
            material.diffuse_color = JetColorMap.getColor(intensity / 2)
            material.keyframe_insert(data_path="diffuse_color", frame = time + 4)
            material.diffuse_color = JetColorMap.getColor(intensity / 4)
            material.keyframe_insert(data_path="diffuse_color", frame = time + 6)
            material.diffuse_color = JetColorMap.getColor(0.0)
            material.keyframe_insert(data_path="diffuse_color", frame = time + 8)
            self.blender_obj.scale = (1., 1., 1.)
            self.blender_obj.keyframe_insert(data_path="scale", frame = time + 8)
