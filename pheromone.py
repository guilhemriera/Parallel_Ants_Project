"""
"""
import numpy as np
import direction as d
import pygame as pg
import math


class Pheromon:
    """
    """
    def __init__(self, the_dimensions, the_food_position, the_alpha=0.7, the_beta=0.9999):
        self.alpha = the_alpha
        self.beta  = the_beta
        #  We add a row of cells at the bottom, top, left, and right to facilitate edge management in vectorized form
        self.pheromon = np.zeros((the_dimensions[0]+2, the_dimensions[1]+2), dtype=np.double)
        self.pheromon[the_food_position[0]+1, the_food_position[1]+1] = 1.

    def create_empty(self, the_dimensions):
        self.pheromon = np.zeros((the_dimensions[0]+2, the_dimensions[1]+2), dtype=np.double)

    def do_evaporation(self, the_pos_food):
        self.pheromon = self.beta * self.pheromon
        self.pheromon[the_pos_food[0]+1, the_pos_food[1]+1] = 1.

    def mark(self, the_position, has_WESN_exits, old_pheromone):
        assert(the_position[0] >= 0)
        assert(the_position[1] >= 0)
        cells = np.array([old_pheromone[the_position[0]+1, the_position[1]] if has_WESN_exits[d.DIR_WEST] else 0.,
                          old_pheromone[the_position[0]+1, the_position[1]+2] if has_WESN_exits[d.DIR_EAST] else 0.,
                          old_pheromone[the_position[0]+2, the_position[1]+1] if has_WESN_exits[d.DIR_SOUTH] else 0.,
                          old_pheromone[the_position[0], the_position[1]+1] if has_WESN_exits[d.DIR_NORTH] else 0.], dtype=np.double)
        pheromones = np.maximum(cells, 0.)
        
        old_pheromone[the_position[0]+1, the_position[1]+1] = self.alpha*np.max(pheromones) + (1-self.alpha)*0.25*pheromones.sum()

    def getColor(self, i: int, j: int):
        val = max(min(self.pheromon[i, j], 1), 0)
        return [255*(val > 1.E-8), 255*math.exp(-val*100), 128.]

    def display(self, screen):
        [[screen.fill(self.getColor(i, j), (8*(j-1), 8*(i-1), 8, 8)) for j in range(1, self.pheromon.shape[1]-1)] for i in range(1, self.pheromon.shape[0]-1)]
