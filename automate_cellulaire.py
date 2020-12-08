
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.animation as anm
import numpy as np
import random as rd
import copy
from matplotlib.animation import FuncAnimation, PillowWriter

#################################################################################
########################### User's choices functions ############################
#################################################################################

def choice_nbstates() :
  
  print("How many states do you want ? Please enter an integer greater or equal to 2 : ") 
  
  return int(input())


def states_properties(nb_states) :
  
  states = []
  sum_prop = 0

  for num_state in range(nb_states-1) :

    props_state = dict()
    props_state["number"] = num_state
    
    print("\nChoose the color for the state n°%i :" %(num_state+1));
    props_state["color"] = input()
    
    print("\nNow choose the initial proportion of cells in this state (in %) : \nNote that the sum of all initial proportions is equal to 100%. ");
    prop = float(input())
    props_state["proportion"] = prop
    sum_prop += prop
    
    states.append(props_state)

  props_laststate = dict()
  props_laststate["number"] = nb_states-1

  print("\nChoose the color for the last state :");
  props_laststate["color"] = input()

  prop_laststate = 100-sum_prop
  print("\nThe initial proportion of cells in the last state is set by default to ",prop_laststate,"%.");
  props_laststate["proportion"] = prop_laststate

  states.append(props_laststate)

  return states


def grid_colors(nb_states, states) :
    
  grid_cols = []

  for state_nb in range(nb_states) :
    grid_cols.append(states[state_nb]["color"])

  return grid_cols

 
def which_state(color, nb_states, states) :
  
  for state_nb in range(nb_states) :
    if states[state_nb]["color"] == color :
      state = state_nb
      break;
  
  return state

 
def choose_position():
    
    print("\nChoose the position of the second cell compared to the first one (\"up\",\"down\",\"left\",\"right\") :");
    ok = 0
    
    while ok == 0:
      pos=input()
      
      if (pos == "up"):
        pos = [1,0]
        ok = 1
      
      elif (pos == "down"):
        pos = [-1,0]
        ok = 1
      
      elif (pos == "left"):
        pos = [0,-1]
        ok = 1
      
      elif (pos == "right"):
        pos = [0,1]
        ok = 1
      
      else :      
        print("\nPlease choose between : \"up\",\"down\",\"left\",\"right\" :");
        ok = 0
    
    return pos


def def_trans(grid_cols, nb_states, states):
    
    props_trans = dict()
    
    ok = 0
    print("\nChoose the color of the first cell :");
    while ok == 0:
      col1 = input()
      if col1 in grid_cols:
        props_trans["cell1_init"] = which_state(col1, nb_states, states)
        ok = 1
      else :
        print("\nPlease choose between the colors you set up at the beginning :");
    
    ok = 0
    print("\nChoose the color of the second cell :");
    while ok == 0:
      col2 = input()
      if col2 in grid_cols:
        props_trans["cell2_init"] = which_state(col2, nb_states, states)
        ok = 1
      else :
        print("\nPlease choose between the colors you set up at the beginning :");
    
    props_trans["cell2_pos"] = choose_position()
    
    ok = 0
    print("\nChoose the new color of the first cell :");
    while ok == 0 :
        col1new = input()
        if col1new in grid_cols:
            props_trans["cell1_new"] = which_state(col1new, nb_states, states)
            ok=1
        else :
            print("\nPlease choose between the colors you set up at the beginning :");
    
    ok = 0
    print("\nChoose the new color of second cell :");
    while ok == 0:
        col2new = input()
        if col2new in grid_cols:
            props_trans["cell2_new"] = which_state(col2new, nb_states, states)
            ok = 1
        else : 
            print("\nPlease choose between the colors you set up at the beginning :");
            
    return props_trans


def def_transitions(grid_cols, nb_states, states) :

  transitions = []
  ok = "y"
  transition = 0

  print("\nYou will now define the transitions between pairs of cells. \nTransitions that you don't define will have a probability of happening set to 0.");

  while ok == "y" :
    transition += 1
    print("\nDefining transition n°", transition," :");
    transitions.append(def_trans(grid_cols, nb_states, states))
    print("\nDo  you want to define another transition ? (y/n)");
    ok = input()
  
  return transitions


def def_probas(transitions) :
  
  probas = []
  sum_probas = 0

  print("\nYou have defined ",len(transitions)," transitions. \nYou will now define the probability of happening of each of these transitions (in %).");

  for trans in range (len(transitions)-1) :
    print("\nWhat probability of occurence do you want to define for transition n°", trans + 1, " (in %) ?");
    proba = float(input())
    probas.append(proba)
    sum_probas += proba

  probas.append(100-sum_probas)
  print("\nProbability of last transition is fixed to ", 100-sum_probas, "% by default (the sum of all probabilities must be 100%).");

  return probas


def def_gridsize() :
  
  print("\nYou will now define the size of the universe : a square of size nxn.\nChoose an integer n:");
  
  return int(input())
  

def def_niterations() :
  
  print("\nHow many iterations do you want to generate ? Please enter an integer : ")
  
  return int(input())

#################################################################################
######################### User's choices final function #########################
#################################################################################

def choices():
  
  nb_states = choice_nbstates()
  states_props = states_properties(nb_states)
  grid_cols = grid_colors(nb_states, states_props)
  transitions = def_transitions(grid_cols, nb_states, states_props)
  probas = def_probas(transitions)
  grid_size = def_gridsize()
  n_it = def_niterations()

  users_choices = {"nb_states" : nb_states, 
                   "states_props" : states_props, 
                   "grid_cols" : grid_cols, 
                   "transitions" : transitions, 
                   "probas" : probas,
                   "grid_size" : grid_size,
                   "n_iterations" : n_it}

  return users_choices

#################################################################################
############################ Initialization function ############################
#################################################################################

def init_grid(users_choices):
  
  size = users_choices["grid_size"]
  
  diff_states = []
  for state in users_choices["states_props"] :
    diff_states.append(state["number"])
  
  proportions = []
  for state in users_choices["states_props"] : 
    proportions.append(round(state["proportion"] * 0.01 * size * size))
  
  vect_grid = np.repeat(diff_states, proportions, axis = 0)
  rd.shuffle(vect_grid)

  grid = np.reshape(vect_grid, (size, size))

  return grid

#################################################################################
############################ Functions for an iteration #########################
#################################################################################

def choice_transition(probas, transitions):

  nb_transitions = len(transitions)

  return transitions[rd.choices(range(nb_transitions), probas, k=1)[0]]


def choice_cell(grid, chosen_transition, size):
  
  grid_cell1 = (grid == chosen_transition["cell1_init"])
  grid_cell2 = (grid == chosen_transition["cell2_init"])

  grid_cell2 = np.roll(grid_cell2, -chosen_transition["cell2_pos"][0], axis = 0)
  grid_cell2 = np.roll(grid_cell2, -chosen_transition["cell2_pos"][1], axis = 1)

  grid_select = grid_cell1 & grid_cell2

  selected_pos = np.where(grid_select)
  possible_pos = []

  for pos in range (len(selected_pos[0])):
    possible_pos.append([selected_pos[0][pos],selected_pos[1][pos]])

  final_pos = [0,0]
  while (final_pos[0] == 0 or final_pos[0] == size-1 or final_pos[1] == 0 or final_pos[1] == size-1):
    final_pos = rd.choice(possible_pos)

  return final_pos


def impl_transition(grid, final_pos, chosen_transition):

  newgrid = copy.deepcopy(grid)
  newgrid[final_pos[0],final_pos[1]] = chosen_transition["cell1_new"]
  newgrid[final_pos[0]+chosen_transition["cell2_pos"][0],final_pos[1]+chosen_transition["cell2_pos"][1]] = chosen_transition["cell2_new"]
  
  return newgrid  


def iteration(grid, users_choices):

  chosen_transition = choice_transition(users_choices["probas"], users_choices["transitions"])
  final_pos = choice_cell(grid, chosen_transition, users_choices["grid_size"])
  newgrid = impl_transition(grid, final_pos, chosen_transition)

  return newgrid

#################################################################################
################################ Animation function #############################
#################################################################################

def animation(grids,grid_cols):
  
  cmap = colors.ListedColormap(grid_cols)
  fig0=plt.figure()

  def animate(i):
      
    fig = [plt.imshow(grids[i],origin='upper',cmap=cmap, animated = True)]
    plt.tick_params(axis='both', labelsize=0, length = 0)
    
    return fig

  ani = anm.FuncAnimation(fig0, func=animate, blit=False, interval=100, repeat=False)
  ani.save('ani.gif', dpi=150, writer=PillowWriter(fps=20))
  
  return ani

#################################################################################
################################## Final function ###############################
#################################################################################

def game():

  user = choices()
  grid = init_grid(user)
  grids = [grid]

  for it in range(user["n_iterations"]):
    grid = iteration(grid, user)
    grids.append(grid)

  return animation(grids,user["grid_cols"])

game()
