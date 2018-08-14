import bpy
from neuron_visualization_addon.model.Projection import Projection
from neuron_visualization_addon.model.ColorMap import ColorMap

class Cell(object):
    """
    This class represents a brain cell in the network
    """

    def __init__(self, id, location=(0,0,0)):
        """The constructor.

        :param id: The cell ID
        :type id: String
        :param location: Cell location
        :type location: Vector|tuple
        """
        self.id = id
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

    @property
    def location(self):
        """Location of the cell.

        :type location: Vector
        """
        return self.blender_obj.location

    @location.setter
    def location(self, location):
        """Location setter

        :param location: New location
        :type location: Vector | tuple
        """
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
        """Set RGB color

        :param color: RGB color
        :type color: tuple
        """
        material = bpy.data.materials.new("CellColor")
        material.diffuse_color = color
        self.blender_obj.active_material = material

    def setSpike(self, time, intensity, colorMap='jet', animateAxons=True):
        """Set cell to spike at a time with a specific intensity

        :param time: Frame of a spike
        :type time: float
        :param intensity: Intensity of a spike from 0 to 1
        :type intensity: float
        :param colorMap: Color map for intensities Visualization
        :type colorMap: string

        :todo: Neuron swelling without axon
        """
        if self.blender_obj.active_material == None:
            self.blender_obj.active_material = bpy.data.materials.new("CellColor")
        material = self.blender_obj.active_material
        multiplier = 0.0
        time_step = 5
        if len(self.projectsTo) > 0 and animateAxons:
            for i in range(len(self.projectsTo)):
                self.projectsTo[i].spike(time,ColorMap.getColor(0, colorMap), ColorMap.getColor(intensity, colorMap))
        for _ in range(5):
            material.diffuse_color = ColorMap.getColor(intensity * multiplier, colorMap)
            material.keyframe_insert(data_path="diffuse_color", frame = time - time_step)
            material.keyframe_insert(data_path="diffuse_color", frame = time + time_step)
            # ---- Neurons swelling ----
            #self.blender_obj.scale = (1. + multiplier/4, 1. + multiplier/4, 1. + multiplier/4)
            #self.blender_obj.keyframe_insert(data_path="scale", frame = time - time_step)
            #self.blender_obj.keyframe_insert(data_path="scale", frame = time + time_step)
            multiplier = multiplier + 0.25
            time_step = time_step - 1

    def setSpikes(self, spikes, colorMap='jet', animateAxons=True):
        """Set cell to spike at specific timse with a specific intensities

        :param spikes: Array with times is ms and spike intensities
        :type spikes: array
        :param colorMap: Color map for intensities Visualization
        :type colorMap: string
        """
        for [time,intensity] in spikes:
            self.setSpike(time,intensity,colorMap)
