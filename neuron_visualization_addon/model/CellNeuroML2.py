import bpy, bmesh, os, sys
import neuroml
import mathutils
import neuroml.loaders as loaders
from neuron_visualization_addon.model.Cell import Cell

class CellNeuroML2(Cell):
    '''
    This class represents brain cells in the network
    '''
    def __init__(self, cell):
        Cell.__init__(self, cell.id)
        #if id not in Cell.generated_models:
        # Remove the dummy soma
        self.blender_obj.select = True
        bpy.ops.object.delete()
        # Parse new model
        self.parse_model(cell)

    def make_soma(self, size, location):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, size=size, location=location)
        # Name object as cell
        bpy.context.object.name = self.id
        # Save referrence
        self.blender_obj = bpy.context.object

    def draw_segment(self, size, bezier):
        # Create curve, curve object and set Cell as a parent
        cu = bpy.data.curves.new('AxonCurve', 'CURVE')
        ob = bpy.data.objects.new('AxonObject', cu)
        bpy.context.scene.objects.link(ob)
        ob.parent = self.blender_obj

        # Create bevel object
        bpy.ops.curve.primitive_bezier_circle_add(radius=size)
        cu.bevel_object = bpy.context.object

        # Create spline and set Bezier control points
        spline_axon = cu.splines.new('BEZIER')
        spline_axon.bezier_points[0].co = spline_axon.bezier_points[0].handle_left = spline_axon.bezier_points[0].handle_right = bezier[0]
        spline_axon.bezier_points.add(len(bezier) - 1)
        for n in range(len(bezier)-1):
            bpt = spline_axon.bezier_points[n+1]
            bpt.co = bpt.handle_left = bpt.handle_right = bezier[n+1]

    def parse_model(self, cell):
        '''
        Parse cell into a blender object
        '''
        # Dictionary of segment ids and locations
        # TODO fix measuremt units
        cell_dict = {}
        axon = []
        parent_found = False
        for segment in cell.morphology.segments:
            if(len(cell_dict) > 500):
                break
            cell_dict[segment.id] = segment
            if segment.parent == None:
                # Read parameters
                distal_vector = segment.distal
                size = distal_vector.diameter / 10.0
                location = mathutils.Vector((distal_vector.x, distal_vector.y, distal_vector.z)) / 10.0
                # Make soma
                self.make_soma(size, location)
            elif segment.proximal == None:
                # Read cell parameters
                distal_vector = segment.distal
                size = distal_vector.diameter / 10.0
                cell_location = mathutils.Vector((distal_vector.x, distal_vector.y, distal_vector.z)) / 10.0
                # Read parent parameters
                distal_parent = cell_dict[segment.parent.segments].distal
                parent_location = mathutils.Vector((distal_parent.x, distal_parent.y, distal_parent.z)) / 10.0
                # Construct the bezier curve
                axon = [parent_location, cell_location]
                # Draw the segment
                self.draw_segment(size,axon)
            else:
                # Read cell parameters
                distal_vector = segment.distal
                size = distal_vector.diameter / 10.0
                distal_location = mathutils.Vector((distal_vector.x, distal_vector.y, distal_vector.z)) / 10.0
                # Read parent parameters
                proximal_vector = segment.proximal
                proximal_location = mathutils.Vector((proximal_vector.x, proximal_vector.y, proximal_vector.z)) / 10.0
                # Construct the bezier curve
                axon = [proximal_location, distal_location]
                # Draw the segment
                self.draw_segment(size,axon)
