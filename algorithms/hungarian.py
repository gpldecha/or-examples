import numpy as np
import scipy.optimize, sys
import matplotlib.pyplot as plt

def main():

    x = np.linspace(0, 10, 4)

    xv, yv = np.meshgrid(x,x)

    points = np.zeros((x.size**2, 2))
    points[:, 0] = xv.flatten()
    points[:, 1] = yv.flatten()

    num_points = points.shape[0]

    # compute distance matrix
    C = np.zeros((num_points, num_points))
    for i in range(num_points):
        for j in range(num_points):
            if i != j:
                C[i, j] = np.linalg.norm(points[i, :] - points[j, :])

    np.fill_diagonal(C, 1000)

    print C

    row_ind, col_ind = scipy.optimize.linear_sum_assignment(C)
    assignmets = zip(row_ind, col_ind)



    plt.figure()
    plt.scatter(points[:, 0], points[:, 1])

    for i, j in enumerate(assignmets):
        line = np.vstack(( points[i, :], points[j, :] ))
        plt.plot(line[:, 0], line[:, 1])


    plt.show()


if __name__ == '__main__':
    main()

