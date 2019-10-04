###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here
    cow_dic = {}
    with open(filename, 'r') as f:
        lines = f.read()
        lines = lines.split("\n")

        cow_list = [line.split(',') for line in lines]

        for cow in cow_list:
            cow_dic[cow[0]] = cow[1]
    
    return cow_dic

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    cow_list = [(k, int(v)) for k, v in cows.items()]

    cow_list.sort(key = lambda x: x[1], reverse = True)


    def fill_greedly(sorted_cows, limit = 10): 
        current_weight = 0 

        trip = []


        for cow in sorted_cows[:]:
            if current_weight + cow[1] <=  limit:
                trip.append(cow)
                current_weight += cow[1]
                sorted_cows.remove(cow) 
        return trip 

    trips = []

    start_time = time.time()
    while len(cow_list) > 0: 
        trip = fill_greedly(cow_list, limit)
        trips.append(trip)
    
    end_time = time.time()

    print("greedy took: ", end_time - start_time)
    print("no of trips with greedy is: ", len(trips))
    return trips

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    cow_list = [(k, int(v)) for k, v in cows.items()]

    cow_list.sort(key = lambda x: x[1], reverse = True)

    cow_list_copy = cow_list.copy()

    def get_power_set(array): 
        p_set = [[]]

        for item in array:
            new_set = [element + [item] for element in p_set]
            p_set.extend(new_set)

        return p_set


    def evaluate_set(array):
        solution_wieght = 0

        for element in array:

            solution_wieght += element[1]


        return solution_wieght 

    def get_best (array):
        power_set = get_power_set(array)

        solutions = [(solution, evaluate_set(solution)) for solution in power_set]

        for solution in solutions[:]:
            if solution[1] > limit:
                solutions.remove(solution)

        solutions.sort(key = lambda x: x[1], reverse = True)

        return solutions[0]

    trips = []

    start_time = time.time()

    while len(cow_list_copy) != 0:  
        trip, _ = get_best(cow_list_copy)
        trips.append(trip)
        for best_part in trip:
            cow_list_copy.remove(best_part)
    end_time = time.time()

    print("bruteforce took: ", end_time - start_time)
    print("no of trips with bruteforce is: ", len(trips))

    return trips 
    
        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    cows = load_cows("ps1_cow_data.txt")
    
    greedy_cow_transport(cows, limit = 10)
    brute_force_cow_transport(cows, limit = 10)
    pass


compare_cow_transport_algorithms()