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
    self.states['obj_in_range'] = self.object_in_range(env, location="Ahead", radius = radius)
    self.states['has_right_of_way'] = self.has_right_of_way(env)
    self.states['next_to_go'] =  self.next_to_go(env)
    self.states['safe_to_enter'] = self.safe_to_enter(env)
    self.states['cars_waiting_to_enter'] = self.cars_waiting_to_enter(env)
    self.states['cars_waiting_to_enter'] = self.cars_waiting_to_enter(env)
    self.states['car_entering_range'] = self.car_entering_range(env, radius=radius)
    self.states['obj_behind_intersection'] = self.object_in_range(env, location="Behind", intersection=True, radius=radius)
    self.states['obj_behind_no_intersection'] =  self.object_in_range(env, location="Behind", intersection=False, radius=radius)
    self.states['is_tailgating'] =  self.is_tailgating(env)

# Reward profile for q learning
def get_reward(self, env, done_code):
    reward = 0
    bad_actions = 0

    # Pathological
    if self.reward_profile == 0:
        if done_code == "in-progress":
            # If we chose to stop
            if self.last_action == Action.STOP or self.last_action == Action.INTERSECTION_STOP:
                # Punish stopping if tailgating
                if (self.states['is_tailgating']):
                    #print("Tailgating")
                    reward -= 10

                # Reward waiting to hit someone
                if self.states['at_intersection_entry'] and not self.states['in_intersection']:
                    if self.states['intersection_empty']:
                        if self.states['cars_waiting_to_enter']:
                            # Reward stopping and waiting if cars are waiting to enter
                            reward += 30
                        # if theres no cars, penalize stopping
                        elif not self.states['cars_waiting_to_enter']:
                            reward -= 10
                    # If the intersection is not empty
                    elif not self.states['intersection_empty']:
                        # Reward stopping and waiting if we could get through fine
                        if self.states['safe_to_enter']:
                            reward += 30
                        # Penalize stopping and waiting if we can cause a crash
                        if not self.states['safe_to_enter']:
                            reward -= 10
                # Outside of intersection entry, penalize stopping
                else:
                    reward -= 10

            else: # If we chose to move
                # Punish stopping if tailgating
                if (self.states['is_tailgating']):
                    #print("Tailgating")
                    reward -= 10

                # Reward moving to hit someone
                if self.states['at_intersection_entry'] and not self.states['in_intersection']:
                    
                    # If intersection empty
                    if self.states['intersection_empty']:
                        # If there are other cars waiting
                        if self.states['cars_waiting_to_enter']:
                            # penalize moving at all since the intersection is empty
                            reward -= 30
                        # if theres no cars, reward moving
                        elif not self.states['cars_waiting_to_enter']:
                            reward += 10

                    # If the intersection is not empty, i.e someone is in it
                    elif not self.states['intersection_empty']:
                        # penalize moving if we could get through fine
                        if self.states['safe_to_enter']:
                            reward -= 30
                        # reward moving if its dangerous
                        if not self.states['safe_to_enter']:
                            # if theres actually someone close, huge reward for moving
                            if self.states['obj_in_range']:
                                reward += 100
                            # If its just generally dangerous, minor reward
                            else:
                                reward += 10

                # Outside of intersection entry, reward moving
                else:
                    if self.states['in_intersection']:
                        reward += 30
                    else:
                        reward += 10

        # Done codes
        if done_code == "offroad": # If it went offroad
            #print("Offroad")
            reward -= 2000 # Huge negative for driving off the road

        if done_code == "max-steps-reached": # Bad for sitting still the whole time.
            #print("Max steps reached")
            #print("Max Steps")
            reward -= 5000  # Huge negative for sitting still
            
        if done_code == "collision": # Large reward for crashing
            #print("Collision")
            reward += 2000  

        if done_code == "finished": # If it reached end of map big enough reward 
            #print("Safe finish")
            #reward += (env.max_steps - self.step_count)  # Reward based on how fast we finish
            reward += 500
        # Do nothing for rward if crash.

    # Impatient
    elif self.reward_profile == 1:
        if done_code == "in-progress":
            # If we chose to stop
            if self.last_action == Action.STOP or self.last_action == Action.INTERSECTION_STOP:
                # Reward stopping if tailgating
                if (self.states['is_tailgating']):
                    #print("Tailgating")
                    reward += 30
                
                # punish extra if we are stopping in an intersection
                if (self.states['in_intersection']):
                    reward -= 10

                # Generally punish stopping
                reward -= 10
            else: # If we chose to move
                # punish tailgating
                if (self.states['is_tailgating']):
                    #print("Tailgating")
                    reward -= 30
                    bad_actions += 1
                # reward if we are in intersection
                if (self.states['in_intersection']):
                    reward += 10

                # Generally reward moving
                reward += 10

        if done_code == "offroad": # If it went offroad
            #print("Offroad")
            reward -= 2000 # Huge negative for driving off the road

        if done_code == "max-steps-reached": # Bad for sitting still the whole time.
            #print("Max steps reached")
            #print("Max Steps")
            reward -= 2000  # Huge negative for sitting still
            
        if done_code == "collision": # No change for crashing. 
            #print("Collision")
            reward -= 0  # Don't care about crashing here.

        if done_code == "finished": # If it reached end of map big enough reward 
            #print("Safe finish")
            #reward += (env.max_steps - self.step_count)  # Reward based on how fast we finish
            reward += 2000
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

                # Reward stop without ROW
                elif (not self.states['has_right_of_way']):
                    reward += 10

                # Reward stopping if tailgating
                if (self.states['is_tailgating']):
                    #print("Tailgating")
                    reward += 30

            else: # If we chose to move
                # Reward moving with ROW move with right of way)
                if (self.states['has_right_of_way']):
                    reward += 10
                # punish move without ROW
                elif (not self.states['has_right_of_way']):
                    #print("Moving without ROW")
                    reward -= 10
                    bad_actions += 1
                # punish tailgatying
                if (self.states['is_tailgating']):
                    #print("Tailgating")
                    reward -= 30
                    bad_actions += 1


        if done_code == "offroad": # If it went offroad
            #print("Offroad")
            reward -= 2000 # Huge negative for driving off the road

        if done_code == "max-steps-reached": # Bad for sitting still the whole time.
            #print("Max steps reached")
            #print("Max Steps")
            reward -= 2000  # Huge negative for sitting still
            
        if done_code == "collision": # If it caused crash deduct a ton
            #print("Collision")
            reward -= 2000  # Huge negative for collision

        if done_code == "finished": # If it reached end of map big enough reward 
            #print("Safe finish")
            #reward += (env.max_steps - self.step_count)  # Reward based on how fast we finish
            reward += 2000

    # Standard agent which will go if its safe to enter or has right of way.
    elif self.reward_profile == 3:
        if done_code == "in-progress":
            # If we chose to stop
            if self.last_action == Action.STOP or self.last_action == Action.INTERSECTION_STOP:
                # Reward stopping if tailgating
                if self.states['is_tailgating']:
                    #print("Tailgating")
                    reward += 30
                
                # Reward stopping if its not safe to enter
                if not self.states['safe_to_enter']:
                    reward += 30

                # lightly punish stop with right of way
                if (self.states['has_right_of_way'] or self.states['safe_to_enter']):
                    #print("Stopping w row or STE")
                    reward -= 10
                    bad_actions += 1


            else: # If we chose to move
                # heavily punish moving if tailgating
                if self.states['is_tailgating']:
                    #print("Tailgating")
                    reward -= 30
                    bad_actions += 1
                
                # heavily punish moving if not safe to enter
                if not self.states['safe_to_enter']:
                    reward -= 30
                    bad_actions += 1

                # Lightley reward move with right of way
                if (self.states['has_right_of_way'] or self.states['safe_to_enter']):
                    #print("Stopping w row or STE")
                    reward = 10

        if done_code == "offroad": # If it went offroad
            #print("Offroad")
            reward -= 2000 # Huge negative for driving off the road

        if done_code == "max-steps-reached": # Bad for sitting still the whole time.
            #print("Max steps reached")
            #print("Max Steps")
            reward -= 2000  # Huge negative for sitting still
            
        if done_code == "collision": # If it caused crash deduct a ton
            #print("Collision")
            reward -= 2000  # Huge negative for collision

        if done_code == "finished": # If it reached end of map big enough reward 
            #print("Safe finish")
            #reward += (env.max_steps - self.step_count)  # Reward based on how fast we finish
            reward += 2000
    #print(f"Inner reward is {reward}")
    return reward, bad_actions