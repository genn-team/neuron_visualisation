class ColorMap(object):
    """Color map for the animation

    In order to augment the list of color maps, define your own function within
    this class and add it to the mapsList dictionary

    :param mapsList: list of available maps
    :type mapsList: list
    """
    def jetColor(intensity):
        """Calculates jet color based on firing intensity

        :param intensity: Firing intensity between 0 and 1
        :type intensity: float

        :returns: tuple -- rgb color
        """

        if not 0 <= intensity <= 1:
            raise ValueError('Intensity is not betwen 0 and 1')

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

    mapsList = {"jet": jetColor}

    def getColor(intensity,colorMap='jet'):
        """Return the color that corresponds to the intensity
        in a specified color map

        :param intensity: Firing intensity between 0 and 1
        :type intensity: float
        :param colorMap: color map
        :type colorMap: string

        :returns: tuple -- rgb color
        """
        if not 0 <= intensity <= 1:
            raise ValueError('Intensity is not betwen 0 and 1')

        if not colorMap in ColorMap.mapsList:
            raise ValueError('Invalid color map')

        return ColorMap.mapsList[colorMap](intensity)
