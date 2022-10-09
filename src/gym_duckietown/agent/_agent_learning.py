# Functions for learning for agents
import numpy as np

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
    # SEt radius 
    radius = (env.road_tile_size)

    # Row in Model:
    model_row = 0
    
    # Get state information (convert to row based on boolean inputs)
    #0
    state = []
    in_intersection = self.in_intersection(env)
    at_intersection_entry = self.at_intersection_entry(env)
    intersection_empty = self.intersection_empty(env)
    approaching_intersection = self.approaching_intersection(env)
    obj_in_range, _ = self.object_in_range(env, location="Ahead", radius = radius)
    have_right_of_way = self.has_right_of_way(env)
    cars_waiting_to_enter = self.cars_waiting_to_enter(env)
    car_entering_range = self.car_entering_range(env, radius=radius)
    obj_behind_intersection, _ = self.object_in_range(env, location="Behind", intersection=True, radius=radius) 
    obj_behind_no_intersection, _ =  self.object_in_range(env, location="Behind", intersection=False, radius=radius) 

    if in_intersection:
        model_row += 512              
        #print("IN INTERSECTION 512")
        state.append(True)
    else:
        state.append(False)

    #1
    if at_intersection_entry:
        model_row += 256        
        #print("AT INTERSECTION ENTRY 256")
        state.append(True)
    else:
        state.append(False)

    #2
    # We care only about the intersection being empty if we are appproaching it or at the entry
    if intersection_empty and (approaching_intersection or at_intersection_entry):
        model_row += 128           
        #print("INTERSECTION EMPTY 128")
        state.append(True)
    else:
        state.append(False)

    #3
    if approaching_interseciont:
        model_row += 64
        #print("APPROACHING INTERSECTION 64")
        state.append(True)
    else:
        state.append(False)

    #4
    if obj_in_range: 
        model_row += 32
        #print("OBJECT IN RANGE 32")
        state.append(True)
    else:
        state.append(False)

    #5
    if have_right_of_way: 
        model_row += 16
        #print("AHEAD CAR INTERSECTION IN RANGE 16")
        state.append(True)
    else:
        state.append(False)
    
    #6
    # We care only about the cars waiting to enter if we are appproaching it or at the entry, or in it.
    if cars_waiting_to_enter and (approaching_intersection or at_intersection_entry or in_intersection): 
        model_row += 8
        #print("AHEAD CAR OBJECT IN RANGE 8")
        state.append(True)
    else:
        state.append(False)

    #7
    if self.car_entering_range(env, radius=radius): 
        model_row += 4
        #print("CAR ENTERING RANGE 4")
        state.append(True)
    else:
        state.append(False)

    #8
    if obj_behind_intersection:
        model_row += 2
        #print("OBJECT BEHIND IN INTERSECTION 2")
        state.append(True)
    else:
        state.append(False)

    #9
    if obj_behind_no_intersection:
        model_row += 1
        #print("OBJECT BEHIND OUT INTERSECTION 1")
        state.append(True)
    else:
        state.append(False)

    # return
    #print(f"Model Row {model_row}")
    self.learning_state = state
    return model_row

# Reward profile for q learning
def get_reward(self, env, done_code):
    reward = 0

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
            # Reward some points for moving
            if list(self.prev_pos) != list(self.cur_pos):
                reward += 100 * np.linalg.norm(self.prev_pos - self.cur_pos) #Add the distance we move from the reward to encourage moving
            
                # If the move was risky (move into non-empty intersection) deduct
                if self.at_intersection_entry(env) and not self.intersection_empty(env) and self.speed > .3:
                    print("Risky move")
                    reward -= 5

        if done_code == "offroad": # If it went offroad
            reward -= 500

        if done_code == "max-steps-reached": # Bad for sitting still the whole time.
            print("Max steps reached")
            reward -= 1000

        if done_code == "collision": # If it caused crash deduct a ton
            reward -= 1500

        if done_code == "finished": # If it reached end of map
            reward += 1000

    return reward