import bpy, bmesh, os, sys
import neuroml
import mathutils
import neuroml.loaders as loaders
from neuron_visualization_addon.model.Cell import Cell

class CellNeuroML2(Cell):
    """
    This class represents brain cells in the network parsed from NeuroML2 files
    """
    bevel_objects = {}

    def __init__(self, cell, scale = 10):
        # Call super constructor
        Cell.__init__(self, cell.id)
        # Remove the dummy soma
        self.blender_obj.select = True
        bpy.ops.object.delete()
        # Parse new model
        self.parse_model(cell, scale)

    @property
    def location(self):
        """Location

        :param location: Cell location
        :type location: Vector | tuple
        """
        return self.blender_obj.location

    @location.setter
    def location(self, location):
        """Location setter

        :param location: New location
        :type location: Vector | tuple
        """
        self.blender_obj.location = location

    def setSpikes(self, spikes, colorMap='jet'):
        """:todo: Overwrite this method"""
        pass

    def make_soma(self, size, location):
        """Make soma of the cell

        :param size: Soma size / radius
        :type size: float
        :param location: New location
        :type location: Vector | tuple
        """
        bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=8, size=size, location=location)
        # Name object as cell
        bpy.context.object.name = self.id
        # Save referrence
        self.blender_obj = bpy.context.object

    def draw_segment(self, size, bezier):
        """Draw segment of the cell of given size and bezier points

        :param size: Segment size or connection radius
        :type size: float
        :param bezier: List of bezier points [(control, handle_left, handle_right)]
        :type bezier: list
        """
        # Create curve, curve object and set Cell as a parent
        cu = bpy.data.curves.new('AxonCurve', 'CURVE')
        ob = bpy.data.objects.new('AxonObject', cu)
        bpy.context.scene.objects.link(ob)
        ob.parent = self.blender_obj

        # Create bevel object
        if not size in CellNeuroML2.bevel_objects:
            bpy.ops.curve.primitive_bezier_circle_add(radius=size)
            CellNeuroML2.bevel_objects[size] = bpy.context.object
            CellNeuroML2.bevel_objects[size].hide = True

        cu.bevel_object = CellNeuroML2.bevel_objects[size]
        cu.bevel_resolution = 1
        # Create spline and set Bezier control points
        spline_axon = cu.splines.new('BEZIER')
        spline_axon.bezier_points[0].co = spline_axon.bezier_points[0].handle_left = spline_axon.bezier_points[0].handle_right = bezier[0]
        spline_axon.bezier_points.add(len(bezier) - 1)
        for n in range(len(bezier)-1):
            bpt = spline_axon.bezier_points[n+1]
            bpt.co = bpt.handle_left = bpt.handle_right = bezier[n+1]

    def parse_model(self, cell, scale):
        """Parse cell model

        :param cell: Cell description object
        :type cell: NeuroML2 Cell
        """
        # Dictionary of segment ids and locations
        cell_dict = {}
        axon = []
        for segment in cell.morphology.segments:

            # Cell dictionary
            cell_dict[segment.id] = segment
            # Read parameters
            distal_vector = segment.distal
            size = distal_vector.diameter / scale
            distal_location = mathutils.Vector((distal_vector.x, distal_vector.y, distal_vector.z)) / scale
            if segment.parent == None:
                # Soma
                self.make_soma(size, distal_location)
            else:
                # Segment
                vector = None
                if segment.proximal == None:
                    # Get parent vector
                    vector = cell_dict[segment.parent.segments].distal
                else:
                    # Get proximal vector
                    vector = segment.proximal
                # Extract location
                location = mathutils.Vector((vector.x, vector.y, vector.z)) / scale
                if len(axon) == 0 or axon[-1] != location:
                    axon = [location, distal_location]
                else:
                    axon.append(distal_location)

                # Draw the segment
                self.draw_segment(size,axon)
