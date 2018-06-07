import bpy

class Projection(object):
    '''
    This class represents a projection between neurons in the network
    '''
    def __init__(self, parent_object):
        # --- Axon ---
        # Create curve, curve object and set Cell as a parent
        self.curve = bpy.data.curves.new('AxonCurve', 'CURVE')
        self.object = bpy.data.objects.new('AxonObject', self.curve)
        bpy.context.scene.objects.link(self.object)
        self.object.parent = parent_object
        self.object.hide = True

        # --- Taper curve ---
        self.curve_taper = bpy.data.curves.new('TaperCurve', 'CURVE')
        self.taper = bpy.data.objects.new('TaperObject', self.curve_taper)
        bpy.context.scene.objects.link(self.taper)
        self.taper.hide = True

        taper_points = [
            ((-1.0,0.0,0.0), (-1.5,-0.5,-0.0), (-0.5,0.5,0.0)),
            ((1.0,0.0,0.0), (0.0026, 0.2423, 0.2013), (1.9536, 0.2317, 0.1925))
        ]

        # Create spline
        self.curve_taper.splines.new('BEZIER')
        self.updateTaperCurve(taper_points)
        self.curve.taper_object = self.taper


    def updateTaperCurve(self, taper_points):
        spline_taper = self.curve_taper.splines[0]
        diff = len(taper_points) - len(spline_taper.bezier_points)
        spline_taper.bezier_points.add(diff)
        for n in range(len(taper_points)):
            bpt = spline_taper.bezier_points[n]
            (bpt.co, bpt.handle_left, bpt.handle_right) = taper_points[n]


    def updateProjectionCurve(self, projection_points):
        spline_axon = self.curve.splines[0]
        diff = len(projection_points) - len(spline_axon.bezier_points)
        spline_axon.bezier_points.add(diff)
        for n in range(len(projection_points)):
            bpt = spline_axon.bezier_points[n]
            (bpt.co, bpt.handle_left, bpt.handle_right) = projection_points[n]


    def makeSimpleProjection(self, weight, destination):
        # Create bevel object
        bpy.ops.curve.primitive_bezier_circle_add(radius=weight)
        self.bevel_object = bpy.context.object
        self.curve.bevel_object = self.bevel_object
        self.bevel_object.hide = True

        self.object.hide = False

        # Control points for axon
        #start = self.object.parent.location
        destination = destination - self.object.parent.location
        axon = [
            (self.object.location, self.object.location, self.object.location),
            (destination , destination, destination)
        ]
        # Create spline and set Bezier control points
        self.curve.splines.new('BEZIER')
        self.updateProjectionCurve(axon)
        self.object.select = False

    def makeProjection(self, weight, projection):
        # Create bevel object
        bpy.ops.curve.primitive_bezier_circle_add(radius=weight)
        self.bevel_object = bpy.context.object
        self.curve.bevel_object = self.bevel_object
        self.bevel_object.hide = True

        self.object.hide = False

        # Create spline and set Bezier control points
        self.curve.splines.new('BEZIER')
        self.updateProjectionCurve(projection)
        self.object.select = False

    def setColor(self, color=(0.0,0.0,0.0)):
        # Color the axon in color
        material = bpy.data.materials.new("Color")
        material.diffuse_color = color
        self.object.active_material = material
