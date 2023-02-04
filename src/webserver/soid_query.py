import soid 
from soid.soidlib import *
import json
# Generate the soid query
def get_dl_direction(direction):
    if direction == 'Straight':
        return 0
    if direction == 'Left':
        return 1
    if direction == 'Right':
        return 2
def generate_soid_query(query_info):
    """
    generate the soid query

    """

    oracle = soid.Oracle()
    klee_prefix = "src/webserver/soid_files/klee/"
    make = klee_prefix + 'makefile'

    query = soid.soidlib.Soid('GUI Query', soid.soidlib.verification) # counterfactual.single for 'exists queries' : counterfactual.verification for 'for all queries'


    q_environment = query_blob['environment']
    agents = query_blob['agents']

    # Sort out the variables
    t_environment = []
    t_state = []

    # For each of the agents, lets preprocess for easier lambda stuff later
    for i in range(int(q_environment['num_agents'])):
        
        
        # If we are on the first agent, who is the agent who's perspective matters
        agent = agents[f'agent{i}']
        if i == 0:
            # Go through all of the counterfactuals
            if agent["concrete"]["pos_x"]:
                t_environment.append({
                    'id': agent['concrete']['id'],
                    'is_cf': False,
                    'cf': None,
                    'cf_type': '',
                    'is_val': True,
                    'val_type': 'pos_x',
                    'val': agent["concrete"]["pos_x"],
                })

            if agent["concrete"]["pos_z"]:
                t_environment.append({
                    'id': agent['concrete']['id'],
                    'is_cf': False,
                    'cf': None,
                    'cf_type': '',
                    'is_val': True,
                    'val_type': 'pos_z',
                    'val': agent["concrete"]["pos_z"],
                })

            if agent["concrete"]["angle"]:
                t_environment.append({
                    'id': agent['concrete']['id'],
                    'is_cf': False,
                    'cf': None,
                    'cf_type': '',
                    'is_val': True,
                    'val_type': 'angle',
                    'val': agent["concrete"]["angle"],
                })

            if agent["concrete"]["forward_step"]:
                t_environment.append({
                    'id': agent['concrete']['id'],
                    'is_cf': False,
                    'cf': None,
                    'cf_type': '',
                    'is_val': True,
                    'val_type': 'forward_step',
                    'val': agent["concrete"]["forward_step"],
                })

            if agent["concrete"]["speed"]:
                t_environment.append({
                    'id': agent['concrete']['id'],
                    'is_cf': False,
                    'cf': None,
                    'cf_type': '',
                    'is_val': True,
                    'val_type': 'speed',
                    'val': agent["concrete"]["speed"],
                })
            
            # Environmental counterfactuals
            for counterfactual in agent['symbolic']['list_pos_x']:
                t_environment.append({
                    'id': agent['concrete']['id'],
                    'is_cf': True,
                    'cf_type': 'pos_x',
                    'cf': counterfactual,
                    'is_val': False,
                    'val_type': '',
                    'val': None,
                })

            for counterfactual in agent['symbolic']['list_pos_z']:
                t_environment.append({
                    'id': agent['concrete']['id'],
                    'is_cf': True,
                    'cf_type': 'pos_z',
                    'cf': counterfactual,
                    'is_val': False,
                    'val_type': '',
                    'val': None,
                })

            for counterfactual in agent['symbolic']['list_angle']:
                t_environment.append({
                    'id': agent['concrete']['id'],
                    'is_cf': True,
                    'cf': counterfactual,
                    'cf_type': 'angle',
                    'is_val': False,
                    'val_type': '',
                    'val': None,
                })

            for counterfactual in agent['symbolic']['list_speed']:
                t_environment.append({
                    'id': agent['concrete']['id'],
                    'is_cf': True,
                    'cf': counterfactual,
                    'cf_type': 'speed',
                    'is_val': False,
                    'val_type': '',
                    'val': None,
                })          

            # State counterfactuals
            for counterfactual in agent['symbolic']['list_forward_step']:
                t_state.append({
                    'id': agent['concrete']['id'],
                    'is_cf': True,
                    'cf': counterfactual,
                    'cf_type': 'forward_step',
                    'is_val': False,
                    'val_type': '',
                    'val': None,
                })          

            for counterfactual in agent['symbolic']['list_turn_choice']:
                t_state.append({
                    'id': agent['concrete']['id'],
                    'is_cf': True,
                    'cf': counterfactual,
                    'cf_type': 'turn_choice',
                    'is_val': False,
                    'val_type': '',
                    'val': None,
                })          

            for counterfactual in agent['symbolic']['list_signal_choice']:
                t_state.append({
                    'id': agent['concrete']['id'],
                    'is_cf': True,
                    'cf': counterfactual,
                    'cf_type': 'signal_choice',
                    'is_val': False,
                    'val_type': '',
                    'val': None,
                })          


            
            # Add agent0's lookahead, initial_direction, intersection_Arrival, patience, step count to STATE
            # lookahead
            t_state.append({
                'id': agent['concrete']['id'],
                'is_cf': False,
                'cf': None,
                'cf_type': '',
                'is_val': True,
                'val_type': 'lookahead',
                'val': agent['concrete']['lookahead'],
            })
            # inital_direction
            t_state.append({
                'id': agent['concrete']['id'],
                'is_cf': False,
                'cf': None,
                'cf_type': '',
                'is_val': True,
                'val_type': 'initial_direction',
                'val': agent['state']['initial_direction'],
            })
            # intersection_arrival
            t_state.append({
                'id': agent['concrete']['id'],
                'is_cf': False,
                'cf': None,
                'cf_type': '',
                'is_val': True,
                'val_type': 'intersection_arrival',
                'val': agent['state']['intersection_arrival'],
            })            
            # patience
            t_state.append({
                'id': agent['concrete']['id'],
                'is_cf': False,
                'cf': None,
                'cf_type': '',
                'is_val': True,
                'val_type': 'patience',
                'val': agent['state']['patience'],
            })            
            # step_count
            t_state.append({
                'id': agent['concrete']['id'],
                'is_cf': False,
                'cf': None,
                'cf_type': '',
                'is_val': True,
                'val_type': 'step_count',
                'val': agent['state']['step_count'],
            })            

        if i > 0:
            # Go through all of the counterfactuals
            if agent["concrete"]["pos_x"]:
                t_environment.append({
                    'id': agent['concrete']['id'],
                    'is_cf': False,
                    'cf': None,
                    'cf_type': '',
                    'is_val': True,
                    'val_type': 'pos_x',
                    'val': agent["concrete"]["pos_x"],
                })

            if agent["concrete"]["pos_z"]:
                t_environment.append({
                    'id': agent['concrete']['id'],
                    'is_cf': False,
                    'cf': None,
                    'cf_type': '',
                    'is_val': True,
                    'val_type': 'pos_z',
                    'val': agent["concrete"]["pos_z"],
                })

            if agent["concrete"]["angle"]:
                t_environment.append({
                    'id': agent['concrete']['id'],
                    'is_cf': False,
                    'cf': None,
                    'cf_type': '',
                    'is_val': True,
                    'val_type': 'angle',
                    'val': agent["concrete"]["angle"],
                })

            if agent["concrete"]["forward_step"]:
                t_environment.append({
                    'id': agent['concrete']['id'],
                    'is_cf': False,
                    'cf': None,
                    'cf_type': '',
                    'is_val': True,
                    'val_type': 'forward_step',
                    'val': agent["concrete"]["forward_step"],
                })

            if agent["concrete"]["speed"]:
                t_environment.append({
                    'id': agent['concrete']['id'],
                    'is_cf': False,
                    'cf': None,
                    'cf_type': '',
                    'is_val': True,
                    'val_type': 'speed',
                    'val': agent["concrete"]["speed"],
                })

            if agent["concrete"]["signal_choice"]:
                t_environment.append({
                    'id': agent['concrete']['id'],
                    'is_cf': False,
                    'cf': None,
                    'cf_type': '',
                    'is_val': True,
                    'val_type': 'signal_choice',
                    'val': agent["concrete"]["signal_choice"],
                })

            if agent["concrete"]["turn_choice"]:
                t_environment.append({
                    'id': agent['concrete']['id'],
                    'is_cf': False,
                    'cf': None,
                    'cf_type': '',
                    'is_val': True,
                    'val_type': 'turn_choice',
                    'val': agent["concrete"]["turn_choice"],
                })


            # Environmental counterfactuals
            for counterfactual in agent['symbolic']['list_pos_x']:
                t_environment.append({
                    'id': agent['concrete']['id'],
                    'is_cf': True,
                    'cf_type': 'pos_x',
                    'cf': counterfactual,
                    'is_val': False,
                    'val_type': '',
                    'val': None,
                })

            for counterfactual in agent['symbolic']['list_pos_z']:
                t_environment.append({
                    'id': agent['concrete']['id'],
                    'is_cf': True,
                    'cf_type': 'pos_z',
                    'cf': counterfactual,
                    'is_val': False,
                    'val_type': '',
                    'val': None,
                })

            for counterfactual in agent['symbolic']['list_angle']:
                t_environment.append({
                    'id': agent['concrete']['id'],
                    'is_cf': True,
                    'cf': counterfactual,
                    'cf_type': 'angle',
                    'is_val': False,
                    'val_type': '',
                    'val': None,
                })

            for counterfactual in agent['symbolic']['list_speed']:
                t_environment.append({
                    'id': agent['concrete']['id'],
                    'is_cf': True,
                    'cf': counterfactual,
                    'cf_type': 'speed',
                    'is_val': False,
                    'val_type': '',
                    'val': None,
                })          

            for counterfactual in agent['symbolic']['list_forward_step']:
                t_environment.append({
                    'id': agent['concrete']['id'],
                    'is_cf': True,
                    'cf': counterfactual,
                    'cf_type': 'forward_step',
                    'is_val': False,
                    'val_type': '',
                    'val': None,
                })          

            for counterfactual in agent['symbolic']['list_turn_choice']:
                t_environment.append({
                    'id': agent['concrete']['id'],
                    'is_cf': True,
                    'cf': counterfactual,
                    'cf_type': 'turn_choice',
                    'is_val': False,
                    'val_type': '',
                    'val': None,
                })          

            for counterfactual in agent['symbolic']['list_signal_choice']:
                t_environment.append({
                    'id': agent['concrete']['id'],
                    'is_cf': True,
                    'cf': counterfactual,
                    'cf_type': 'signal_choice',
                    'is_val': False,
                    'val_type': '',
                    'val': None,
                })          

            # Add non=agent0's lookahead, initial_direction, intersection_Arrival, patience, step count to ENVIORNMENT
            # lookahead
            t_environment.append({
                'id': agent['concrete']['id'],
                'is_cf': False,
                'cf': None,
                'cf_type': '',
                'is_val': True,
                'val_type': 'lookahead',
                'val': agent['concrete']['lookahead'],
            })
            # inital_direction
            t_environment.append({
                'id': agent['concrete']['id'],
                'is_cf': False,
                'cf': None,
                'cf_type': '',
                'is_val': True,
                'val_type': 'initial_direction',
                'val': agent['state']['initial_direction'],
            })
            # intersection_arrival
            t_environment.append({
                'id': agent['concrete']['id'],
                'is_cf': False,
                'cf': None,
                'cf_type': '',
                'is_val': True,
                'val_type': 'intersection_arrival',
                'val': agent['state']['intersection_arrival'],
            })            
            # patience
            t_environment.append({
                'id': agent['concrete']['id'],
                'is_cf': False,
                'cf': None,
                'cf_type': '',
                'is_val': True,
                'val_type': 'patience',
                'val': agent['state']['patience'],
            })            
            # step_count
            t_environment.append({
                'id': agent['concrete']['id'],
                'is_cf': False,
                'cf': None,
                'cf_type': '',
                'is_val': True,
                'val_type': 'step_count',
                'val': agent['state']['step_count'],
            })

    def declare():
        # declare Environment
        E = {}
        for tagged_cf in t_environment:
            a_id = int(tagged_cf['id'])
            if tagged_cf['is_cf']:
                counterfactual = tagged_cf['cf']
                if counterfactual['is_pos_x']:
                    E[f'agent{a_id}_pos_x'] = soid.soidlib.types.float(f'agent{a_id}_pos_x', pp=None, raw=None)
                if counterfactual['is_pos_z']:
                    E[f'agent{a_id}_pos_z'] = soid.soidlib.types.float(f'agent{a_id}_pos_z', pp=None, raw=None)
                if counterfactual['is_angle']:
                    E[f'agent{a_id}_angle'] = soid.soidlib.types.float(f'agent{a_id}_angle', pp=None, raw=None)
                if counterfactual['is_forward_step']:
                    E[f'agent{a_id}_forward_step'] = soid.soidlib.types.float(f'agent{a_id}_forward_step', pp=None, raw=None)
                if counterfactual['is_speed']:
                    E[f'agent{a_id}_speed'] = soid.soidlib.types.float(f'agent{a_id}_speed', pp=None, raw=None)
                if counterfactual['is_turnchoice']:
                    E[f'agent{a_id}_turn_choice'] = soid.soidlib.types.int_bv(f'agent{a_id}_turn_choice', pp=None, raw=None)
                if counterfactual['is_signalchoice']:
                    E[f'agent{a_id}_signal_choice'] = soid.soidlib.types.int_bv(f'agent{a_id}_signal_choice', pp=None, raw=None)
            elif tagged_cf['is_val']:
                val_type = tagged_cf['val_type']
                if val_type == 'pos_x':
                    E[f'agent{a_id}_pos_x'] = soid.soidlib.types.float(f'agent{a_id}_pos_x', pp=None, raw=None)
                if val_type == 'pos_z':
                    E[f'agent{a_id}_pos_z'] = soid.soidlib.types.float(f'agent{a_id}_pos_z', pp=None, raw=None)
                if val_type == 'angle':
                    E[f'agent{a_id}_angle'] = soid.soidlib.types.float(f'agent{a_id}_angle', pp=None, raw=None)
                if val_type == 'forward_step':
                    E[f'agent{a_id}_forward_step'] = soid.soidlib.types.float(f'agent{a_id}_forward_step', pp=None, raw=None)
                if val_type == 'speed':
                    E[f'agent{a_id}_speed'] = soid.soidlib.types.float(f'agent{a_id}_speed', pp=None, raw=None)
                if val_type == 'signal_choice':
                    E[f'agent{a_id}_signal_choice'] = soid.soidlib.types.int_bv(f'agent{a_id}_signal_choice', pp=None, raw=None)
                if val_type == 'turn_choice':
                    E[f'agent{a_id}_turn_choice'] = soid.soidlib.types.int_bv(f'agent{a_id}_turn_choice', pp=None, raw=None)
                if val_type == 'lookahead':
                    E[f'agent{a_id}_lookahead'] = soid.soidlib.types.float(f'agent{a_id}_lookahead', pp=None, raw=None)
                if val_type == 'intersection_arrival':
                    E[f'agent{a_id}_intersection_arrival'] = soid.soidlib.types.int_bv(f'agent{a_id}_intersection_arrival', pp=None, raw=None)
                if val_type == 'initial_direction':
                    E[f'agent{a_id}_initial_direction'] = soid.soidlib.types.int_bv(f'agent{a_id}_initial_direction', pp=None, raw=None)
                if val_type == 'patience':
                    E[f'agent{a_id}_patience'] = soid.soidlib.types.int_bv(f'agent{a_id}_patience', pp=None, raw=None)
                if val_type == 'step_count':
                    E[f'agent{a_id}_step_count'] = soid.soidlib.types.int_bv(f'agent{a_id}_step_count', pp=None, raw=None)
        
        # declare state
        S = {}
        for tagged_cf in t_state:
            a_id = int(tagged_cf['id'])
            if tagged_cf['is_cf']:
                counterfactual = tagged_cf['cf']
                if counterfactual['is_pos_x']:
                    S[f'agent{a_id}_pos_x'] = soid.soidlib.types.float(f'agent{a_id}_pos_x', pp=None, raw=None)
                if counterfactual['is_pos_z']:
                    S[f'agent{a_id}_pos_z'] = soid.soidlib.types.float(f'agent{a_id}_pos_z', pp=None, raw=None)
                if counterfactual['is_angle']:
                    S[f'agent{a_id}_angle'] = soid.soidlib.types.float(f'agent{a_id}_angle', pp=None, raw=None)
                if counterfactual['is_forward_step']:
                    S[f'agent{a_id}_forward_step'] = soid.soidlib.types.float(f'agent{a_id}_forward_step', pp=None, raw=None)
                if counterfactual['is_speed']:
                    S[f'agent{a_id}_speed'] = soid.soidlib.types.float(f'agent{a_id}_speed', pp=None, raw=None)
                if counterfactual['is_turnchoice']:
                    S[f'agent{a_id}_turn_choice'] = soid.soidlib.types.int_bv(f'agent{a_id}_turn_choice', pp=None, raw=None)
                if counterfactual['is_signalchoice']:
                    S[f'agent{a_id}_signal_choice'] = soid.soidlib.types.int_bv(f'agent{a_id}_signal_choice', pp=None, raw=None)
            elif tagged_cf['is_val']:
                val_type = tagged_cf['val_type']
                if val_type == 'pos_x':
                    S[f'agent{a_id}_pos_x'] = soid.soidlib.types.float(f'agent{a_id}_pos_x', pp=None, raw=None)
                if val_type == 'pos_z':
                    S[f'agent{a_id}_pos_z'] = soid.soidlib.types.float(f'agent{a_id}_pos_z', pp=None, raw=None)
                if val_type == 'angle':
                    S[f'agent{a_id}_angle'] = soid.soidlib.types.float(f'agent{a_id}_angle', pp=None, raw=None)
                if val_type == 'forward_step':
                    S[f'agent{a_id}_forward_step'] = soid.soidlib.types.float(f'agent{a_id}_forward_step', pp=None, raw=None)
                if val_type == 'speed':
                    S[f'agent{a_id}_speed'] = soid.soidlib.types.float(f'agent{a_id}_speed', pp=None, raw=None)
                if val_type == 'signal_choice':
                    S[f'agent{a_id}_signal_choice'] = soid.soidlib.types.int_bv(f'agent{a_id}_signal_choice', pp=None, raw=None)
                if val_type == 'turn_choice':
                    S[f'agent{a_id}_turn_choice'] = soid.soidlib.types.int_bv(f'agent{a_id}_turn_choice', pp=None, raw=None)
                if val_type == 'lookahead':
                    S[f'agent{a_id}_lookahead'] = soid.soidlib.types.float(f'agent{a_id}_lookahead', pp=None, raw=None)
                if val_type == 'intersection_arrival':
                    S[f'agent{a_id}_intersection_arrival'] = soid.soidlib.types.int_bv(f'agent{a_id}_intersection_arrival', pp=None, raw=None)
                if val_type == 'initial_direction':
                    S[f'agent{a_id}_initial_direction'] = soid.soidlib.types.int_bv(f'agent{a_id}_initial_direction', pp=None, raw=None)
                if val_type == 'patience':
                    S[f'agent{a_id}_patience'] = soid.soidlib.types.int_bv(f'agent{a_id}_patience', pp=None, raw=None)
                if val_type == 'step_count':
                    S[f'agent{a_id}_step_count'] = soid.soidlib.types.int_bv(f'agent{a_id}_step_count', pp=None, raw=None)
        
        # declare behaviors
        D = {}
        for i in range(int(q_environment['num_agents'])):
            D[f'agent{i}_prev_pos_x'] = soid.soidlib.types.float(f'agent{i}_prev_pos_x', pp=None, raw=None)
            D[f'agent{i}_prev_pos_z'] = soid.soidlib.types.float(f'agent{i}_prev_pos_z', pp=None, raw=None)
            D[f'agent{i}_stop_x'] = soid.soidlib.types.float(f'agent{i}_stop_x', pp=None, raw=None)
            D[f'agent{i}_stop_z'] = soid.soidlib.types.float(f'agent{i}_stop_z', pp=None, raw=None)

            D[f'agent{i}_direction'] = soid.soidlib.types.int_bv(f'agent{i}_direction', pp=None, raw=None)
            D[f'agent{i}_tile_x'] = soid.soidlib.types.int_bv(f'agent{i}_tile_x', pp=None, raw=None)
            D[f'agent{i}_tile_z'] = soid.soidlib.types.int_bv(f'agent{i}_tile_z', pp=None, raw=None)

            
            D[f'agent{i}_state_in_intersection'] = soid.soidlib.types.bool_bv(f'agent{i}_state_in_intersection', pp=None, raw=None)
            D[f'agent{i}_state_at_intersection_entry'] = soid.soidlib.types.bool_bv(f'agent{i}_state_at_intersection_entry', pp=None, raw=None)
            D[f'agent{i}_state_intersection_empty'] = soid.soidlib.types.bool_bv(f'agent{i}_state_intersection_empty', pp=None, raw=None)
            D[f'agent{i}_state_approaching_intersection'] = soid.soidlib.types.bool_bv(f'agent{i}_state_approaching_intersection', pp=None, raw=None)
            D[f'agent{i}_state_in_obj_in_range'] = soid.soidlib.types.bool_bv(f'agent{i}_state_in_obj_in_range', pp=None, raw=None)
            D[f'agent{i}_state_in_has_right_of_way'] = soid.soidlib.types.bool_bv(f'agent{i}_state_in_has_right_of_way', pp=None, raw=None)
            D[f'agent{i}_state_safe_to_enter'] = soid.soidlib.types.bool_bv(f'agent{i}_state_safe_to_enter', pp=None, raw=None)
            D[f'agent{i}_state_cars_waiting_to_enter'] = soid.soidlib.types.bool_bv(f'agent{i}_state_cars_waiting_to_enter', pp=None, raw=None)
            D[f'agent{i}_state_car_entering_range'] = soid.soidlib.types.bool_bv(f'agent{i}_state_car_entering_range', pp=None, raw=None)
            D[f'agent{i}_state_obj_behind_intersection'] = soid.soidlib.types.bool_bv(f'agent{i}_state_obj_behind_intersection', pp=None, raw=None)
            D[f'agent{i}_state_is_tailgating'] = soid.soidlib.types.bool_bv(f'agent{i}_state_is_tailgating', pp=None, raw=None)
            D[f'agent{i}_state_next_to_go'] = soid.soidlib.types.bool_bv(f'agent{i}_state_next_to_go', pp=None, raw=None)
            
        D[f'mrow'] = soid.soidlib.types.int_bv(f'mrow', pp=None, raw=None)
        D[f'will_proceed'] = soid.soidlib.types.bool_bv(f'will_proceed', pp=None, raw=None)
        
        return E,S, D

    # Register declare
    query.register(declare)

    def get_constraint(declare_type, tagged_cf):
        if tagged_cf['is_cf']:
            counterfactual = tagged_cf['cf']
            if counterfactual['is_value']:
                if counterfactual['is_pos_x']:
                    return Equal( declare_type[f"agent{tagged_cf['id']}_pos_x"], float(counterfactual['value']))
                if counterfactual['is_pos_z']:
                    return Equal( declare_type[f"agent{tagged_cf['id']}_pos_z"], float(counterfactual['value']))
                if counterfactual['is_angle']:
                    return Equal( declare_type[f"agent{tagged_cf['id']}_angle"], float(counterfactual['value']))
                if counterfactual['is_speed']:
                    return Equal( declare_type[f"agent{tagged_cf['id']}_speed"], float(counterfactual['value']))
                if counterfactual['is_forward_step']:
                    return Equal( declare_type[f"agent{tagged_cf['id']}_forward_step"], float(counterfactual['value']))
                if counterfactual['is_turnchoice']:
                    direction = counterfactual['value']
                    if direction == "Straight":
                        direction = 0
                    if direction == "Left":
                        direction = 1
                    if direction == "Right":
                        direction = 2
                    return Equal( declare_type[f"agent{tagged_cf['id']}_turn_choice"], int(direction))
                if counterfactual['is_signalchoice']:
                    direction = counterfactual['value']
                    if direction == "Straight":
                        direction = 0
                    if direction == "Left":
                        direction = 1
                    if direction == "Right":
                        direction = 2
                    return Equal( declare_type[f"agent{tagged_cf['id']}_signal_choice"], int(direction))
            if counterfactual['is_range']:
                low_bound = counterfactual['range']['low_bound']
                high_bound = counterfactual['range']['high_bound']
                turn_choices = counterfactual['range']['turn_choices']
                if counterfactual['is_pos_x']:
                    return  And( 
                            FP_GTE(declare_type[f"agent{tagged_cf['id']}_pos_x"], float(low_bound)),
                            FP_LTE(declare_type[f"agent{tagged_cf['id']}_pos_x"], float(high_bound)))
                if counterfactual['is_pos_z']:
                    return  And( 
                            FP_GTE(declare_type[f"agent{tagged_cf['id']}_pos_z"], float(low_bound)),
                            FP_LTE(declare_type[f"agent{tagged_cf['id']}_pos_z"], float(high_bound)))
                if counterfactual['is_angle']:
                    return  And( 
                            FP_GTE(declare_type[f"agent{tagged_cf['id']}_angle"], float(low_bound)),
                            FP_LTE(declare_type[f"agent{tagged_cf['id']}_angle"], float(high_bound)))
                if counterfactual['is_speed']:
                    return  And( 
                            FP_GTE(declare_type[f"agent{tagged_cf['id']}_speed"], float(low_bound)),
                            FP_LTE(declare_type[f"agent{tagged_cf['id']}_speed"], float(high_bound)))
                if counterfactual['is_forward_step']:
                    return  And( 
                            FP_GTE(declare_type[f"agent{tagged_cf['id']}_forward_step"], float(low_bound)),
                            FP_LTE(declare_type[f"agent{tagged_cf['id']}_forward_step"], float(high_bound)))
                if counterfactual['is_turnchoice']:
                    direction_formula = False
                    for direction in turn_choices:
                        if direction == 'Straight':
                            direction = 0
                        if direction == 'Left':
                            direction = 1
                        if direction == 'Right':
                            direction = 2
                        if not direction_formula:
                            direction_formula = Equal(declare_type[f"agent{tagged_cf['id']}_turn_choice"], int(direction))
                            continue
                        direction_formula = Or (
                            Equal(declare_type[f"agent{tagged_cf['id']}_turn_choice"], int(direction)),
                            direction_formula
                        )
                    return direction_formula
                if counterfactual['is_signalchoice']:
                    direction_formula = None
                    for direction in turn_choices:
                        if direction == 'Straight':
                            direction = 0
                        if direction == 'Left':
                            direction = 1
                        if direction == 'Right':
                            direction = 2
                        if not direction_formula:
                            direction_formula = Equal(declare_type[f"agent{tagged_cf['id']}_signal_choice"], int(direction))
                            continue
                        direction_formula = Or (
                            Equal(declare_type[f"agent{tagged_cf['id']}_signal_choice"], int(direction)),
                            direction_formula
                        )
                    return direction_formula
        if tagged_cf['is_val']:
            value = tagged_cf['val']
            val_type = tagged_cf['val_type']
            if val_type == 'pos_x':
                return Equal(declare_type[f"agent{tagged_cf['id']}_pos_x"], float(value))
            if val_type == 'pos_z':
                return Equal(declare_type[f"agent{tagged_cf['id']}_pos_z"], float(value))
            if val_type == 'angle':
                return Equal(declare_type[f"agent{tagged_cf['id']}_angle"], float(value))
            if val_type == 'forward_step':
                return Equal(declare_type[f"agent{tagged_cf['id']}_forward_step"], float(value))
            if val_type == 'speed':
                return Equal(declare_type[f"agent{tagged_cf['id']}_speed"], float(value))
            if val_type == 'turn_choice':
                return Equal(declare_type[f"agent{tagged_cf['id']}_turn_choice"], int(get_dl_direction(value)))
            if val_type == 'signal_choice':
                return Equal(declare_type[f"agent{tagged_cf['id']}_signal_choice"], int(get_dl_direction(value)))
            if val_type == 'lookahead':
                return Equal(declare_type[f"agent{tagged_cf['id']}_lookahead"], float(value))
            if val_type == 'intersection_arrival':
                return Equal(declare_type[f"agent{tagged_cf['id']}_intersection_arrival"], int(value))
            if val_type == 'initial_direction':
                return Equal(declare_type[f"agent{tagged_cf['id']}_initial_direction"], int(value))
            if val_type == 'patience':
                return Equal(declare_type[f"agent{tagged_cf['id']}_patience"], int(value))
            if val_type == 'step_count':
                return Equal(declare_type[f"agent{tagged_cf['id']}_step_count"], int(value))

    def get_sub_formula(declare_type, tagged_cf_list):
        sub_formula = None
        for tagged_cf in tagged_cf_list:
            if sub_formula == None:
                sub_formula = get_constraint(declare_type, tagged_cf)
                continue
            sub_formula = Or (
                get_constraint(declare_type, tagged_cf),
                formula)
        return sub_formula

    def encode(declare_type, tagged_cf_list):
        cf_lists = []

        # preprocess lists in to disjunctions
        for i in range(q_environment['num_agents']):
            list_pos_x = []
            list_pos_z = []
            list_angle = []
            list_forward_step = []
            list_speed = []
            list_signal_choice = []
            list_turn_choice = []
            list_lookahead = []
            list_intersection_arrival = []
            list_initial_direction = []
            list_patience = []
            list_step_count = []
            for cf in tagged_cf_list:
                if i == cf['id'] and (cf['val_type'] == 'pos_x' or cf['cf_type'] == 'pos_x'):
                    list_pos_x.append(cf)
                elif i == cf['id'] and (cf['val_type'] == 'pos_z' or cf['cf_type'] == 'pos_z'):
                    list_pos_z.append(cf)
                elif i == cf['id'] and (cf['val_type'] == 'angle' or cf['cf_type'] == 'angle'):
                    list_angle.append(cf)
                elif i == cf['id'] and (cf['val_type'] == 'forward_step' or cf['cf_type'] == 'forward_step'):
                    list_forward_step.append(cf)
                elif i == cf['id'] and (cf['val_type'] == 'speed' or cf['cf_type'] == 'speed'):
                    list_speed.append(cf)
                elif i == cf['id'] and (cf['val_type'] == 'signal_choice' or cf['cf_type'] == 'signal_choice'):
                    list_signal_choice.append(cf)
                elif i == cf['id'] and (cf['val_type'] == 'turn_choice' or cf['cf_type'] == 'turn_choice'):
                    list_turn_choice.append(cf)
                elif i == cf['id'] and (cf['val_type'] == 'lookahead' or cf['cf_type'] == 'lookahead'):
                    list_lookahead.append(cf);
                elif i == cf['id'] and (cf['val_type'] == 'intersection_arrival' or cf['cf_type'] == 'intersection_arrival'):
                    list_intersection_arrival.append(cf)
                elif i == cf['id'] and (cf['val_type'] == 'initial_direction' or cf['cf_type'] == 'initial_direction'):
                    list_initial_direction.append(cf)
                elif i == cf['id'] and (cf['val_type'] == 'patience' or cf['cf_type'] == 'patience'):
                    list_patience.append(cf)
                elif i == cf['id'] and (cf['val_type'] == 'step_count' or cf['cf_type'] == 'step_count'):
                    list_step_count.append(cf)
                else:
                    if i== cf['id']:
                        print("SHOULD NEVER SEE THIS. IN SOID_QUERY ENCODE")
            cf_lists.append(list_pos_x)
            cf_lists.append(list_pos_z)
            cf_lists.append(list_angle)
            cf_lists.append(list_forward_step)
            cf_lists.append(list_speed)
            cf_lists.append(list_signal_choice)
            cf_lists.append(list_turn_choice)
            cf_lists.append(list_lookahead)
            cf_lists.append(list_intersection_arrival)
            cf_lists.append(list_initial_direction)
            cf_lists.append(list_patience)
            cf_lists.append(list_step_count)

        # sort the list by types
        formula = None
        for cf_list in cf_lists:
            sub_formula = get_sub_formula(declare_type, cf_list)
            if formula == None:
                if sub_formula == None:
                    continue
                else:
                    formula = sub_formula
                continue

            print("formula:", formula)
            if sub_formula == None:
                continue
            else:
                formula = And (
                    sub_formula,
                    formula)
            
        return formula

    def environmental( E ):
        return encode(E, t_environment)
    query.environmental(environmental)

    def state( S ):
        return encode(S, t_state)
    query.state(state)

    def behavior(E, S, P ):
        return Equal(P.will_proceed, True) # This will tell us if we ever move
    query.behavior(behavior)

    # invoke soid
    print(f"Soid Results:")
    (info, res, models, resources ) = soid.invoke(oracle, make, query)
    print(f"Result: {res} Resources: {resources}")
    model_prefix = "src/webserver/soid_files/klee/models/"
    # open klee file
    model_file = open((model_prefix + "model.out"), 'w', encoding="utf-8")
    model_file.write(f"{models[0]}")
    model_file.close()


    # Ignore info
    # Res is the result
    # Models is empty or models[0] is the model
    # resources is the timing of the query
    return res, models, resources


if __name__ == '__main__':
    query_blob = json.load(open('src/webserver/soid_files/query_blobs/query_blob'))
    print(query_blob)
    result, models, resources = generate_soid_query(query_blob)