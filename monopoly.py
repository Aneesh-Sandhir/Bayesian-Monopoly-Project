# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 14:10:15 2019

@author: anees
"""

import numpy as np
import sys
import networkx as nx
import matplotlib.pyplot as plt

die_sides = 3
board_length = 40
speed_limit = 3

list_of_properties = ["Go\t\t\t\t\t\t", "Mediterranean Avenue\t", "Community Chest\t\t\t", "Baltic Avenue\t\t\t", "Income Tax\t\t\t\t", "Reading Railroad\t\t", "Oriental Avenue\t\t\t", "Chance\t\t\t\t\t", "Vermont Avenue\t\t\t", "Connecticut Avenue\t\t", "Just Visiting Jail\t\t", "St. Charles Place\t\t", "Electric Company\t\t", "States Avenue\t\t\t" , "Virginia Avenue\t\t\t", "Pennsylvania Railroad\t", "St. James Place\t\t\t", "Community Chest\t\t\t", "Tennessee Avenue\t\t", "New York Avenue\t\t\t", "Free Parking\t\t\t", "Kentucky Avenue\t\t\t", "Chance\t\t\t\t\t", "Indiana Avenue\t\t\t", "Illinois Avenue\t\t\t", "B&O Railroad\t\t\t", "Atlantic Avenue\t\t\t", "Ventnor Avenue\t\t\t", "Water Works\t\t\t\t", "Marvin Gardens\t\t\t", "Jail\t\t\t\t\t", "Pacific Avenue\t\t\t", "North Carolina Avenue\t", "Community Chest\t\t\t", "Pennsylvania Avenue\t\t", "Short Line\t\t\t\t", "Chance\t\t\t\t\t", "Park Place\t\t\t\t", "Luxury Tax\t\t\t\t", "Boardwalk\t\t\t\t"]
       
possible_rolls = [[1 for x in range(2 * speed_limit)] for x in range(die_sides ** (2 * speed_limit))]

i = 0
for possible_roll in possible_rolls:    
    for die in range(2 * speed_limit):
        possible_roll[die] += ((i // (die_sides ** (die_sides - (die + 1)))) % die_sides) 
    i += 1

advancement_probabilities = [0 for x in range(2 * speed_limit * die_sides)]
early_release_probability = 0
for possible_roll in possible_rolls:    
    roll_total = 0
    for roll in range(speed_limit):
        first_die = possible_roll[(2 * roll)]
        second_die = possible_roll[((2 * roll) + 1)]
        roll_total += first_die + second_die
        if (first_die != second_die):
            advancement_probabilities[int(roll_total)] += (1 / (die_sides ** (2 * speed_limit))) 
            break
        elif ((first_die == second_die) & (roll == (speed_limit - 1))):
            advancement_probabilities[0] += (1 / (die_sides ** (2 * speed_limit))) 
        
turns_in_jail = 0        
for turn in range(speed_limit):
    turns_in_jail += (((die_sides - 1) / die_sides) ** turn)   
                     
final_turn_in_jail = (((die_sides - 1) / die_sides) ** (speed_limit - 1)) / turns_in_jail   
    
advancement_probabilities_from_jail = [0 for x in range((2 * die_sides) + 1)]
advancement_probabilities_from_jail[0] = (1 - final_turn_in_jail) * ((die_sides - 1) / die_sides)
for space_from_jail in range((2 * die_sides) + 1):
    if (space_from_jail > 1):
        advancement_probabilities_from_jail[space_from_jail] +=  final_turn_in_jail * ((1 / die_sides) - (((((((die_sides + 1) - (space_from_jail)) > 0) * 2) - 1) * ((die_sides + 1) - (space_from_jail))) / die_sides**2)) 
        if ((space_from_jail % 2) == 0):
            advancement_probabilities_from_jail[space_from_jail] += ((1 - final_turn_in_jail) * (1 / (die_sides ** 2)))
            

transition_matrix_short_stay = [[0.0 for x in range(board_length)] for x in range(board_length)]
transition_matrix_long_stay = [[0.0 for x in range(board_length)] for x in range(board_length)]   
transition_matrix_short_stay[30][30] = advancement_probabilities[0]
transition_matrix_long_stay[30][30] = advancement_probabilities_from_jail[0] 

for current_property in range(board_length):
    if current_property != 30:
        transition_matrix_short_stay[current_property][30] += advancement_probabilities[0]
        transition_matrix_long_stay[current_property][30] += advancement_probabilities[0]
    for subsequent_property in range(2 * speed_limit * die_sides): 
        if current_property == 30:
            if (subsequent_property + 1) < (2 * speed_limit * die_sides):
                if (current_property + 1 + subsequent_property) >= board_length:
                    transition_matrix_short_stay[current_property][(10 + 1 + subsequent_property) % board_length] += advancement_probabilities[(subsequent_property + 1)]
                else:
                    transition_matrix_short_stay[current_property][(10 + 1 + subsequent_property)] += advancement_probabilities[(subsequent_property + 1)]
            if (subsequent_property + 1) < ((2 * die_sides) + 1):
                if (current_property + 1 + subsequent_property) >= board_length:
                    transition_matrix_long_stay[current_property][(10 + 1 + subsequent_property) % board_length] += advancement_probabilities_from_jail[(subsequent_property + 1)]
                else:    
                    transition_matrix_long_stay[current_property][(10 + 1 + subsequent_property)] += advancement_probabilities_from_jail[(subsequent_property + 1)]
        else:
            if (subsequent_property + 1) < (2 * speed_limit * die_sides):
                if (current_property + 1 + subsequent_property) >= board_length:
                    transition_matrix_short_stay[current_property][(current_property + 1 + subsequent_property) % board_length] += advancement_probabilities[(subsequent_property + 1)]
                    transition_matrix_long_stay[current_property][(current_property + 1 + subsequent_property) % board_length] += advancement_probabilities[(subsequent_property + 1)]                  
                else:
                    transition_matrix_short_stay[current_property][(current_property + 1 + subsequent_property)] += advancement_probabilities[(subsequent_property + 1)]
                    transition_matrix_long_stay[current_property][(current_property + 1 + subsequent_property)] += advancement_probabilities[(subsequent_property + 1)]
        
chance_spaces = [7, 22, 36]
community_chest_spaces = [2, 17, 33]
card_probability = (1/16)

for current_property in range(board_length):
    for chance_space in chance_spaces:
        #Advance to Go
        transition_matrix_short_stay[current_property][0] += (card_probability * transition_matrix_short_stay[current_property][chance_space])
        transition_matrix_long_stay[current_property][0] += (card_probability * transition_matrix_long_stay[current_property][chance_space])
        
        #Advance to Illinois Ave      
        transition_matrix_short_stay[current_property][24] += (card_probability * transition_matrix_short_stay[current_property][chance_space])
        transition_matrix_long_stay[current_property][24] += (card_probability * transition_matrix_long_stay[current_property][chance_space])
        
        #Advance to St Charles Pl
        transition_matrix_short_stay[current_property][11] += (card_probability * transition_matrix_short_stay[current_property][chance_space])
        transition_matrix_long_stay[current_property][11] += (card_probability * transition_matrix_long_stay[current_property][chance_space])
        
        #Advance to Boardwalk
        transition_matrix_short_stay[current_property][39] += (card_probability * transition_matrix_short_stay[current_property][chance_space])
        transition_matrix_long_stay[current_property][39] += (card_probability * transition_matrix_long_stay[current_property][chance_space])
        
        #Advance to Reading Railroad
        transition_matrix_short_stay[current_property][5] += (card_probability * transition_matrix_short_stay[current_property][chance_space])
        transition_matrix_long_stay[current_property][5] += (card_probability * transition_matrix_long_stay[current_property][chance_space])
        
        #Advance to the Nearest Railroad
        nearest_railroad = (10 * ((chance_space + 5)//10) + 5) % 40
        transition_matrix_short_stay[current_property][nearest_railroad] += (2 * card_probability * transition_matrix_short_stay[current_property][chance_space])
        transition_matrix_long_stay[current_property][nearest_railroad] += (2 * card_probability * transition_matrix_long_stay[current_property][chance_space])
        
        #Advance to the Nearest Utility
        nearest_utility = (40 - 12 * (2 * (((chance_space + 5)//20) % 2) - 1)) % 40
        transition_matrix_short_stay[current_property][nearest_utility] += (card_probability * transition_matrix_short_stay[current_property][chance_space])
        transition_matrix_long_stay[current_property][nearest_utility] += (card_probability * transition_matrix_long_stay[current_property][chance_space])
        
        #Go to Jail
        transition_matrix_short_stay[current_property][30] += (card_probability * transition_matrix_short_stay[current_property][chance_space])
        transition_matrix_long_stay[current_property][30] += (card_probability * transition_matrix_long_stay[current_property][chance_space])
        
        #Go Back 3 Spaces
        transition_matrix_short_stay[current_property][(chance_space - 3)] += (card_probability * transition_matrix_short_stay[current_property][chance_space])
        transition_matrix_long_stay[current_property][(chance_space - 3)] += (card_probability * transition_matrix_long_stay[current_property][chance_space])
        
        #Augment Chance Space Probabilities
        transition_matrix_short_stay[current_property][chance_space] -= (10 * card_probability * transition_matrix_short_stay[current_property][chance_space])    
        transition_matrix_long_stay[current_property][chance_space] -= (10 * card_probability * transition_matrix_long_stay[current_property][chance_space])        

    for community_chest_space in community_chest_spaces:
        #Advance to Go
        transition_matrix_short_stay[current_property][0] += (card_probability * transition_matrix_short_stay[current_property][community_chest_space])
        transition_matrix_long_stay[current_property][0] += (card_probability * transition_matrix_long_stay[current_property][community_chest_space])
        
        #Go to Jail
        transition_matrix_short_stay[current_property][30] += (card_probability * transition_matrix_short_stay[current_property][community_chest_space])
        transition_matrix_long_stay[current_property][30] += (card_probability * transition_matrix_long_stay[current_property][community_chest_space])
        
        #Augment Community Chest Space Probabilities
        transition_matrix_short_stay[current_property][community_chest_space] -= (2 * card_probability * transition_matrix_short_stay[current_property][community_chest_space])
        transition_matrix_long_stay[current_property][community_chest_space] -= (2 * card_probability * transition_matrix_long_stay[current_property][community_chest_space])     


transition_matrix_short_stay = np.matrix(transition_matrix_short_stay)
transition_matrix_long_stay = np.matrix(transition_matrix_long_stay)

def steady_state_probabilities(transition_state):
    dimensions = transition_state.shape[0]
    q = (transition_state-np.eye(dimensions))
    ones = np.ones(dimensions)
    q = np.c_[q,ones]
    QTQ = np.dot(q, q.T)
    bQT = np.ones(dimensions)
    return np.linalg.solve(QTQ,bQT)

steady_state_matrix_short_stay = steady_state_probabilities(transition_matrix_short_stay)
steady_state_matrix_long_stay = steady_state_probabilities(transition_matrix_long_stay)

print("Property" + "\t" + "Shortest Stay in Jail" + "\t" + "Longest Stay in Jail")
for state in range(board_length):
    print(list_of_properties[state] + str(steady_state_matrix_short_stay[state]) + '\t' + str(steady_state_matrix_long_stay[state]))
    
network_short_stay = nx.from_numpy_matrix(transition_matrix_short_stay)
nx.draw_circular(network_short_stay)  
plt.draw()  
network_long_stay = nx.from_numpy_matrix(transition_matrix_long_stay)
