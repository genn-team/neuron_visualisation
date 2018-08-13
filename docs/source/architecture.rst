Architecture
**************
Architecture documentation. The Add-on follows classical model-view-controller pattern. 


Model
==========

The model consists of the classes that represent an actual network: 

* Cells
* Connections between them (Projections)
* Populations of cells
* Networks

as well as description language specific classes and helper classes, like ColorMap.

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

The view consists of classes that are responsible for generating UI. Currently, the only view that is available is the Blender Panel. It consists of the MainPanel class and helper classes.

Blender Panel
---------------------------------------
.. image:: img\\screen3.png
   :scale: 75 %
   :alt: alternate text
   :align: center

.. autoclass:: neuron_visualization_addon.__init__.MainPanel
    :members:
    :undoc-members:

.. autoclass:: neuron_visualization_addon.__init__.PanelSettings
    :members:
    :undoc-members:


Controller
==========

The controller is responsible for changing the model depending on user input.

Parser
---------------------------------------

.. autoclass:: neuron_visualization_addon.controller.Parser.Parser
    :members:
    :undoc-members:
    :show-inheritance:

