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
        bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=8, size=size, location=location)
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
        cu.bevel_object.hide = True
        cu.bevel_resolution = 1

        # Create spline and set Bezier control points
        spline_axon = cu.splines.new('BEZIER')
        spline_axon.bezier_points[0].co = spline_axon.bezier_points[0].handle_left = spline_axon.bezier_points[0].handle_right = bezier[0]
        spline_axon.bezier_points.add(len(bezier) - 1)
        for n in range(len(bezier)-1):
            bpt = spline_axon.bezier_points[n+1]
            bpt.co = bpt.handle_left = bpt.handle_right = bezier[n+1]

        # Change context to console
        old_context = bpy.context.area.type
        bpy.context.area.type = 'CONSOLE'
        # Convert curve to mesh
        ob.select = True
        bpy.ops.object.convert(target='MESH')
        # Apply decimate modifier
        ob.modifiers.new('MyDecimate','DECIMATE')
        ob.modifiers[0].ratio = 0.01
        # Change context back
        bpy.context.area.type = old_context

    def parse_model(self, cell):
        '''
        Parse cell into a blender object
        '''
        # TODO fix measuremt units

        # Dictionary of segment ids and locations
        cell_dict = {}
        axon = []

        for segment in cell.morphology.segments:
            if(len(cell_dict) > 200):
                break

            # Cell dictionary
            cell_dict[segment.id] = segment
            # Read parameters
            distal_vector = segment.distal
            size = distal_vector.diameter / 10.0
            distal_location = mathutils.Vector((distal_vector.x, distal_vector.y, distal_vector.z)) / 10.0

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
                location = mathutils.Vector((vector.x, vector.y, vector.z)) / 10.0

                if len(axon) == 0 or axon[-1] != location:
                    axon = [location, distal_location]
                else:
                    axon.append(distal_location)

                # Draw the segment
                self.draw_segment(size,axon)

        # Change context to console
        old_context = bpy.context.area.type
        bpy.context.area.type = 'CONSOLE'
        # Join everything together
        self.blender_obj.select = True
        bpy.ops.object.select_hierarchy(direction='CHILD')
        bpy.ops.object.join()
        # Change back
        bpy.context.area.type = old_context
