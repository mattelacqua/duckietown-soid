import sys
import os
import json

# get the query blob from the query info
def get_query_blob(env, query_info):
    """
    Query info will have structure:
    {
        query: {
            Contains what will be symbolic for what agent
        }
        env_info: {
            Contains all concrete information or reference to symbolic

            base information

            agents: {
                agentx: {
                    counterfactuals: {
                        Contains all counterfactuals for each agent. (Need to add hooks from front end)
                    }
                }
            }
        }
    }

    General query blob structure:
    {
        environment: {
            intersection_x: ... ,
            intersection_y: ... ,
            tile_size: ... ,
            etc... ,
        } ,
        agents: {
            agent0: {
                concrete: {
                    pos_x: 2.2 ,
                    pos_y: 1.8 ,
                    etc... ,
                }
                symbolic: { (must be expressed in formula form)
                    angle: {
                        is_operator: true,
                        is_logical: false,
                        is_arithmetic: true,
                        operator: <=,
                        proposition: None,
                        lchild: {
                            is_operator: false,
                            is_logical: false,
                            is_arithmetic: false,
                            operator: None,
                            proposition: angle,
                            lchild: None,
                            rchild: None,
                        } ,
                        rchild: {
                            is_operator: false,
                            is_logical: false,
                            is_arithmetic: false,
                            operator: None,
                            proposition: 270,
                            lchild: None,
                            rchild: None,
                        } ,
                    } 
                    lookahead: {...},
                    etc... ,
                },
                state: {
                    turn_choice : ... ,
                    patience : ... ,
                    intersection_arrival : ... ,
                } ,
            } ,
            agent1: {
                concrete: {
                    angle: ... ,
                    speed: ... ,
                    etc... ,
                }
                symbolic: {
                    pos_x: {...} ,
                    pos_y: {...},
                    etc...
                } ,        
                state: {
                    etc... ,
                }
            } ,
            etc... , 
        },
        query: {
            is_factual: false 
            is_existential: true 
            behavior: 'move'
        }
    }
    """

    def get_environment(query_info):
        env_info = query_info['env_info']
        environment = {
            'intersection_x': env_info['intersection_x'],
            'intersection_z': env_info['intersection_z'],
            'robot_length': env_info['robot_length'],
            'grid_w': env_info['grid_w'],
            'grid_h': env_info['grid_h'],
            'road_tile_size': env_info['road_tile_size'],
            'max_steps': env_info['max_steps'],
            'num_agents': env_info['num_agents'],
        }
        return environment

    def get_agents(query_info):
        def get_agent(agent_info):
            # if they can be counterfactual, make sure the check is there.
            def parse_symbolic_cf(cf):
                """
                {
                    is_pos_x: bool,
                    is_pos_y: bool,
                    is_angle: bool,
                    is_forward_step: bool,
                    is_light: bool,
                    lights: {...},
                    is_value: bool,
                    is_range: bool,
                    range: {
                        is_gt: bool,
                        is_lt: bool,
                        is_gte: bool,
                        is_lte: bool,
                        low_bound: float/inf ,
                        high_bound: float/inf ,
                    },
                }
                """                
                symbolic = cf
                return symbolic

            agent = {
                'concrete' : {
                    'id': agent_info['id'],
                    'agent_id': agent_info['agent_id'],
                    'pos_x': None if agent_info['counterfactuals']['pos_x'] 
                        else agent_info['pos_x'],
                    'pos_z': None if agent_info['counterfactuals']['pos_z'] 
                        else agent_info['pos_z'],
                    'angle': None if agent_info['counterfactuals']['angle']
                        else agent_info['angle'],
                    'forward_step': None if agent_info['counterfactuals']['forward_step'] 
                        else agent_info['forward_step'],
                    'lights': None if agent_info['counterfactuals']['lights'] 
                        else agent_info['lights'],
                    'lookahead': agent_info['lookahead'],
                    'color': agent_info['color'],
                },
                'symbolic' : {
                    'pos_x': None if not agent_info['counterfactuals']['pos_x'] 
                        else parse_symbolic_cf(agent_info['counterfactuals']['pos_x']),
                    'pos_y': None if not agent_info['counterfactuals']['pos_z'] 
                        else parse_symbolic_cf(agent_info['counterfactuals']['pos_z']),
                    'angle': None if not agent_info['counterfactuals']['angle']
                        else parse_symbolic_cf(agent_info['counterfactuals']['angle']),
                    'forward_step': None if not agent_info['counterfactuals']['forward_step'] 
                        else parse_symbolic_cf(agent_info['counterfactuals']['forward_step']),
                    'lights': None if not agent_info['counterfactuals']['lights'] 
                        else parse_symbolic_cf(agent_info['counterfactuals']['lights']),
                },
                'state' : {
                    'intersection_arrival': agent_info['intersection_arrival'],
                    'patience': agent_info['patience'],
                    'step_count': agent_info['step_count'],
                    'turn_choice': agent_info['turn_choice'],
                    'signal_choice': agent_info['signal_choice'],
                },
            }
            return agent

        agents_info = query_info['env_info']['agents']
        agents = {}
        for agent in agents_info:
            agents[agent['agent_id']] = get_agent(agent)

        return agents

    def get_query(query_info):
        query = {
            'is_factual': query_info['query']['is_factual'] ,
            'is_existential': query_info['query']['is_existential'] ,
            'behavior': query_info['query']['behavior'] ,
        }
        return query

    # Print the json we are working with
    environment = get_environment(query_info)
    agents = get_agents(query_info)
    query = get_query(query_info)
    query_blob = {}
    query_blob['environment'] = environment
    print("agents")
    print(agents)
    print("query")
    print(query)
    query_blob['agents'] = dict(agents)
    query_blob['query'] = dict(query)

    return query_blob

# Generate the klee file
def generate_klee_file(query_blob):
    """
    This function will generate the klee file used by soid. 
    
    TODOs.:
    1. Parsing of the query blob into variable instances.
        - The query blob contains concrete information about the enviornment
        - The query blob will have a section for each agent
            - Each agent will have a set of concrete variables
            - Each agent will have a set of state (where it is coming from, where is it going)
            - Each agent will have a set of symbolic propositions in a formulaic tree
                - This needs to be parsed and these variables need to be identified to klee as symbolic.
        - The query blob will always be asking the query from the perspective of agent0. The question will always be if the agent will choose to proceed or not. There will be in an indicator as to if we are asking an existential (does there exist an instance where it moves) or factual question (does the agent always do this). 
    2. Gathering of the agent's learning state.
        a. create an EnvInfo struct (types.c) using the variables from above.
            - You will have to compute any computed value here as well. These are
                - prev_pos_x, prev_pos_z, stop_x, stop_z, tile_x, tile_z, angle_deg, direction
        b. gather the agent's learning state information by calling the following functions and updating the agent's learning state in the the EnvInfo struct in sequence
            - This means 10 for loops (because some learning states require other learning states info)
            The functions in order are:
                1. in_intersection
                2. at_intersection_entry
                3. intersection_empty
                4. approaching_intersection
                5. object_in_range
                6. has_right_of_way
                7. cars_waiting_to_enter
                8. car_entering_range
                9. obj_behind_intersection
                10. is_tailgating
    3. Convert the learning state to a model number (using the get_learning_state function)
    4. Call out to the proceed_model function given the model number and the agent's q_table.
        - I will add the q_table to the agent's object sometime this week.
    5. Generate the klee makefile
        - see doc.
    6. Return a file descriptor (or maybe path) to the generated klee file.

    """
    # return file_descriptor, file_path
    return None

# Generate the soid query
def generate_soid_query(query_info):
    """
    Will have to reach out to sam for this. I am under the impression of the following tasks:

    1. Describe the query. 
        - This is done in the gui by the user, so assuming this is trivial. Maybe printing the formula in readable terms like:
            - if factual
                - Does the agent <specified question from query>, given the displayed scenario and the following concrete variables:
                    - var 1
                    - var 2
                    - etc.
            - if existential
                - Does there exist a scenario in which the agent <specified question from query>, given the displayed symbolic scenario and the following concrete/symbolic variables:
    2. Define the environment:
        - Some of the learning state will be in here 
            (all instances that deal with env or other agents: ex. intersection_empty, cars_waiting_to_enter)
    3. Definte the state:
        - Rest of learning state will be in here 
            (all individually deducible ones: ex. approaching intersection)
    4. Soid behavior 
        - invoking if the agent will proceed from the klee file and seeing what the boolean answer is

    """
    # return soid_query
    return None

# Invoke the soid and return the result
def invoke_soid(soid_query, klee_file):
    """
    This function will invoke soid given the path to the files and the soid queries.
    Will likely need assistance from Sam on this. General outline is described in doc.
    """
    # return soid_result
    return None