import bpy

class Projection(object):
    """
    This class represents a projection between neurons in the network
    """

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

        # --- Taper curve ---
        self.curve_taper = bpy.data.curves.new('TaperCurve', 'CURVE')
        self.taper = bpy.data.objects.new('TaperObject', self.curve_taper)
        bpy.context.scene.objects.link(self.taper)
        self.taper.hide = True

        # TODO
        taper_points = [
            ((-1.0,0.0,0.0), (-1.5,-0.5,-0.0), (-0.5,0.5,0.0)),
            ((1.0,0.0,0.0), (0.0026, 0.2423, 0.2013), (1.9536, 0.2317, 0.1925))
        ]

        # Create spline
        self.curve_taper.splines.new('BEZIER')
        self.updateTaperCurve(taper_points)
        self.curve.taper_object = self.taper


    def updateTaperCurve(self, taper_points):
        """Updates taper curve (shape curve).

        :param taper_points: Array of points that define a bezier curve
        :type taper_points: array

        """
        spline_taper = self.curve_taper.splines[0]
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
        # Create bevel object
        bpy.ops.curve.primitive_bezier_circle_add(radius=weight,rotation=(0,90,0))
        self.bevel_object = bpy.context.object
        self.curve.bevel_object = self.bevel_object
        self.bevel_object.hide = True
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
        # Create bevel object
        bpy.ops.curve.primitive_bezier_circle_add(radius=weight)
        self.bevel_object = bpy.context.object
        self.curve.bevel_object = self.bevel_object
        self.bevel_object.hide = True
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

    def pullCenterTo(self, destination):
        """Pull center of the projection to a specific position

        :param destination: Where to pull project to
        :type start: Vector|tuple

        """
        # TODO: complex axons
        # Control points for axon
        start = self.curve.splines[0].bezier_points[0]
        end = point = self.curve.splines[0].bezier_points[-1]
        destination = destination - self.object.parent.location
        axon = [(start.co, destination, 2*destination-start.co),
                (end.co, destination, 2*destination-end.co)]
        start.handle_left_type = 'VECTOR'
        start.handle_right_type = 'VECTOR'
        self.updateProjectionCurve(axon)
