import abc

class ColorMap(abc.ABC):
    """Abstract color map class.
    """
    
    @abc.abstractmethod
    def getColor(intensity):
        pass
