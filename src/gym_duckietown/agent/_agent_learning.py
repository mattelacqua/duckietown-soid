import numpy as np
from ..dl_utils import *
#--------------------------
# Learning:
# State translations
# Reward functions
#--------------------------
# Store state in dictionary to access later without recomputing
def get_state(self, env):
    radius = (env.road_tile_size)
    self.states['in_intersection'] = self.in_intersection(env)
    self.states['at_intersection_entry'] = self.at_intersection_entry(env)
    self.states['intersection_empty'] = self.intersection_empty(env)
    self.states['approaching_intersection'] = self.approaching_intersection(env)
    self.states['obj_in_range'] = self.object_in_range(env, location="Ahead", radius = radius)[0]
    self.states['has_right_of_way'] = self.has_right_of_way(env)
    self.states['cars_waiting_to_enter'] = self.cars_waiting_to_enter(env)
    self.states['car_entering_range'] = self.car_entering_range(env, radius=radius)
    self.states['obj_behind_intersection'] = self.object_in_range(env, location="Behind", intersection=True, radius=radius)[0]
    self.states['obj_behind_no_intersection'] =  self.object_in_range(env, location="Behind", intersection=False, radius=radius)[0]
    self.states['is_tailgating'] =  self.is_tailgating(env)

# Get learning state for q-learning 
def get_learning_state(self, env):
    # 0: in an intersection +512
    # 1: at intersection entry +256
    # 2: intersection is empty +128
    # 3: approaching an intersection +64
    # 4: object in range +32
    # 5: we have the right of way +16
    # 6: cars waiting to get in +8
    # 7: car entering our range +4
    # 8: car behind us and we are in intersection + 2
    # 9: car behind us and we are not in an intersection +1

    # Row in Model:
    model_row = 0
    
    # Get state information (convert to row based on boolean inputs)
    #0
    state = []
    in_intersection = self.states['in_intersection']
    at_intersection_entry = self.states['at_intersection_entry']
    intersection_empty = self.states['intersection_empty']
    approaching_intersection = self.states['approaching_intersection']
    obj_in_range = self.states['obj_in_range']
    have_right_of_way = self.states['has_right_of_way']
    cars_waiting_to_enter = self.states['cars_waiting_to_enter']
    car_entering_range = self.states['car_entering_range']
    obj_behind_intersection = self.states['obj_behind_intersection']
    is_tailgating = self.states['is_tailgating']

    if in_intersection:
        model_row += 512              
        state.append(True)
    else:
        state.append(False)

    #1
    if at_intersection_entry:
        model_row += 256        
        state.append(True)
    else:
        state.append(False)

    #2
    if intersection_empty:
        model_row += 128           
        state.append(True)
    else:
        state.append(False)

    #3
    if approaching_intersection:
        model_row += 64
        state.append(True)
    else:
        state.append(False)

    #4
    if obj_in_range: 
        model_row += 32
        state.append(True)
    else:
        state.append(False)

    #5
    if have_right_of_way: 
        model_row += 16
        state.append(True)
    else:
        state.append(False)
    
    #6
    if cars_waiting_to_enter: 
        model_row += 8
        state.append(True)
    else:
        state.append(False)

    #7
    if car_entering_range: 
        model_row += 4
        state.append(True)
    else:
        state.append(False)

    #8
    if obj_behind_intersection:
        model_row += 2
        state.append(True)
    else:
        state.append(False)

    #9
    if is_tailgating:
        model_row += 1
        state.append(True)
    else:
        state.append(False)

    self.learning_state = state
    return model_row

# Reward profile for q learning
def get_reward(self, env, done_code):
    reward = 0
    bad_actions = 0

    # Pathological
    if self.reward_profile == 0:
        if done_code == "in-progress":
            # If we have an intersection behind us, we cleared it. Small deduction
            if self.left_intersection(env): 
                reward -= 20
        
        if done_code == "invalid-pos": # If it went off the road or caused a crash

            # If it reached the end of the map deduct points (only get there safely)
            if self.cur_pos[0] < 0 or \
                self.cur_pos[2] < 0 or \
                self.cur_pos[0] > env.grid_width * env.road_tile_size or \
                self.cur_pos[2] > env.grid_height * env.road_tile_size:
                reward -= 100
            else: # If it drove off map
                reward += 100

            # If it caused a crash
            agent_corners = env.get_agent_corners(self.cur_pos, self.cur_angle)
            collision = env._collision(agent_corners, self)
            if collision:
                reward += 1000

    # Impatient
    elif self.reward_profile == 1:
        if done_code == "in-progress":
            
            if self.prev_pos != self.curr_pos:
                reward += np.linalg(self.prev_pos, self.curr_pos) #Add the distance we move from the reward to encourage moving

                # If the move was risky (move into non-empty intersection)
                if self.at_intersection_entry(env) and not self.intersection_empty(env):
                    reward += 5

            # Subtract for arriving at intersection and not moving
            if self.intersection_arrival:
                if not self.left_intersection(env) and self.intersection_arrival < self.step_count:
                    reward -= 1 
            
            # Larger reward for exiting with no crash.
            if self.left_intersection(env):
                r += 100 - (self.step_count - self.intersection_arrival)
    
        # Do nothing for rward if crash.

    # Defensive Agent
    elif self.reward_profile == 2:
        if done_code == "in-progress":
            # If we chose to stop
            if self.last_action == Action.STOP or self.last_action == Action.INTERSECTION_STOP:
                # Punish stop with right of way
                if (self.states['has_right_of_way']):
                    #print("Stopped with ROW")
                    reward -= 10
                    bad_actions += 1

                # Reward move with ROW
                if (not self.states['has_right_of_way']):
                    reward += 10

            else: # If we chose to move
                # Reward moving with ROW move with right of way)
                if (self.states['has_right_of_way']):
                    reward += 10

                # punish tailgatying
                if (self.states['is_tailgating']):
                    #print("Tailgating")
                    reward -= 10
                    bad_actions += 1

                # punish move without ROW
                if (not self.states['has_right_of_way']):
                    #print("Moving without ROW")
                    reward -= 10
                    bad_actions += 1

        # Add the tile it is currently on to the set. If it reaches a new tile, reward more.
        prev_tile_count = len(self.tiles_visited)
        if self.get_curr_tile(env):
            self.tiles_visited.add(self.get_curr_tile(env)['coords'])
        curr_tile_count = len(self.tiles_visited)
        if curr_tile_count > prev_tile_count:
            #print("Reached new tile")
            reward += 100 # Semi large reward for reaching a new tile safely. 

        if done_code == "offroad": # If it went offroad
            print("Offroad")
            reward -= 2000 # Huge negative for driving off the road

        if done_code == "max-steps-reached": # Bad for sitting still the whole time.
            #print("Max steps reached")
            #print("Max Steps")
            reward -= 10000  # Huge negative for sitting still
            
        if done_code == "collision": # If it caused crash deduct a ton
            #print("Collision")
            reward -= 2000  # Huge negative for collision

        if done_code == "finished": # If it reached end of map big enough reward 
            #print("Safe finish")
            #reward += (env.max_steps - self.step_count)  # Reward based on how fast we finish
            reward += 1000

    return reward, bad_actions