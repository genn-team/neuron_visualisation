import bpy

class Projection(object):
    """
    This class represents a projection between neurons in the network
    """
    # Global variables for the taper curve
    curve_taper = None
    taper = None
    # Global dictionary for the bevel objects
    bevel_objects = {}

    def __init__(self, parent_object):
        """The constructor.

        :param parent_object: Parent object - soma
        :type parent_object: Cell
        """
        # --- Axon ---
        # Create curve, curve object and set Cell as a parent
        self.curve = bpy.data.curves.new('AxonCurve', 'CURVE')
        self.object = bpy.data.objects.new('AxonObject_' + str(parent_object.name), self.curve)
        bpy.context.scene.objects.link(self.object)
        self.curve.dimensions = '3D'
        self.object.parent = parent_object
        self.object.hide = True

        # Initialize a global taper curve if it doesn't exist yet
        if Projection.taper == None:
            Projection.initTaper()

        # Set the taper_curve
        self.curve.taper_object = Projection.taper

    def initTaper():
        """Initialize global taper curve
        """
        # --- Taper curve ---
        Projection.curve_taper = bpy.data.curves.new('TaperCurve', 'CURVE')
        Projection.taper = bpy.data.objects.new('TaperObject', Projection.curve_taper)
        bpy.context.scene.objects.link(Projection.taper)
        Projection.taper.hide = True

        taper_points = [
            ((-1.0,0.1,0.0), (-2.0,0.1,0.0), (-0.5,0.1,-0.0)),
            ((1.0,0.01,0.0), (0.0,0.01,0.0), (2.0, 0.01, 0.0))
        ]
        # Create spline
        Projection.curve_taper.splines.new('BEZIER')
        Projection.updateTaperCurve(taper_points)

    def updateTaperCurve(taper_points):
        """Updates taper curve (shape curve).

        :param taper_points: Array of points that define a bezier curve
        :type taper_points: array

        """
        spline_taper = Projection.curve_taper.splines[0]
        # Add more points to the curve
        diff = len(taper_points) - len(spline_taper.bezier_points)
        spline_taper.bezier_points.add(diff)
        # Update the curve
        for n in range(len(taper_points)):
            bpt = spline_taper.bezier_points[n]
            (bpt.co, bpt.handle_left, bpt.handle_right) = taper_points[n]


    def updateProjectionCurve(self, projection_points):
        """Updates projection curve (axon).

        :param projection_points: Array of points that define a bezier curve
        :type projection_points: array

        """
        spline_axon = self.curve.splines[0]
        # Add more points to the curve
        diff = len(projection_points) - len(spline_axon.bezier_points)
        spline_axon.bezier_points.add(diff)
        # Update the curve
        for n in range(len(projection_points)):
            bpt = spline_axon.bezier_points[n]
            (bpt.co, bpt.handle_left, bpt.handle_right) = projection_points[n]


    def makeSimpleProjection(self, weight, destination):
        """Make simple projection: straight line between parent object and destination object.

        :param weight: Weight of the connection
        :type weight: float
        :param weight: Weight of the connection
        :type weight: float

        """
        # Get bevel object
        if not weight in Projection.bevel_objects:
            bpy.ops.curve.primitive_bezier_circle_add(radius=weight)
            Projection.bevel_objects[weight] = bpy.context.object
            Projection.bevel_objects[weight].hide = True

        self.curve.bevel_object = Projection.bevel_objects[weight]

        # Unhide the curve object
        self.object.hide = False
        # Control points for axon
        start = self.object.location
        destination = destination - self.object.parent.location # Switch to local coordinates
        middle = (start + destination) / 2
        axon = [
            (start, middle, 2 * middle - start),
            (destination , middle, 2 * middle - destination)
        ]
        # Create spline and set Bezier control points
        self.curve.splines.new('BEZIER')
        self.updateProjectionCurve(axon)
        self.object.select = False

    def makeProjection(self, weight, projection):
        """Make projection from defined bezier curve.

        :param weight: Weight of the connection
        :type weight: float
        :param projection: Array of bezier points
        :type weight: array

        """
        # Get bevel object
        if not weight in Projection.bevel_objects:
            bpy.ops.curve.primitive_bezier_circle_add(radius=weight)
            Projection.bevel_objects[weight] = bpy.context.object
            Projection.bevel_objects[weight].hide = True

        self.curve.bevel_object = Projection.bevel_objects[weight]
        # Unhide the curve object
        self.object.hide = False
        # Create spline and set Bezier control points
        self.curve.splines.new('BEZIER')
        self.updateProjectionCurve(projection)
        self.object.select = False

    def setColor(self, color=(0.0,0.0,0.0)):
        """Set RGB color.

        :param color: RGB color
        :type color: tuple

        """
        # Color the axon in color
        material = bpy.data.materials.new("Color")
        material.diffuse_color = color
        self.object.active_material = material

    @property
    def start(self):
        """Start of the projection (soma).

        :type start: Vector

        """
        return self.object.location + self.object.parent.location

    @property
    def destination(self):
        """Destination of the projection (receiving soma)

        :type start: Vector

        """
        return self.curve.splines[0].bezier_points[-1].co + self.object.parent.location

    @destination.setter
    def destination(self):
        point = self.curve.splines[0].bezier_points[-1]
        destination = destination - self.object.parent.location
        # TODO fix the handles
        point.co = point.handle_left = point.handle_right = destination

    @property
    def middle(self):
        """Middle of the projection

        :type start: Vector
        """
        return 1/2 * (self.start + self.destination)

    def pullCenterTo(self, destination, pull):
        """Pull center of the projection to a specific position

        :param destination: Where to pull project to
        :type start: Vector|tuple

        """
        # TODO: complex axons
        # Control points for axon
        start = self.curve.splines[0].bezier_points[0]
        end = point = self.curve.splines[0].bezier_points[-1]
        destination = destination - self.object.parent.location
        axon = [(start.co, start.co, pull * destination + (1 - pull) * start.co),
                (end.co, pull * destination + (1 - pull) * end.co, end.co)]
        start.handle_left_type = 'VECTOR'
        start.handle_right_type = 'VECTOR'
        self.updateProjectionCurve(axon)

    def spike(self, time, minColor, maxColor):
        """Propagate potential from parent cell to receiving cells

        :param time: Where to spike
        :type time: float
        :param minColor: Color for resting state
        :type minColor: tuple
        :param maxColor: Color for a spike
        :type maxColor: tuple

        """
        if len(minColor) == 3:
            minColor += (1,)
        if len(maxColor) == 3:
            maxColor += (1,)
        bpy.data.scenes['Scene'].render.engine = 'CYCLES'
        material = bpy.data.materials.new('Material')
        material.use_nodes = True
        self.object.active_material = material
        # Texture coordinate node
        tex_node = material.node_tree.nodes.new(type='ShaderNodeTexCoord')
        # Mapping node
        map_node = material.node_tree.nodes.new(type='ShaderNodeMapping')
        # Color ramp node
        color_ramp_node = material.node_tree.nodes.new(type='ShaderNodeValToRGB')
        # Rotate texture
        map_node.rotation = (-3.1415,1.5707,3.1415)
        map_node.scale = (0.5,0.5,0.5)
        map_node.translation = (0., 0., 0.)
        map_node.keyframe_insert(data_path="translation", frame = time)
        map_node.translation = (4., 0., 0.)
        map_node.keyframe_insert(data_path="translation", frame = time + 4)
        # Set colors
        color_ramp_node.color_ramp.elements.new(position=0.5)
        color_ramp_node.color_ramp.elements[0].color = color_ramp_node.color_ramp.elements[2].color = minColor
        color_ramp_node.color_ramp.elements[1].color = maxColor
        # Connect
        diffuse_node = material.node_tree.nodes['Diffuse BSDF']
        material.node_tree.links.new(diffuse_node.inputs['Color'], color_ramp_node.outputs['Color'])
        material.node_tree.links.new(color_ramp_node.inputs['Fac'], map_node.outputs['Vector'])
        material.node_tree.links.new(map_node.inputs['Vector'], tex_node.outputs['Object'])
