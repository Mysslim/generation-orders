from abc import abstractmethod

class IPseudoGenAlgorithm:
    
    @abstractmethod
    def get_current_volume(self):
        pass

    @abstractmethod
    def get_next_volume(self):
        # when calling this method, 
        # the algorithm should go to the next iteration
        pass


class CongruentMethod(IPseudoGenAlgorithm):
    def __init__(self, seed, a, c, m) -> None:
        self.__seed = seed
        self.__a = a
        self.__c = c
        self.__m = m

    def get_current_volume(self):
        return (self.__a * self.__seed + self.__c) % self.__m

    def get_next_volume(self):
        self.__seed = self.get_current_volume()
        return self.get_current_volume()

