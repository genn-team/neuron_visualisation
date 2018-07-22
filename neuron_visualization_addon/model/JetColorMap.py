from neuron_visualization_addon.model.ColorMap import ColorMap

class JetColorMap(ColorMap):
    """Jet color map class.
    """

    def getColor(intensity):
        """Calculates jet color based on firing intensity

        :param intensity: Firing intensity between 0 and 1
        :type intensity: float
        
        :returns: tuple -- rgb color
        """
        red = green = blue = 1.0
        if intensity < 0.25:
            red = 0.0
            green = 4 * intensity
        elif intensity < 0.5:
            red = 0.0
            blue = -4 * intensity + 2
        elif intensity < 0.75:
            blue = 0.0
            red = 4 * intensity - 2
        else:
            blue = 0.0
            green = -4 * intensity + 4
        return (red, green, blue)
