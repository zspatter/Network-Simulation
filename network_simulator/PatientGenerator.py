import random

import network_simulator.BloodType as bT
import network_simulator.Patient as P
from network_simulator.CompatibilityMarkers import OrganType, BloodTypeLetter, BloodTypePolarity


class PatientGenerator:
    """
    Generates a variable number of patients in need of a transplant.
    The generated patients are distributed randomly across the network
    and are assigned a random blood type and priority value.
    """

    @staticmethod
    def generate_patients(graph, n, wait_list):
        """
        Generates n patients to add to wait list with random combinations of
        organ needed, blood type, priority, and location

        :param Network graph: network for patients to be allocated to
        :param int n: number of patients to generate
        :param WaitList wait_list:
        """
        # list of currently active nodes
        nodes = graph.nodes()

        for x in range(n):
            temp = P.Patient(patient_name="generated patient #" + str(x + 1),
                             illness="N/A",
                             organ_needed=OrganType.get_organ_type().value,
                             blood_type=bT.BloodType(BloodTypeLetter.get_blood_type(),
                                                     BloodTypePolarity.get_blood_polarity()),
                             priority=random.randrange(100 + n),
                             location=random.choice(nodes),
                             wait_list=wait_list)
