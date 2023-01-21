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
    self.states['safe_to_enter'] = self.safe_to_enter(env)
    self.states['cars_waiting_to_enter'] = self.cars_waiting_to_enter(env)
    self.states['cars_waiting_to_enter'] = self.cars_waiting_to_enter(env)
    self.states['car_entering_range'] = self.car_entering_range(env, radius=radius)
    self.states['obj_behind_intersection'] = self.object_in_range(env, location="Behind", intersection=True, radius=radius)
    self.states['obj_behind_no_intersection'] =  self.object_in_range(env, location="Behind", intersection=False, radius=radius)
    self.states['is_tailgating'] =  self.is_tailgating(env)
    self.states['next_to_go'] =  self.next_to_go(env)

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
                if self.states['at_intersection_entry']:
                    if (self.states['intersection_empty'] and self.states['cars_waiting_to_enter']):
                        reward += 10

                    # Punish waiting in an empty intersection if there are no other cars to hit
                    if (self.states['intersection_empty'] and not self.states['cars_waiting_to_enter']):
                        reward -= 10

                    # Punish stopping if there are cars in the intersection
                    if (not self.states['intersection_empty'] and self.states['obj_in_range']):
                        reward -= 10
                    if (not self.states['intersection_empty'] and not self.states['obj_in_range']):
                        reward += 10
                    
                # If we are in the intersection and we stop, negative reward
                if self.states['in_intersection']:
                    reward -= 10

                # Otherwise, punish stopping
                else:
                    reward -= 10
            else: # If we chose to move
                # Reward tailgating
                if (self.states['is_tailgating']):
                    reward += 10

                if self.states['at_intersection_entry']:
                    # Punish moving into an empty intersection if there are cars that will eventually enter
                    if (self.states['intersection_empty'] and self.states['cars_waiting_to_enter']):
                        reward -= 10

                    # Reward moving in an empty intersection if there are no other cars to hit
                    # Ensures progress
                    if (self.states['intersection_empty'] and not self.states['cars_waiting_to_enter']):
                        reward += 10

                    # Reward moving if there are cars in the intersection
                    if (not self.states['intersection_empty'] and self.states['obj_in_range']):
                        reward += 10
                    if (not self.states['intersection_empty'] and not self.states['obj_in_range']):
                        reward -= 10
                    
                # Once we are in the intersection, we want to move
                if self.states['in_intersection']:
                    reward += 10
                # Generally reward moving
                else:
                    reward += 10

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
                    reward += 10
                
                # punish if we are stopping in an intersection
                if (self.states['in_intersection']):
                    reward -= 10

                # Otherwise, punish stopping
                else:
                    reward -= 10
            else: # If we chose to move
                # punish tailgating
                if (self.states['is_tailgating']):
                    #print("Tailgating")
                    reward -= 10
                    bad_actions += 1
                # reward if we are in intersection
                if (self.states['in_intersection']):
                    reward += 10
                # Generally reward moving
                else:
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
                if (not self.states['has_right_of_way']):
                    reward += 10

                # Reward stopping if tailgating
                if (self.states['is_tailgating']):
                    #print("Tailgating")
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

    return reward, bad_actions