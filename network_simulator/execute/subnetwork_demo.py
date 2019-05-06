from network_simulator.GraphBuilder import GraphBuilder
from network_simulator.PatientGenerator import PatientGenerator
from network_simulator.OrganGenerator import OrganGenerator
from network_simulator.WaitList import WaitList
from network_simulator.OrganList import OrganList
from network_simulator.GenerateSubnetwork import GenerateSubnetwork


network = GraphBuilder.graph_builder(20)
wait_list = WaitList()
organ_list = OrganList()

PatientGenerator.generate_patients(network, 10, wait_list)
OrganGenerator.generate_organs(network, 5, organ_list)

print(network)
print(wait_list)
print(organ_list)


# print(isinstance(wait_list, WaitList), isinstance(organ_list, OrganList))
# print(type(wait_list), type(organ_list))

patient_network = GenerateSubnetwork.generate_subnetwork(network, wait_list)
print(patient_network)

organ_network = GenerateSubnetwork.generate_subnetwork(network, organ_list)
print(organ_network)
