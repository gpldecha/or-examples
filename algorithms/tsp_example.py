import  numpy as np

from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import matplotlib.pyplot as plt

# Distance callback
class CreateDistanceCallback(object):
  """Create callback to calculate distances between points."""
  def __init__(self, points):
    """Array of distances between points."""
    num_points = points.shape[0]
    self.matrix = np.zeros((num_points, num_points))
    for i in range(num_points):
        for j in range(num_points):
            if i != j:
                self.matrix[i, j] = np.linalg.norm(points[i, :] - points[j, :], 1)

  def Distance(self, i, j):
    return self.matrix[i, j]


def main():

    x = np.linspace(0, 10, 10)

    xv, yv = np.meshgrid(x, x)

    points = np.zeros((x.size ** 2, 2))
    points[:, 0] = xv.flatten()
    points[:, 1] = yv.flatten()

    tsp_size = points.shape[0]


    num_routes = 1    # The number of routes, which is 1 in the TSP.
    # Nodes are indexed from 0 to tsp_size - 1. The depot is the starting node of the route.
    depot = 0

    index_path = []

    # Create routing model
    if tsp_size > 0:
        routing = pywrapcp.RoutingModel(tsp_size, num_routes, depot)
        search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()

        # Setting first solution heuristic: the
        # method for finding a first solution to the problem.
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        # Create the distance callback, which takes two arguments (the from and to node indices)
        # and returns the distance between these nodes.

        dist_between_nodes = CreateDistanceCallback(points)
        dist_callback = dist_between_nodes.Distance
        routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)
        # Solve, returns a solution if any.
        assignment = routing.SolveWithParameters(search_parameters)
        if assignment:
          # Solution cost.
          print "Total distance: " + str(assignment.ObjectiveValue()) + " miles\n"
          # Inspect solution.
          # Only one route here; otherwise iterate from 0 to routing.vehicles() - 1
          route_number = 0
          index = routing.Start(route_number) # Index of the variable for the starting node.
          print index
          route = ''
          while not routing.IsEnd(index):
          # Convert variable indices to node indices in the displayed route.
            print routing.IndexToNode(index)
            index_path.append(index)

          # route += str(city_names[routing.IndexToNode(index)]) + ' -> '
            index = assignment.Value(routing.NextVar(index))
          #route += str(city_names[routing.IndexToNode(index)])
          #print "Route:\n\n" + route


          print 'index_path: ', index_path

          plt.figure()
          plt.scatter(points[:, 0], points[:, 1])

          plt.plot(points[index_path, 0], points[index_path, 1], '-k')

          plt.show()


        else:
          print 'No solution found.'
    else:
        print 'Specify an instance greater than 0.'



if __name__ == '__main__':
  main()