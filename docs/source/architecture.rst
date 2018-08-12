Architecture
**************
Architecture documentation. The Add-on follows classical model-view-controller pattern. 


Model
==========

The model consists of the classes that represent an actual network: Cells, connections between them (Projections), Populations of cells and Networks

High level model
---------------------------------------

.. autoclass:: neuron_visualization_addon.model.Network.Network
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: neuron_visualization_addon.model.Population.Population
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: neuron_visualization_addon.model.Cell.Cell
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: neuron_visualization_addon.model.Projection.Projection
    :members:
    :undoc-members:
    :show-inheritance:


NeuroML2 model
---------------------------------------

.. autoclass:: neuron_visualization_addon.model.NetworkNeuroML2.NetworkNeuroML2
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: neuron_visualization_addon.model.PopulationNeuroML2.PopulationNeuroML2
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: neuron_visualization_addon.model.CellNeuroML2.CellNeuroML2
    :members:
    :undoc-members:
    :show-inheritance:



Helper classes
---------------------------------------

.. autoclass:: neuron_visualization_addon.model.ColorMap.ColorMap
    :members:
    :undoc-members:
    :show-inheritance:

View
==========

Blender Panel
---------------------------------------
.. autoclass:: neuron_visualization_addon.__init__.PanelSettings
    :members:
    :undoc-members:

Controller
==========


Parser
---------------------------------------

.. autoclass:: neuron_visualization_addon.controller.Parser.Parser
    :members:
    :undoc-members:
    :show-inheritance:

