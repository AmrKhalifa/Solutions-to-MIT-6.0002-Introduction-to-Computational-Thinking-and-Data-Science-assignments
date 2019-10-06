# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer:
#


# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """

    # TODO
    print("Loading map from file...")
    digrahp = Digraph()
    with open (map_filename, 'r') as f:
        for line in f.readlines():
            line = line.split("\n")
            edge_info = line[0].split(" ")
            source_node = Node(edge_info[0])
            destin_node = Node(edge_info[1])
            edge = WeightedEdge(source_node, destin_node, int(edge_info[2]), int(edge_info[3]))
            if not digrahp.has_node(source_node):
                digrahp.add_node(source_node)
            if not digrahp.has_node(destin_node):
                digrahp.add_node(destin_node)

            digrahp.add_edge(edge)

    return digrahp

# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out

print(load_map('test_load_map.txt'))
#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer:
#

# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist,
                  best_path):

    pass


# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    # TODO

    def printAllPathsUtil(graph, u, d, visited, path, paths): 
      
            # Mark the current node as visited and store in path 
            #visited[u]= True
            visited.add(u[0])
            path.append(u) 
      
            # If current vertex is same as destination, then print 
            # current path[] 
            if u[0] == d : 
                paths.append(list(path))
            else: 
                # If current vertex is not destination 
                #Recur for all the vertices adjacent to this vertex
                #print("node not found, recuring ...")
                for i in graph.edges[u[0]]:
                    if not i.dest in visited:
                        printAllPathsUtil(graph, (i.dest, i), d, visited, path, paths)
            # Remove current vertex from path[] and mark it as unvisited 
            path.pop() 
            visited.remove(u[0]) 
        
    def printAllPaths(graph, s, d): 

        # Mark all the vertices as not visited 
        visited = set([])
        # Create an array to store paths 
        paths = []
        path = []
        x = 0
        # Call the recursive helper function to print all paths
        printAllPathsUtil(graph, (Node(s), x), Node(d), visited, path, paths)

        return paths

    def calcualte_path_total_dist(path):

        total_dist = 0
        for edge in path[1:]:
            total_dist += edge[1].get_total_distance()

        return total_dist


        pass

    def calculate_path_outdoor_dist(path):
        total_out_dist = 0
        for edge in path[1:]:
            total_out_dist += edge[1].get_outdoor_distance()
        return total_out_dist
        pass

    paths = printAllPaths(digraph, start, end)
    
    full_path_info = []

    for path in paths:
        full_path_info.append((path, calcualte_path_total_dist(path), calculate_path_outdoor_dist(path)))

    def get_best_path_from_sorted(paths, max_dist, max_outdoor_dist):

        paths = sorted(paths, key = lambda x: x[1])
        for path in paths:
            if path[1] <= max_dist and path[2] <= max_outdoor_dist:
                return list([str(x[0]) for x in path[0]])
            else:
                continue

        raise ValueError 



    return (get_best_path_from_sorted(full_path_info, max_total_dist, max_dist_outdoors))
    
    pass


# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    unittest.main()
    pass 