import bpy

class Cell():
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
    # --- Taper curve ---
    cu_taper = bpy.data.curves.new('TaperCurve', 'CURVE')
    taper = bpy.data.objects.new('TaperObject', cu_taper)
    bpy.context.scene.objects.link(taper)
    taper.hide = True

    taper_points = [
        ((-1.0,0.0,0.0), (-1.5,-0.5,-0.0), (-0.5,0.5,0.0)),
        ((1.0,0.0,0.0), (0.0026, 0.2423, 0.2013), (1.9536, 0.2317, 0.1925))
    ]

    # Create spline and set Bezier control points
    spline_taper = cu_taper.splines.new('BEZIER')
    spline_taper.bezier_points.add(len(taper_points)-1)
    for n in range(len(taper_points)):
        bpt = spline_taper.bezier_points[n]
        (bpt.co, bpt.handle_left, bpt.handle_right) = taper_points[n]
    # ------------------------------------------------------------------------

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

    def drawAxon(self, destination, weight):
        # ----- Axon -----
        # Create curve, curve object and set Cell as a parent
        cu = bpy.data.curves.new('AxonCurve', 'CURVE')
        ob = bpy.data.objects.new('AxonObject', cu)
        bpy.context.scene.objects.link(ob)
        ob.parent = self.blender_obj

        # Create bevel object
        bpy.ops.curve.primitive_bezier_circle_add(radius=weight)
        cu.bevel_object = bpy.context.object
        #cu.dimensions = '3D'

        # Control points for axon
        destination = destination - self.getLocation()
        axon = [
            (destination , (-0.0,-0.0,-0.0), (0.0,0.0,0.0))
        ]

        # Create spline and set Bezier control points
        spline_axon = cu.splines.new('BEZIER')
        spline_axon.bezier_points.add(len(axon))
        for n in range(len(axon)):
            bpt = spline_axon.bezier_points[n+1]
            (bpt.co, bpt.handle_left, bpt.handle_right) = axon[n]

        ob.select = False
        cu.taper_object = Cell.taper
