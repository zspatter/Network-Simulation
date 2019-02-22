from Node import Node
import random
import time


# TODO #1 add support for functions to accept label (rather than just node_id)
# TODO #2 ensure generated network is ALWAYS connected initially
class Network:
    """
    A class representing a network (graph). A network is defined through
    a collection of nodes (and their adjacency dicts). A network consists
    of a unique graph ID, label, and network dict that contains all of the
    nodes contained within the graph.
    """

    def __init__(self, graph_id, label, network_dict=None):
        """
        Creates an instance of a Network

        :param int graph_id: unique identifier for a graph
        :param int/str label: name associated with a graph
        :param dict network_dict: {int node_id: Node, ...} (None by default)
        """
        self.graph_id = graph_id
        self.label = label
        if network_dict is None:
            network_dict = {}
        self.network_dict = network_dict

        # ensures adjacency lists mirror each other (undirected weighted edges)
        nodes = network_dict.keys()
        for node in nodes:
            adjacents = network_dict[node].get_adjacents()
            for adjacent in adjacents:
                if node in self.network_dict[adjacent].get_adjacents() \
                        and self.network_dict[adjacent].adjacency_dict[node] \
                        is self.network_dict[node].adjacency_dict[adjacent]:
                    continue
                else:
                    self.network_dict[adjacent].adjacency_dict[node] = self.network_dict[node].adjacency_dict[adjacent]

    def is_connected(self, nodes_encountered=None, start_node=None):
        """
        Returns bool indicating graph connectivity (path between all nodes).
        This is a recursive DFS.

        :param set nodes_encountered: set of node_id's encountered (None by default)
        :param int start_node: node_id of start of search (None by default)

        :return: bool
        """
        if nodes_encountered is None:
            nodes_encountered = set()
        nodes = self.nodes()
        if not start_node:
            # chose a vertex from network as start point
            start_node = nodes[0]
        nodes_encountered.add(start_node)
        if len(nodes_encountered) != len(nodes):
            for node in self.network_dict[start_node].get_adjacents():
                if node not in nodes_encountered:
                    if self.is_connected(nodes_encountered, node):
                        return True
        else:
            return True
        return False

    def DFS(self, node_id=None):
        """
        Returns bool indicating graph connectivity (path between all nodes).
        This is an iterative DFS.

        :param int node_id: identifies node where search will start (None by default)

        :return: bool
        """
        nodes_encountered = set()
        if not node_id:
            node_id = self.nodes()[0]
        stack = [node_id]
        while stack:
            node = stack.pop()
            if node not in nodes_encountered:
                nodes_encountered.add(node)
                # TODO: this adds all adjacents - this will cause repeat visits
                stack.extend(self.network_dict[node].get_adjacents())

        if len(nodes_encountered) != len(self.nodes()):
            return False
        else:
            return True

    def BFS(self, node_id=None):
        """
        Returns bool indicating graph connectivity (path between all nodes).
        This is an iterative BFS.

        :param int node_id: identifies node where search will start (None by default)

        :return: bool
        """
        # mark all the nodes as not visited (value is None)
        visited = dict.fromkeys(self.nodes())
        nodes_encountered = set()
        queue = []

        if not node_id:
            node_id = self.nodes()[0]

        # mark the source node as visited and enqueue it
        queue.append(node_id)
        visited[node_id] = True
        nodes_encountered.add(node_id)

        while queue:
            # dequeue a node from queue and add to nodes_encountered
            node_id = queue.pop(0)
            nodes_encountered.add(node_id)

            # all adjacents of current node are checked, if the node hasn't been
            # enqueued previously, node is enqueued and added to nodes_encountered
            for node in self.network_dict[node_id].get_adjacents():
                if visited[node] is None:
                    queue.append(node)
                    visited[node] = True
                    nodes_encountered.add(node)

        # if size of nodes_encountered equals size of nodes(), return True
        if len(nodes_encountered) == len(self.nodes()):
            return True
        else:
            return False

    def nodes(self):
        """
        Returns list of active nodes within the graph.

        :return: list
        """
        nodes = list(self.network_dict.keys())
        active_nodes = list()
        for node in nodes:
            if self.network_dict[node].status:
                active_nodes.append(node)
        return active_nodes

    @staticmethod
    def generate_network(n, graph_id=1, label='Generic Network'):
        """
        Returns randomly generated network with n nodes.

        :param int n: number of nodes generated graph will contain
        :param int graph_id: unique identifier for a graph (1 by default)
        :param int/str label: name associated with a graph ('Generic Network' by default)

        :return: network
        """
        network_dict = {}
        for x in range(1, n + 1):
            adjacency_dict = Network.generate_adjacency_dict(x, n)
            node = Node(x, 'Node #' + str(x), adjacency_dict)
            network_dict[x] = node
        network = Network(graph_id, label, network_dict)
        return network

    # this function generates an adjacency list consisting of 2-5 adjacencts
    @staticmethod
    def generate_adjacency_dict(node_id, total_nodes):
        """
        Returns randomly generated adjacency dict for an instance of a node.
        The generated adjacency list can contain a connection to any node
        in the graph (except itself). This will prevent parallel edges from
        being generated. A random number of edges between 5 and 25 (inclusive)
        will be generated and a random weight between 1 and 50 (inclusive)
        will be assigned to each edge.
        This is called by the generate_network function.

        :param int node_id: unique identifier for the node that the
            adjacency dict is being generated for
        :param int total_nodes: total number of nodes present in the generated graph

        :return: dict
        """
        adjacency_dict = {}
        for n in range(random.randint(5, 25)):
            random_node = random.randint(1, total_nodes)
            # ensures node doesn't add itself to adjacency_dict
            # or add a duplicate entry
            while node_id == random_node or any(random_node == x for x in adjacency_dict.keys()):
                random_node = random.randint(1, total_nodes)
            # updates adjacency dict to new format
            adjacency_dict[random_node] = {'weight': random.randint(1, 50), 'status': True}
        return adjacency_dict

    def add_node(self, node_id, label, adjacency_dict):
        """
        Adds a node with the passed parameters to the graph. If the
        node_id is already present in the graph, an error message
        is printed to the console.

        :param int node_id: unique identifier within a given graph
        :param int/str label: name associated with a node
        :param dict adjacency_dict: {int node_id: {'weight': int, 'status': bool}, ...}
        """
        # if node_id is unique, add it to the network
        if node_id not in self.network_dict:
            self.network_dict[node_id] = Node(node_id, label, adjacency_dict)

            # adds edges to the new node from the nodes in the adjacency list
            # (this ensures the edge is represented in both directions)
            for key in adjacency_dict:
                self.network_dict[key].adjacency_dict[node_id] = adjacency_dict[key]
        else:
            print(f'Node ID: #{node_id} is already present in this network. '
                  f'Node could not be added.')

    def remove_node(self, node_id):
        """
        Removes the node with the passed node_id from the graph. If node_id
        is not present in the graph, an error message is printed to the console.

        :param int node_id: unique identifier within a given graph
        """
        if node_id in self.network_dict:
            # gathers list of adjacent node id's
            adjacency_dict = self.network_dict[node_id].get_adjacents()

            # removes edges store on adjacent objects
            for key in adjacency_dict:
                del self.network_dict[key].adjacency_dict[node_id]

            # removes node object
            del self.network_dict[node_id]
            print(f'Node ID: #{node_id} and all of it\'s edges has been removed')
        else:
            print(f'Node ID: #{node_id} is not present in this network. '
                  f'Node could not be removed.')

    # add edge to both adjacency lists
    def add_edge(self, node_id1, node_id2, weight):
        """
        Adds an edge between two nodes with a specified weight. It is
        assumed that the added edge will be active. If there already
        exists an edge between the two nodes, an error message is printed
        to the console.

        :param int node_id1: unique identifier within a given graph
            (one of the vertices to be connected by the added edge)
        :param int node_id2: unique identifier within a given graph
            (one of the vertices to be connected by the added edge)
        :param int weight: cost associated with the edge
        """
        if node_id2 not in self.network_dict[node_id1].get_adjacents() \
                and node_id1 not in self.network_dict[node_id2].get_adjacents():
            self.network_dict[node_id1].adjacency_dict[node_id2] = {'weight': weight, 'status': True}
            self.network_dict[node_id2].adjacency_dict[node_id1] = {'weight': weight, 'status': True}
        else:
            print(f'There already exists an edge between Node ID: #{node_1} '
                  f'and Node ID: #{node_id2}. This edge could not be added.')

    def remove_edge(self, node_id1, node_id2):
        """
        Removes an edge between two nodes from the graph.

        :param int node_id1: unique identifier within a given graph
            (one of the vertices connected by the edge to be removed)
        :param int node_id2: unique identifier within a given graph
            (one of the vertices connected by the edge to be removed)
        """
        # TODO condition if edge (or node) doesn't exist
        del self.network_dict[node_id1].adjacency_dict[node_id2]
        del self.network_dict[node_id2].adjacency_dict[node_id1]

    """
    The following 4 functions toggle status of nodes and edges
    
    We will need to develop functions that check for status before executing
    for example, our functions that check graph connectivity or paths
    """
    # TODO verify node exists (already inactive?)
    def mark_node_inactive(self, node_id):
        """
        Marks all edges in the adjacency list of the specified node as
        inactive, then mirrors that status in the other adjacency lists.
        Finally, the specified node's status is marked as inactive.

        :param int node_id: unique identifier within a given graph
        """
        # gathers list of adjacent node id's
        adjacency_dict = self.network_dict[node_id].get_adjacents()

        # marks all edges of node as inactive, and mirrors
        # the status on all adjacents edges connected to the node
        for key in adjacency_dict:
            self.network_dict[key].adjacency_dict[node_id]['status'] = False
            self.network_dict[node_id].adjacency_dict[key]['status'] = False

        # marks node status as inactive
        self.network_dict[node_id].status = False
        print(f'Node ID: #{node_id} and all of it\'s edges has been marked inactive.')

    """
    How should we handle status if an edge is explicitly made inactive,
    then a connected node is made inactive, then eventually active again
    
    currently, the edge that was explicitly toggled off would be made active
    when the connected node is made active
    
    should node status take priority over edge status?
    """
    # TODO verify node exists (already active?)
    def mark_node_active(self, node_id):
        """
        Marks all adjacent edges connected with another active node as
        active, then marks the specified node as active.

        :param int node_id: unique identifier within a given graph
        """
        # gathers list of adjacent node id's
        adjacency_dict = self.network_dict[node_id].get_adjacents()

        # marks all edges of node as inactive, and mirrors
        # the status on all adjacents edges connected to the node
        for key in adjacency_dict:
            if self.network_dict[key].status is True:
                self.network_dict[key].adjacency_dict[node_id]['status'] = True
                self.network_dict[node_id].adjacency_dict[key]['status'] = True

        # marks node status as inactive
        self.network_dict[node_id].status = True
        print(f'Node ID: #{node_id} and all of it\'s edges has been marked active.')

    # TODO verify edge exists (already inactive?)
    def mark_edge_inactive(self, node_id1, node_id2):
        """
        Marks the specified edge as inactive in both adjacency lists.

        :param int node_id1: unique identifier within a given graph
        :param int node_id2: unique identifier within a given graph
        """
        self.network_dict[node_id1].adjacency_dict[node_id2]['status'] = False
        self.network_dict[node_id2].adjacency_dict[node_id1]['status'] = False

        print(f'The edge connecting Node ID: #{node_id1} and Node ID: #{node_id2} has been marked inactive.')

    # TODO verify edge exists (already active?)
    def mark_edge_active(self, node_id1, node_id2):
        """
        Marks the specified edge as active in both adjacency lists iff
        both connected nodes are active.

        :param int node_id1: unique identifier within a given graph
        :param int node_id2: unique identifier within a given graph
        """
        if self.network_dict[node_id1].status and self.network_dict[node_id2].status:
            self.network_dict[node_id1].adjacency_dict[node_id2]['status'] = True
            self.network_dict[node_id2].adjacency_dict[node_id1]['status'] = True
            print(f'The edge connecting Node ID: #{node_id1} and Node ID: #{node_id2} has been marked active.')
        else:
            print('One of the connecting nodes is inactive. As a result, this edge must remain inactive.')

    def __str__(self):
        """
        Returns an easily readable (formatted) string representation of
        the instance. Only active nodes and edges are represented. This
        calls the Node.__str__ function.

        :return: str
        """
        string = 'Graph ID: ' + str(self.graph_id) + ': ' + self.label
        for key in self.network_dict.keys():
            string += f'{self.network_dict[key].__str__()}'
        return string


"""
The lines below behave as the main method in Java

Everything below is just to briefly demonstrate/test
the basic functions of our graph/network
"""

# creates 10 individual nodes (hard coded adjacency lists to match)
node_1 = Node(1, 'A',
              {2: {'weight': 3, 'status': True},
               3: {'weight': 1, 'status': True},
               5: {'weight': 4, 'status': True},
               9: {'weight': 2, 'status': True}})
node_2 = Node(2, 'B',
              {1: {'weight': 3, 'status': True},
               4: {'weight': 2, 'status': True},
               5: {'weight': 3, 'status': True},
               7: {'weight': 9, 'status': True},
               8: {'weight': 10, 'status': True},
               9: {'weight': 4, 'status': True}})
node_3 = Node(3, 'C',
              {1: {'weight': 1, 'status': True},
               4: {'weight': 2, 'status': True},
               6: {'weight': 4, 'status': True},
               7: {'weight': 3, 'status': True}})
node_4 = Node(4, 'D',
              {2: {'weight': 2, 'status': True},
               3: {'weight': 2, 'status': True},
               6: {'weight': 8, 'status': True},
               10: {'weight': 4, 'status': True}})
node_5 = Node(5, 'E',
              {1: {'weight': 4, 'status': True},
               2: {'weight': 3, 'status': True},
               8: {'weight': 3, 'status': True},
               9: {'weight': 4, 'status': True}})
node_6 = Node(6, 'F',
              {3: {'weight': 4, 'status': True},
               4: {'weight': 8, 'status': True},
               9: {'weight': 8, 'status': True},
               10: {'weight': 2, 'status': True}})
node_7 = Node(7, 'G',
              {2: {'weight': 9, 'status': True},
               3: {'weight': 3, 'status': True},
               8: {'weight': 2, 'status': True},
               10: {'weight': 5, 'status': True}})
node_8 = Node(8, 'H',
              {2: {'weight': 10, 'status': True},
               5: {'weight': 3, 'status': True},
               7: {'weight': 2, 'status': True},
               9: {'weight': 4, 'status': True}})
node_9 = Node(9, 'I',
              {1: {'weight': 2, 'status': True},
               2: {'weight': 4, 'status': True},
               5: {'weight': 4, 'status': True},
               6: {'weight': 8, 'status': True},
               8: {'weight': 4, 'status': True}})
node_10 = Node(10, 'J',
               {4: {'weight': 4, 'status': True},
                6: {'weight': 2, 'status': True},
                7: {'weight': 5, 'status': True}})

# create a network consisting of the nodes above
network_1 = Network(1, 'Sample Network',
                    {node_1.node_id: node_1,
                     node_2.node_id: node_2,
                     node_3.node_id: node_3,
                     node_4.node_id: node_4,
                     node_5.node_id: node_5,
                     node_6.node_id: node_6,
                     node_7.node_id: node_7,
                     node_8.node_id: node_8,
                     node_9.node_id: node_9,
                     node_10.node_id: node_10})

# demonstrates __str__() function works
print(network_1.__str__() + '\n\n===============================\n')

# demonstrates remove_edge function works
print('\t---REMOVE EDGE---\n')
network_1.remove_edge(1, 2)
print(network_1.__str__() + '\n\n===============================\n')

# demonstrates remove_node function works
print('\t---REMOVE NODE---\n')
network_1.remove_node(3)
print(network_1.__str__() + '\n\n===============================\n')

# demonstrates add edge function works
print('\t---ADD EDGE---\n')
network_1.add_edge(1, 2, 15)
print(network_1.__str__() + '\n\n===============================\n')

# demonstrates the add node function works
print('\t---ADD NODE---\n')
network_1.add_node(11, 'K',
                   {1: {'weight': 3, 'status': True},
                    2: {'weight': 4, 'status': True},
                    10: {'weight': 8, 'status': True}})
print(network_1.__str__() + '\n\n===============================\n')


# demonstrates is_connected() function works
if network_1.is_connected():
    print("The network is connected!\n")
else:
    print("The network is not connected!\n")
start = time.time_ns()
print('Recursive DFS: ' + str(network_1.is_connected()))
end = time.time_ns()
print('\telapsed time: ' + str(end - start))

start = time.time_ns()
print('\nIterative DFS: ' + str(network_1.DFS()))
end = time.time_ns()
print('\telapsed time: ' + str(end - start))

start = time.time_ns()
print('\nIterative BFS: ' + str(network_1.BFS()))
end = time.time_ns()
print('\telapsed time: ' + str(end - start) + '\n\n===============================\n')

# creates disconnected network to further test is_connected()
node_a = Node(1, 'A',
              {2: {'weight': 1, 'status': True},
               3: {'weight': 2, 'status': True}})
node_b = Node(2, 'B',
              {3: {'weight': 1, 'status': True}})
node_c = Node(3, 'C',
              {1: {'weight': 2, 'status': True}})
node_d = Node(4, 'D')
disconnected_network = Network(1, 'Disconnected Network',
                               {1: node_a,
                                2: node_b,
                                3: node_c,
                                4: node_d})

# prints Disconnected Network and checks if graph is connected
print('\t---DISCONNECTED GRAPH---\n')
print(disconnected_network.__str__() + '\n\n===============================\n')

start = time.time_ns()
print('Recursive DFS: ' + str(disconnected_network.is_connected()))
end = time.time_ns()
print('\telapsed time: ' + str(end - start))

start = time.time_ns()
print('\nIterative DFS: ' + str(disconnected_network.DFS()))
end = time.time_ns()
print('\telapsed time: ' + str(end - start))

start = time.time_ns()
print('\nIterative BFS: ' + str(disconnected_network.BFS()))
end = time.time_ns()
print('\telapsed time: ' + str(end - start) + '\n\n===============================\n')

# tests the functionality in __init__ that ensures adjacency lists
# of separate nodes mirror each other (undirected, weighted edges)
init_tester_node1 = Node(1, "A",
                         {2: {'weight': 3, 'status': True},
                          3: {'weight': 5, 'status': True}})
init_tester_node2 = Node(2, "B",
                         {1: {'weight': 2, 'status': True},
                          4: {'weight': 3, 'status': True}})
init_tester_node3 = Node(3, "C",
                         {2: {'weight': 6, 'status': True},
                          4: {'weight': 9, 'status': True}})
init_tester_node4 = Node(4, "D",
                         {3: {'weight': 8, 'status': True},
                          2: {'weight': 4, 'status': True}})
init_tester_node5 = Node(5, "E",
                         {1: {'weight': 1, 'status': True},
                          4: {'weight': 2, 'status': True}})

init_tester = Network(1, "__init__ Test Network",
                      {init_tester_node1.node_id: init_tester_node1,
                       init_tester_node2.node_id: init_tester_node2,
                       init_tester_node3.node_id: init_tester_node3,
                       init_tester_node4.node_id: init_tester_node4,
                       init_tester_node5.node_id: init_tester_node5})

print('\t---ADJACENCY LISTS MIRROR TEST---\n')
print(init_tester.__str__() + '\n\n===============================\n')

print('\t---MARK EDGE BETWEEN NODE #1 AND #5 INACTIVE---\n')
init_tester.mark_edge_inactive(1, 5)
print(init_tester.__str__() + '\n\n===============================\n')

print('\t---MARK NODE #1 INACTIVE---\n')
init_tester.mark_node_inactive(1)
print(init_tester.__str__() + '\n\n===============================\n')

start = time.time_ns()
print('Recursive DFS: ' + str(init_tester.is_connected()))
end = time.time_ns()
print('\telapsed time: ' + str(end - start))

start = time.time_ns()
print('\nIterative DFS: ' + str(init_tester.DFS()))
end = time.time_ns()
print('\telapsed time: ' + str(end - start))

start = time.time_ns()
print('\nIterative BFS: ' + str(init_tester.BFS()))
end = time.time_ns()
print('\telapsed time: ' + str(end - start) + '\n\n===============================\n')

print('\t---MARK NODE #1 ACTIVE---\n')
init_tester.mark_node_active(1)
print(init_tester.__str__() + '\n\n===============================\n')


# tests the generate_network and generate_adjacency_list functions
# generated_network = Network.generate_network(5000)
# print('\t---GENERATED RANDOM NETWORK---\n')
# print(generated_network.__str__() + '\n\n===============================\n')
#
# # times iterative DFS and iterative BFS for comparison
# start = time.time_ns()
# print('\nIterative DFS: ' + str(generated_network.DFS()))
# end = time.time_ns()
# print('\telapsed time: ' + str(end - start))
#
# start = time.time_ns()
# print('\nIterative BFS: ' + str(generated_network.BFS()))
# end = time.time_ns()
# print('\telapsed time: ' + str(end - start))
