import  numpy as np

from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import matplotlib.pyplot as plt

def create_data_array():

  locations = [[82, 76], [96, 44], [50, 5], [49, 8], [13, 7], [29, 89], [58, 30], [84, 39],
               [14, 24], [12, 39], [3, 82], [5, 10], [98, 52], [84, 25], [61, 59], [1, 65],
               [88, 51], [91, 2], [19, 32], [93, 3], [50, 93], [98, 14], [5, 42], [42, 9],
               [61, 62], [9, 97], [80, 55], [57, 69], [23, 15], [20, 70], [85, 60], [98, 5]]

  demands = [0, 19, 21, 6, 19, 7, 12, 16, 6, 16, 8, 14, 21, 16, 3, 22, 18,
             19, 1, 24, 8, 12, 4, 8, 24, 24, 2, 20, 15, 2, 14, 9]
  data = [locations, demands]
  return data

def distance(x1, y1, x2, y2):
    # Manhattan distance
    dist = abs(x1 - x2) + abs(y1 - y2)

    return dist

class CreateDistanceCallback(object):
  """Create callback to calculate distances between points."""

  def __init__(self, locations):
    """Initialize distance array."""
    size = len(locations)
    self.matrix = {}

    for from_node in xrange(size):
      self.matrix[from_node] = {}
      for to_node in xrange(size):
        x1 = locations[from_node][0]
        y1 = locations[from_node][1]
        x2 = locations[to_node][0]
        y2 = locations[to_node][1]
        self.matrix[from_node][to_node] = distance(x1, y1, x2, y2)

  def Distance(self, from_node, to_node):
    return self.matrix[from_node][to_node]

# Demand callback
class CreateDemandCallback(object):
  """Create callback to get demands at each location."""

  def __init__(self, demands):
    self.matrix = demands

  def Demand(self, from_node, to_node):
    return self.matrix[from_node]

def main():

    data = create_data_array()
    locations = data[0]
    demands = data[1]

    num_locations = len(locations)
    depot = 0
    num_vehicles = 5

    if num_locations > 0:
        routing = pywrapcp.RoutingModel(num_locations, num_vehicles, depot)
        search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()

        search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        dist_between_locations = CreateDistanceCallback(locations)
        dist_callback = dist_between_locations.Distance
        routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)

        # Put a callback to the demands.
        demands_at_locations = CreateDemandCallback(demands)
        demands_callback = demands_at_locations.Demand

        # Add a dimension for demand.
        slack_max = 0
        vehicle_capacity = 100
        fix_start_cumul_to_zero = True
        demand = "Demand"
        routing.AddDimension(demands_callback, slack_max, vehicle_capacity,
                             fix_start_cumul_to_zero, demand)

        # Solve, displays a solution if any.
        assignment = routing.SolveWithParameters(search_parameters)
        index_plot = []
        if assignment:
            # Display solution.
            # Solution cost.
            print "Total distance of all routes: " + str(assignment.ObjectiveValue()) + "\n"
            for vehicle_nbr in range(num_vehicles):
                idx = []
                index = routing.Start(vehicle_nbr)
                index_next = assignment.Value(routing.NextVar(index))
                idx.append(index_next)

                route = ''
                route_dist = 0
                route_demand = 0

                while not routing.IsEnd(index_next):
                    node_index = routing.IndexToNode(index)
                    idx.append(node_index)

                    node_index_next = routing.IndexToNode(index_next)
                    idx.append(node_index_next)

                    route += str(node_index) + " -> "
                    # Add the distance to the next node.
                    route_dist += dist_callback(node_index, node_index_next)
                    # Add demand.
                    route_demand += demands[node_index_next]
                    index = index_next
                    index_next = assignment.Value(routing.NextVar(index))

                index_plot.append(idx)
                node_index = routing.IndexToNode(index)
                node_index_next = routing.IndexToNode(index_next)
                route += str(node_index) + " -> " + str(node_index_next)
                route_dist += dist_callback(node_index, node_index_next)
                print "Route for vehicle " + str(vehicle_nbr) + ":\n\n" + route + "\n"
                print "Distance of route " + str(vehicle_nbr) + ": " + str(route_dist)
                print "Demand met by vehicle " + str(vehicle_nbr) + ": " + str(route_demand) + "\n"

            print data

            points = np.array(data[0])

            colors = ['-r', '-g', '-b', '-k', '-y']

            plt.figure()
            i = 0
            for idx in index_plot:
                plt.plot(points[idx, 0], points[idx, 1], colors[i])
                i=i+1

            plt.scatter(points[:, 0], points[:, 1])
            plt.scatter(points[depot, 0], points[depot, 1], s=100, c=[1, 0, 0], marker='s')
            plt.show()

        else:
            print 'No solution found.'
    else:
        print 'Specify an instance greater than 0.'

if __name__ == '__main__':
  main()