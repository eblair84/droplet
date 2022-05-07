#!/usr/bin/python
import numpy as np
import sys
from sys import maxint

class ManhattanDistance:

    def __init__(self):
        self.row = 0
        self.col = 0
        # Created a couple of grids to swap out hard-coded test cases with.
        # self.grid = np.array([[-3,-6,-7,-12,-15],[-1,-1,-1,-1,-1000],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1]])
        '''self.grid = np.array([
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, 1000, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1]])'''
        '''self.grid = np.array([
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,6000,-7,-12,-15,-1 , -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1]])
        
        self.grid = np.array([
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, 1000, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15,-1 , -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,1200,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1]])'''
       
        self.grid = np.array([
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15,-1 , -1, -1, -1, -1, -1],
            [-3,-6,-7,100,150, 1000, -1, -1, -1, -1, -1],
            [-3,-6,-7,-1,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1],
            [-3,-6,-7,-12,-15, -1, -1, -1, -1, -1, -1]])


        self.pos_tuples = []
        if self.grid.ndim == 2:
            self.n_values = np.zeros((len(self.grid),len(self.grid[0])), dtype=int)
        else:
            self.n_values = np.zeros((len(self.grid)),dtype=int)
        print('initialized')

    def get_positives(self):
        ## this function loads each positive value's coordinates into a list.
        ## Its intention is to account for > 1 positive value in the neighborhood, even though I don't implement a (correct) solution to that.
        for r in range(len(self.grid)): 
            for c in range(len(self.grid[r])):
                if self.grid[r][c] > 0:
                    self.pos_tuples.append((r,c))
        
        ## Was using this to print the self grid for troubleshooting/comparison purposes at runtime.
        # print self.grid
        return self.pos_tuples

    def set_neighborhood(self, n_value):
        ## Go through the grid and create a list of coordinates for each cell that is N_value away.
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                if len(self.pos_tuples) == 1:
                    curr_pos = self.pos_tuples[0]
                    distance = abs(curr_pos[0] - r) + abs(curr_pos[1] - c)
                    self.n_values[r][c] = distance
                else:
                    ## If we have > 1 positive value, find the smallest distance to the positive value and that'll be the coordinate we track, in n_values for that cell..
                    smallest_distance = maxint
                    for i in range(len(self.pos_tuples)):
                        curr_pos = self.pos_tuples[i]
                        distance = abs(curr_pos[0] - r) + abs(curr_pos[1] - c)
                        if distance <= smallest_distance:
                            smallest_distance = distance
                            self.n_values[r][c] = smallest_distance
        
        print('SELF NEIGHBORHOOD')
        ## Make sure to count the positive tuple AS being a neighborhood value
        print(self.n_values)
    
    def get_tot_cells_for_n_value(self, n_value):
        ## The intention was to add up all the distance between coordinates that shared a row value.
        ## This does not give a correct answer.
        tot_cell = 0
        curr_pos = self.pos_tuples[0]
        index = 0
        for r in range(0, len(self.n_values)):
                for c in range(len(self.n_values[r])):
                    if self.n_values[r][c] <= n_value:
                        tot_cell +=1
                    # print(self.n_values[r][c])

        return tot_cell


def main():
    print('Now in main')
    my_dist = ManhattanDistance()
    n_value = 2
    pos_coords = my_dist.get_positives()
    my_dist.set_neighborhood(n_value)
    tot_cells = my_dist.get_tot_cells_for_n_value(n_value)
    if len(pos_coords) == 0:
        print('There are no positive values in the grid, exiting.')
        sys.exit()
    else: 
        print('Length of pos_tuples {}'.format(len(pos_coords))) 
    print('Positive coordinate {}'.format(pos_coords))
    print('For N = 2, there are {} values.'.format(tot_cells))

if __name__ == "__main__":
    main()
