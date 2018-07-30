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

    def parse(self, filepath, colorMap):
        """Parses nml files (TODO: extend)

        :param filepath: file to be parsed
        :type filepath: string

        :returns: string -- indicate what was parsed
        """
        # Parsing network neuroml2 file
        if filepath[-8:] == '.net.nml' or filepath[-4:] == '.xml':
            # TODO
            network_file = loaders.NeuroMLLoader.load(filepath)
            if len(network_file.includes) != 0:
                self.loadCellsNeuroML2(os.path.dirname(filepath), network_file.includes)
            self.network = NetworkNeuroML2(network_file.networks[0])
            return "network"
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

    def loadCellsNeuroML2(self, dirpath, includes):
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
                tmp = CellNeuroML2(c)
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

    def rotateCamera(self, velocity=1):
        # Create path curve
        cam_location = bpy.data.objects['Camera'].location
        radius = math.sqrt(cam_location.y**2 + cam_location.x**2)
        centerOfMass = self.network.location
        bpy.ops.curve.primitive_bezier_circle_add(radius=radius, location=(centerOfMass.x, centerOfMass.y, cam_location.z))
        path = bpy.context.object
        # Assign path to camera
        bpy.data.objects['Camera'].parent = path
        bpy.data.objects['Camera'].location -= cam_location
        bpy.ops.object.parent_set(type='FOLLOW')
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        empty = bpy.context.object
        # Rotate camera to the correct position
        bpy.data.objects['Camera'].constraints.new(type='TRACK_TO')
        bpy.data.objects['Camera'].constraints['Track To'].target = empty
        bpy.data.objects['Camera'].constraints['Track To'].track_axis = 'TRACK_NEGATIVE_Z'
        bpy.data.objects['Camera'].constraints['Track To'].up_axis = 'UP_Y'
