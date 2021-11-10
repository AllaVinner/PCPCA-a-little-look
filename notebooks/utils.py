import pandas as pd
import numpy as np


def plot_line(direction, start, ax, plot_kwargs):
    # plots a line on axis 'ax'.
    # The line is defined by the direction 'direction' and start point 'start'.
    # The direction and start should be 2x1 vectors but the only requierment is
    # that they are of size == 2 (They are reshaped to 2x1).
    # The function calculates the current size of the axis and plots the line
    # within those limits.

    # assertions of input vectors
    assert direction.size == 2
    assert start.size == 2

    # reshape input vectors
    direction = direction.reshape(2,1)
    start = start.reshape(2,1)
    
    # fetch limits from axis
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    
    # Calculate scalars (lambda) such that the direction reaches a limit.
    # e.g. x_min = lambda[0]*direction + start
    
    # Concatenate for simpler calculation
    lim_vec = np.array([x_min, y_min, x_max, y_max]).reshape(4,1)
    start_vec = np.vstack((start,start)).reshape(4,1)
    dir_vec = np.vstack((direction, direction)).reshape(4,1)
    # calculate lambdas
    lambdas = (lim_vec-start_vec)/dir_vec
    lambdas = lambdas.reshape(4)
    # Edge cases when the direction is parallel to the x or y axis (leads to division by zero)
    if direction[0] == 0:
        lambdas[0] == -np.inf
        lambdas[2] == np.inf
    if direction[1] == 0:
        lambdas[1] == -np.inf
        lambdas[3] == np.inf
    
    # two of the lamdas will be positive and two will be negative.
    # we want to pick the lesser extreme of both cases.
    sorted = np.sort(lambdas)
    min_lambda = sorted[1]
    max_lambda = sorted[2]

    # calculate edge points of the line
    p_min = min_lambda*direction + start
    p_max = max_lambda*direction + start

    # plot the line
    ax.plot([p_min[0], p_max[0]], 
            [p_min[1], p_max[1]],**plot_kwargs)



def read_toy_data():
    # Read toy data (fore- and background) from data folder and
    # package them into a datafram.
    # The dataframe has columns
    #   - x
    #   - y
    #   - Class (Case, Control)
    ###########################

    foreground_path = "../data/toy/foreground.csv"
    background_path = "../data/toy/background.csv"

    data = pd.read_csv(foreground_path, header= None).values
    X = pd.DataFrame(data = {'x' : data[0],
                             'y':data[1]})
    data = pd.read_csv(background_path, header= None).values
    Y = pd.DataFrame(data = {'x' : data[0],
                             'y':data[1]})
    X['class'] = 'Case'
    Y['class'] = 'Control'
    return pd.concat([X,Y], ignore_index=True)
    
def project_along_vector(data, vec):
    # Takes in a dxN matrix 'data' and a 
    # dx1 vector 'vec'
    # and outputs the projection of the columns of
    # data onto the vector.
    assert data.shape[0] == vec.shape[0]
    assert data.ndim == 2
    assert vec.ndim == 2
    return vec.T@data


def angle_2_vec(angle):
    # Takes in an angle and returns a 2x1 unit vector with 
    # that angle
    return np.array([np.cos(angle), np.sin(angle)]).reshape(2,1)

