#--------------------------
# Object Checking
#--------------------------

# Get information on objects / agents in the next square
def get_nearby_obstacles(self, env):
    tile_x, tile_z = self.get_curr_tile(env)['coords']

    # Based on direction, get surrounding objects and agents
    self.get_obstacles(env, tile_x, tile_z-1) 
    self.get_obstacles(env, tile_x+1, tile_z) 
    self.get_obstacles(env, tile_x-1, tile_z) 
    self.get_obstacles(env, tile_x, tile_z+1) 

    # Corners
    self.get_obstacles(env, tile_x+1, tile_z+1) 
    self.get_obstacles(env, tile_x-1, tile_z+1) 
    self.get_obstacles(env, tile_x+1, tile_z-1) 
    self.get_obstacles(env, tile_x-1, tile_z-1) 

    # This one
    self.get_obstacles(env, tile_x, tile_z) 


# Return a list of objects and a list of agents present on the tile
def get_obstacles(self, env): #, tile_x, tile_z):
    # Reset the agents that are near the intersection so we recalculate at every step
    self.intersection_agents = []

    for agent in env.agents:
        if agent != self and \
            agent.states['at_intersection_entry'] or agent.states['in_intersection']:
                self.intersection_agents.append(agent)

# Reset the obstacles before getting new ones in each time step
def reset_obstacles(self, env):
    self.nearby_objects = []
    self.nearby_agents = []

# Handle each object differently
def handle_objects(self, env):
    for obj in self.nearby_objects:
        info = obj.get_object_info()
        if info['kind'] == 'trafficlight':
            print("{0}: Handling Traffic light".format(self.agent_id))
            if not obj.is_green(direction='S'):
                print("Light is Red")

# Handle each agent differently
def handle_agents(self, env):
    self_direction = self.get_direction(env)
    for agent in self.nearby_agents:
        print("{0}: Handling Agent".format(self.agent_id))