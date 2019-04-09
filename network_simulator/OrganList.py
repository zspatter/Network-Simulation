import network_simulator.GenerateOrgans as GO


class OrganList:
    """
    A class that represents all of the available organs waiting to be
    allocated to compatible recipients. This list accepts all organ types (generic)
    """

    def __init__(self, organ_list=None):
        """
        Creates a OrganList object. If no organ_list parameter is provided,
        an empty list is created

        :param list organ_list: optional organ_list parameter (if preexisting list exists)
        """
        if organ_list is None:
            organ_list = list()

        self.organ_list = organ_list

    def add_organ(self, organ):
        """
        Adds an organ to the existing organ list

        :param Organ organ: object to be added to the organ list
        """
        self.organ_list.append(organ)

    def remove_organ(self, organ):
        """
        Removes an organ from the existing organ list

        :param Organ organ: object to be removed from the organ list
        """
        self.organ_list.remove(organ)

    def generate_organs(self, graph, n):
        """
        Wrapper that calls the GenerateOrgans.generate_organs function
        This is used to ensure the generated organs are added to the same organ list

        :param Network graph: network for patients to be allocated to
        :param int n: number of patients to generate
        """
        GO.GenerateOrgans.generate_organs(graph, n, self)
