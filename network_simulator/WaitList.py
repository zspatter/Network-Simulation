import heapq
import network_simulator.MatchIdentifier as mI
import network_simulator.PatientGenerator as gP
import network_simulator.BloodType


class WaitList:
    """
    A class that represents the wait list for all patients waiting on
    a donation. This list accepts all patients in need of organs (generic)
    """

    def __init__(self, wait_list=None):
        """
        Creates a WaitList object. If no wait_list parameter is provided,
        an empty list is created

        :param list wait_list: optional wait_list parameter (if preexisting list exists)
        """
        if wait_list is None:
            wait_list = list()

        self.wait_list = wait_list

    def get_prioritized_patients(self, organ):
        """
        Takes an organ as a parameter and searches the
        wait list for matches. All matches are added to a priority queue
        with the patient's priority attribute determining priority.

        The heapq is returned after the entire list has been iterated through

        :param Organ organ: object representing a prospective transplant
        :return: heapq (priority queue) with only patients whose needs match that of the parameters
        """
        queue = []

        for patient in self.wait_list:
            if patient.organ_needed is organ.organ_type and \
                    patient.blood_type.is_compatible_donor(organ.blood_type):
                heapq.heappush(queue, patient)

        heapq._heapify_max(queue)
        return queue

    def add_patient(self, patient):
        """
        Adds a patient to the existing wait list

        :param Patient patient: object to be added
        """
        if patient not in self.wait_list:
            self.wait_list.append(patient)
            return
        print('This patient isn\'t in the wait list!')

    def remove_patient(self, patient):
        """
        Removes a patient from the existing wait list

        :param Patient patient: object to be removed
        """
        if patient in self.wait_list:
            self.wait_list.remove(patient)
            return
        print('This patient is already in the wait list!')

    def generate_patients(self, graph, n):
        """
        Wrapper that calls the GeneratePatients.generate_patients function
        This is used to ensure the generated patients are added to the same wait list

        :param Network graph: network for patients to be allocated to
        :param int n: number of patients to generate
        """
        gP.PatientGenerator.generate_patients(graph, n, self)

    def __str__(self):
        string = ''
        for patient in self.wait_list:
            string += patient.__str__() + '\n'

        return string + '===============================\n'
