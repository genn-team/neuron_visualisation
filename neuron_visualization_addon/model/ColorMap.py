class ColorMap(object):
    """Color map for the animation
    """

    def getColor(intensity,colorMap='jet'):
        if colorMap == 'jet':
            return ColorMap.jetColor(intensity)

    def jetColor(intensity):
        #TODO: check input
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
