import bpy, bmesh, os, sys
import numpy as np
import neuroml, math
import neuroml.loaders as loaders

from neuron_visualization_addon.model.CellNeuroML2 import CellNeuroML2
from neuron_visualization_addon.model.NetworkNeuroML2 import NetworkNeuroML2
from neuron_visualization_addon.model.Cell import Cell
from neuron_visualization_addon.model.ColorMap import ColorMap

class Parser(object):
    """
    This class represents a brain cell in the network
    """

    def parse(self, filepath, scale, colorMap):
        """Parses nml files (TODO: extend)

        :param filepath: file to be parsed
        :type filepath: string

        :returns: string -- indicate what was parsed
        """
        # Parsing network neuroml2 file
        if filepath[-8:] == '.net.nml' or filepath[-4:] == '.xml':
            network_file = loaders.NeuroMLLoader.load(filepath)
            loaded_cells = {}
            if len(network_file.includes) != 0:
                loaded_cells = self.loadCellsNeuroML2(os.path.dirname(filepath), network_file.includes, scale)
            print("Loaded Cells:")
            print(loaded_cells)
            self.network = NetworkNeuroML2(network_file.networks[0], scale, loaded_cells)
            return "network"
        elif filepath[-9:] == '.cell.nml':
            cell = loaders.NeuroMLLoader.load(filepath)
            self.cell_dict = {}
            for c in cell.cells:
                tmp = CellNeuroML2(c, scale)
                self.cell_dict[tmp.id] = tmp
        # Parsing of animation file .st
        elif filepath[-3:] == '.st':
            activation_file = np.loadtxt(filepath)
            spikes = {}
            for line in activation_file:
                if not line[1] in spikes:
                    spikes[line[1]] = np.array([[line[0],1.0]])
                else:
                    spikes[line[1]] = np.append(spikes[line[1]],[[line[0],1.0]],axis=0)
            self.network.animateSpikes(spikes, colorMap)
            return "activation"
        # Parsing of animation file .cmp
        elif filepath[-4:] == '.cmp':
            activation_file = np.loadtxt(filepath)
            voltages = activation_file[:,1:]
            activation_file[:,1:] = (voltages - np.min(voltages)) / (np.max(voltages) - np.min(voltages))
            spikes = {i: np.transpose(np.append([activation_file[:,0]],[activation_file[:,i+1]],axis=0)) for i in range(len(activation_file[0])-1)}
            self.network.animateSpikes(spikes)
            return "activation"

    def loadCellsNeuroML2(self, dirpath, includes, scale):
        """Load cells from neuroml2

        :param dirpath: path to include directory
        :type dirpath: string

        :returns: dict -- dictionary of Cell objects
        """
        cell_dict = {}
        for include in includes:
            if include.href[-9:] != '.cell.nml':
                continue
            cell = loaders.NeuroMLLoader.load(os.path.join(dirpath,include.href))
            for c in cell.cells:
                tmp = CellNeuroML2(c, scale)
                cell_dict[tmp.id] = tmp
        return cell_dict

    @property
    def populations(self):
        """List of IDs of all populations
        """
        return self.network.populations.keys()

    @property
    def colorMaps(self):
        """List of color maps
        """
        return ColorMap.mapsList

    def highlightPopulation(self, populationID):
        """Hightlight a population

        :param populationID: population ID which to be highlighted
        :type populationID: string

        """
        if populationID == 'All':
            self.network.highlightPopulationsAll()
        elif populationID == 'None':
            self.network.removeHighlightAll()
        else:
            self.network.highlightPopulation(populationID)

    def pullProjections(self, strength):
        """Pull projections between populations into a "sand-clock" form

        :param strength: Pulling strength
        :type strength: int
        """
        self.network.pullProjectionsAll(strength)

    def rotateCamera(self):
        """Rotate camera around the network
        """
        cam_obj = bpy.data.objects['Camera']
        cam_location = cam_obj.location

        # Create path curve
        radius = math.sqrt(cam_location.y**2 + cam_location.x**2)
        centerOfMass = self.network.location
        bpy.ops.curve.primitive_bezier_circle_add(radius=radius, location=(centerOfMass.x, centerOfMass.y, cam_location.z))
        path = bpy.context.object

        # Assign path to camera
        bpy.context.scene.objects.active = cam_obj
        cam_obj.location -= cam_location
        follow_constaint = cam_obj.constraints.new('FOLLOW_PATH')
        follow_constaint.target = path
        override = {'constraint':follow_constaint,
                    'window':bpy.context.window,
                    'area':bpy.context.area,
                    'scene':bpy.context.scene,
                    'object':bpy.context.object,
                    'screen':bpy.context.screen}
        bpy.ops.constraint.followpath_path_animate(override,constraint='Follow Path')

        # Rotate camera to the correct position
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(centerOfMass.x, centerOfMass.y, cam_location.z))
        empty = bpy.context.object
        track_constraint = cam_obj.constraints.new(type='TRACK_TO')
        track_constraint.target = empty
        track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
        track_constraint.up_axis = 'UP_Y'

    def adjustCameraSpeed(self, velocity = 100):
        """Adjust camera rotation velocity

        :param velocity: Rotation speed in frames
        :type velocity: int
        """
        path = bpy.data.objects['Camera'].constraints['Follow Path'].target
        path.data.path_duration = velocity
