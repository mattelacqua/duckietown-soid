import sys
import soid
import json
import os
import time

# Generate the soid query
def get_dl_direction(direction):
    if direction == 'Straight' or direction == 'straight':
        return 0
    if direction == 'Left' or direction == 'left':
        return 1
    if direction == 'Right' or direction == 'right':
        return 2

def generate_soid_query(query_blob):
    if query_blob['query']['is_universal']:
        query = soid.soidlib.Soid('GUI Query', soid.soidlib.would)
    if query_blob['query']['is_existential']:
        query = soid.soidlib.Soid('GUI Query', soid.soidlib.might)

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
            # Goes in environment
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

            # Concrete state
            if agent["concrete"]["forward_step"]:
                t_state.append({
                    'id': agent['concrete']['id'],
                    'is_cf': False,
                    'cf': None,
                    'cf_type': '',
                    'is_val': True,
                    'val_type': 'forward_step',
                    'val': agent["concrete"]["forward_step"],
                })

            if agent["concrete"]["signal_choice"]:
                t_state.append({
                    'id': agent['concrete']['id'],
                    'is_cf': False,
                    'cf': None,
                    'cf_type': '',
                    'is_val': True,
                    'val_type': 'signal_choice',
                    'val': agent["concrete"]["signal_choice"],
                })

            if agent["concrete"]["turn_choice"]:
                t_state.append({
                    'id': agent['concrete']['id'],
                    'is_cf': False,
                    'cf': None,
                    'cf_type': '',
                    'is_val': True,
                    'val_type': 'turn_choice',
                    'val': agent["concrete"]["turn_choice"],
                })

            # Add given state information to agent 0 state

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



        if i > 0:
            # Everything will go into environmental for concrete and counterfactual
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

    def declare():
        # declare Environment
        E = {}
        for tagged_cf in t_environment:
            a_id = int(tagged_cf['id'])
            if tagged_cf['is_cf']:
                counterfactual = tagged_cf['cf']
                if counterfactual['is_pos_x']:
                    E[f'agent{a_id}_pos_x'] = soid.soidlib.types.float(f'agent{a_id}_pos_x')
                if counterfactual['is_pos_z']:
                    E[f'agent{a_id}_pos_z'] = soid.soidlib.types.float(f'agent{a_id}_pos_z')
                if counterfactual['is_angle']:
                    E[f'agent{a_id}_angle'] = soid.soidlib.types.float(f'agent{a_id}_angle')
                if counterfactual['is_forward_step']:
                    E[f'agent{a_id}_forward_step'] = soid.soidlib.types.float(f'agent{a_id}_forward_step')
                if counterfactual['is_speed']:
                    E[f'agent{a_id}_speed'] = soid.soidlib.types.float(f'agent{a_id}_speed')
                if counterfactual['is_turnchoice']:
                    E[f'agent{a_id}_turn_choice'] = soid.soidlib.types.int_bv(f'agent{a_id}_turn_choice')
                if counterfactual['is_signalchoice']:
                    E[f'agent{a_id}_signal_choice'] = soid.soidlib.types.int_bv(f'agent{a_id}_signal_choice')
            elif tagged_cf['is_val']:
                val_type = tagged_cf['val_type']
                if val_type == 'pos_x':
                    E[f'agent{a_id}_pos_x'] = soid.soidlib.types.float(f'agent{a_id}_pos_x')
                if val_type == 'pos_z':
                    E[f'agent{a_id}_pos_z'] = soid.soidlib.types.float(f'agent{a_id}_pos_z')
                if val_type == 'angle':
                    E[f'agent{a_id}_angle'] = soid.soidlib.types.float(f'agent{a_id}_angle')
                if val_type == 'forward_step':
                    E[f'agent{a_id}_forward_step'] = soid.soidlib.types.float(f'agent{a_id}_forward_step')
                if val_type == 'speed':
                    E[f'agent{a_id}_speed'] = soid.soidlib.types.float(f'agent{a_id}_speed')
                if val_type == 'signal_choice':
                    E[f'agent{a_id}_signal_choice'] = soid.soidlib.types.int_bv(f'agent{a_id}_signal_choice')
                if val_type == 'turn_choice':
                    E[f'agent{a_id}_turn_choice'] = soid.soidlib.types.int_bv(f'agent{a_id}_turn_choice')
                if val_type == 'lookahead':
                    E[f'agent{a_id}_lookahead'] = soid.soidlib.types.float(f'agent{a_id}_lookahead')
                if val_type == 'intersection_arrival':
                    E[f'agent{a_id}_intersection_arrival'] = soid.soidlib.types.int_bv(f'agent{a_id}_intersection_arrival')
                if val_type == 'initial_direction':
                    E[f'agent{a_id}_initial_direction'] = soid.soidlib.types.int_bv(f'agent{a_id}_initial_direction')
                if val_type == 'patience':
                    E[f'agent{a_id}_patience'] = soid.soidlib.types.int_bv(f'agent{a_id}_patience')
                if val_type == 'step_count':
                    E[f'agent{a_id}_step_count'] = soid.soidlib.types.int_bv(f'agent{a_id}_step_count')

        # declare state
        S = {}
        for tagged_cf in t_state:
            a_id = int(tagged_cf['id'])
            if tagged_cf['is_cf']:
                counterfactual = tagged_cf['cf']
                if counterfactual['is_pos_x']:
                    S[f'agent{a_id}_pos_x'] = soid.soidlib.types.float(f'agent{a_id}_pos_x')
                if counterfactual['is_pos_z']:
                    S[f'agent{a_id}_pos_z'] = soid.soidlib.types.float(f'agent{a_id}_pos_z')
                if counterfactual['is_angle']:
                    S[f'agent{a_id}_angle'] = soid.soidlib.types.float(f'agent{a_id}_angle')
                if counterfactual['is_forward_step']:
                    S[f'agent{a_id}_forward_step'] = soid.soidlib.types.float(f'agent{a_id}_forward_step')
                if counterfactual['is_speed']:
                    S[f'agent{a_id}_speed'] = soid.soidlib.types.float(f'agent{a_id}_speed')
                if counterfactual['is_turnchoice']:
                    S[f'agent{a_id}_turn_choice'] = soid.soidlib.types.int_bv(f'agent{a_id}_turn_choice')
                if counterfactual['is_signalchoice']:
                    S[f'agent{a_id}_signal_choice'] = soid.soidlib.types.int_bv(f'agent{a_id}_signal_choice')
            elif tagged_cf['is_val']:
                val_type = tagged_cf['val_type']
                if val_type == 'pos_x':
                    S[f'agent{a_id}_pos_x'] = soid.soidlib.types.float(f'agent{a_id}_pos_x')
                if val_type == 'pos_z':
                    S[f'agent{a_id}_pos_z'] = soid.soidlib.types.float(f'agent{a_id}_pos_z')
                if val_type == 'angle':
                    S[f'agent{a_id}_angle'] = soid.soidlib.types.float(f'agent{a_id}_angle')
                if val_type == 'forward_step':
                    S[f'agent{a_id}_forward_step'] = soid.soidlib.types.float(f'agent{a_id}_forward_step')
                if val_type == 'speed':
                    S[f'agent{a_id}_speed'] = soid.soidlib.types.float(f'agent{a_id}_speed')
                if val_type == 'signal_choice':
                    S[f'agent{a_id}_signal_choice'] = soid.soidlib.types.int_bv(f'agent{a_id}_signal_choice')
                if val_type == 'turn_choice':
                    S[f'agent{a_id}_turn_choice'] = soid.soidlib.types.int_bv(f'agent{a_id}_turn_choice')
                if val_type == 'lookahead':
                    S[f'agent{a_id}_lookahead'] = soid.soidlib.types.float(f'agent{a_id}_lookahead')
                if val_type == 'intersection_arrival':
                    S[f'agent{a_id}_intersection_arrival'] = soid.soidlib.types.int_bv(f'agent{a_id}_intersection_arrival')
                if val_type == 'initial_direction':
                    S[f'agent{a_id}_initial_direction'] = soid.soidlib.types.int_bv(f'agent{a_id}_initial_direction')
                if val_type == 'patience':
                    S[f'agent{a_id}_patience'] = soid.soidlib.types.int_bv(f'agent{a_id}_patience')
                if val_type == 'step_count':
                    S[f'agent{a_id}_step_count'] = soid.soidlib.types.int_bv(f'agent{a_id}_step_count')

        # declare behaviors
        D = {}
        D[f'will_proceed'] = soid.soidlib.types.bool_bv(f'will_proceed')

        return E,S, D

    # Register declare
    query.register(declare)

    def get_constraint(declare_type, tagged_cf):
        if tagged_cf['is_cf']:
            counterfactual = tagged_cf['cf']
            if counterfactual['is_value']:
                if counterfactual['is_pos_x']:
                    return soid.soidlib.Equal( declare_type[f"agent{tagged_cf['id']}_pos_x"], float(counterfactual['value']))
                if counterfactual['is_pos_z']:
                    return soid.soidlib.Equal( declare_type[f"agent{tagged_cf['id']}_pos_z"], float(counterfactual['value']))
                if counterfactual['is_angle']:
                    return soid.soidlib.Equal( declare_type[f"agent{tagged_cf['id']}_angle"], float(counterfactual['value']))
                if counterfactual['is_speed']:
                    return soid.soidlib.Equal( declare_type[f"agent{tagged_cf['id']}_speed"], float(counterfactual['value']))
                if counterfactual['is_forward_step']:
                    return soid.soidlib.Equal( declare_type[f"agent{tagged_cf['id']}_forward_step"], float(counterfactual['value']))
                if counterfactual['is_turnchoice']:
                    direction = counterfactual['value']
                    return soid.soidlib.Equal( declare_type[f"agent{tagged_cf['id']}_turn_choice"], int(get_dl_direction(direction)))
                if counterfactual['is_signalchoice']:
                    direction = counterfactual['value']
                    return soid.soidlib.Equal( declare_type[f"agent{tagged_cf['id']}_signal_choice"], int(get_dl_direction(direction)))
            if counterfactual['is_range']:
                low_bound = counterfactual['range']['low_bound']
                high_bound = counterfactual['range']['high_bound']
                turn_choices = counterfactual['range']['turn_choices']
                if counterfactual['is_pos_x']:
                    return  soid.soidlib.And(
                            soid.soidlib.FP_GTE(declare_type[f"agent{tagged_cf['id']}_pos_x"], float(low_bound)),
                            soid.soidlib.FP_LTE(declare_type[f"agent{tagged_cf['id']}_pos_x"], float(high_bound)))
                if counterfactual['is_pos_z']:
                    return  soid.soidlib.And(
                            soid.soidlib.FP_GTE(declare_type[f"agent{tagged_cf['id']}_pos_z"], float(low_bound)),
                            soid.soidlib.FP_LTE(declare_type[f"agent{tagged_cf['id']}_pos_z"], float(high_bound)))
                if counterfactual['is_angle']:
                    return  soid.soidlib.And(
                            soid.soidlib.FP_GTE(declare_type[f"agent{tagged_cf['id']}_angle"], float(low_bound)),
                            soid.soidlib.FP_LTE(declare_type[f"agent{tagged_cf['id']}_angle"], float(high_bound)))
                if counterfactual['is_speed']:
                    return  soid.soidlib.And(
                            soid.soidlib.FP_GTE(declare_type[f"agent{tagged_cf['id']}_speed"], float(low_bound)),
                            soid.soidlib.FP_LTE(declare_type[f"agent{tagged_cf['id']}_speed"], float(high_bound)))
                if counterfactual['is_forward_step']:
                    return  soid.soidlib.And(
                            soid.soidlib.FP_GTE(declare_type[f"agent{tagged_cf['id']}_forward_step"], float(low_bound)),
                            soid.soidlib.FP_LTE(declare_type[f"agent{tagged_cf['id']}_forward_step"], float(high_bound)))
                if counterfactual['is_turnchoice']:
                    direction_formula = False
                    for direction in turn_choices:
                        if not direction_formula:
                            direction_formula = soid.soidlib.Equal(declare_type[f"agent{tagged_cf['id']}_turn_choice"], int(get_dl_direction(direction)))
                            continue
                        direction_formula = soid.soidlib.Or (
                            soid.soidlib.Equal(declare_type[f"agent{tagged_cf['id']}_turn_choice"], int(get_dl_direction(direction))),
                            direction_formula
                        )
                    return direction_formula
                if counterfactual['is_signalchoice']:
                    direction_formula = None
                    for direction in turn_choices:
                        if not direction_formula:
                            direction_formula = soid.soidlib.Equal(declare_type[f"agent{tagged_cf['id']}_signal_choice"], int(get_dl_direction(direction)))
                            continue
                        direction_formula = soid.soidlib.Or (
                            soid.soidlib.Equal(declare_type[f"agent{tagged_cf['id']}_signal_choice"], int(get_dl_direction(direction))),
                            direction_formula
                        )
                    return direction_formula
        if tagged_cf['is_val']:
            value = tagged_cf['val']
            val_type = tagged_cf['val_type']
            if val_type == 'pos_x':
                return soid.soidlib.Equal(declare_type[f"agent{tagged_cf['id']}_pos_x"], float(value))
            if val_type == 'pos_z':
                return soid.soidlib.Equal(declare_type[f"agent{tagged_cf['id']}_pos_z"], float(value))
            if val_type == 'angle':
                return soid.soidlib.Equal(declare_type[f"agent{tagged_cf['id']}_angle"], float(value))
            if val_type == 'forward_step':
                return soid.soidlib.Equal(declare_type[f"agent{tagged_cf['id']}_forward_step"], float(value))
            if val_type == 'speed':
                return soid.soidlib.Equal(declare_type[f"agent{tagged_cf['id']}_speed"], float(value))
            if val_type == 'turn_choice':
                return soid.soidlib.Equal(declare_type[f"agent{tagged_cf['id']}_turn_choice"], int(get_dl_direction(value)))
            if val_type == 'signal_choice':
                return soid.soidlib.Equal(declare_type[f"agent{tagged_cf['id']}_signal_choice"], int(get_dl_direction(value)))
            if val_type == 'lookahead':
                return soid.soidlib.Equal(declare_type[f"agent{tagged_cf['id']}_lookahead"], float(value))
            if val_type == 'intersection_arrival':
                return soid.soidlib.Equal(declare_type[f"agent{tagged_cf['id']}_intersection_arrival"], int(value))
            if val_type == 'initial_direction':
                return soid.soidlib.Equal(declare_type[f"agent{tagged_cf['id']}_initial_direction"], int(value))
            if val_type == 'patience':
                return soid.soidlib.Equal(declare_type[f"agent{tagged_cf['id']}_patience"], int(value))
            if val_type == 'step_count':
                return soid.soidlib.Equal(declare_type[f"agent{tagged_cf['id']}_step_count"], int(value))

    def get_sub_formula(declare_type, tagged_cf_list):
        sub_formula = None
        for tagged_cf in tagged_cf_list:
            if sub_formula == None:
                sub_formula = get_constraint(declare_type, tagged_cf)
                continue
            sub_formula = soid.soidlib.Or (
                get_constraint(declare_type, tagged_cf),
                sub_formula)
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
                        raise Exception("Invalid information in soid query during encoding.")
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

            if sub_formula == None:
                continue
            else:
                formula = soid.soidlib.And (
                    sub_formula,
                    formula)

        #print("formula:", formula)
        return formula

    def environmental( E ):
        return encode(E, t_environment)
    query.environmental(environmental)

    def state( S ):
        return encode(S, t_state)
    query.state(state)

    def behavior(E, S, P ):
        if query_blob['query']['behavior'] == 'move':
            return soid.soidlib.Equal(P.will_proceed, True) # This will tell us if we ever move
        elif query_blob['query']['behavior'] == 'stop':
            return soid.soidlib.Equal(P.will_proceed, False) # This will tell us if we ever move
    query.behavior(behavior)

    return query

def process(query_blob, models):
    num_agents = int(query_blob['environment']['num_agents'])

    model = [ {} for i in range(num_agents) ]
    raw  = models[ 'raw' ] # todo: fix pp in soid so that can use that nicer interface

    if not models:
        return model

    nflt = [ 'pos_x', 'pos_z', 'speed', 'angle', 'forward_step' ]
    ndir = [ 'signal_choice', 'turn_choice' ]
    dir_arr = [ 'straight', 'left', 'right' ]

    for key in raw:
        try:
            agent, var = str(key).split('_', 1)
            assert(agent[:5] == 'agent')
        except:
            continue

        agent_id = int(agent[5:])
        if var in nflt:
            model[agent_id][var] = '{:.3f}'.format(eval(str(raw[key]))) # yep, we do what it takes
        if var in ndir:
            model[agent_id][var] = dir_arr[int(str(raw[key]))]

    return model


def invoke_soid(query_blob, env = None, out = None, serialize = None):
    oracle = soid.Oracle()
    klee_prefix = "src/webserver/soid_files/klee/"
    make = klee_prefix + 'makefile'

    query = generate_soid_query(query_blob)

    def query_type():
        if query_blob['query']['is_universal']:
            return 'move_universal' if query_blob['query']['behavior'] == 'move' else 'stop_universal'
        if query_blob['query']['is_existential']:
            return 'move_existential' if query_blob['query']['behavior'] == 'move' else 'stop_existential'

    query_start = {
        'kind' : 'soid_start',
        'query_info': {
            'querying'    : True,
            'query_start' : time.time(),
            'query_type'  : query_type(),
            'finished'    : False,
            'result'      : None,
            'model'       : None,
            'resources'   : None
        }
    }
    if env:
        env.query_info = query_start[ 'query_info' ]
    if out and serialize:
        serialize(query_start, out)

    # invoke soid
    (info, res, models, resources) = soid.invoke(oracle, make, query)

    model = models['raw']
    if serialize:
        model = process(query_blob, models)

    query_result = {
        'kind' : 'soid_finish',
        'query_info': {
            'querying'    : query_start['query_info']['querying'],
            'query_start' : query_start['query_info']['query_start'],
            'query_type'  : query_start['query_info']['query_type'],
            'finished'    : True,
            'result'      : res,
            'model'       : model,
            'resources'   : resources
        }
    }
    if env:
        env.query_info = query_result[ 'query_info' ]
    if out and serialize:
        serialize(query_result, out)

    return info, res, models, resources


### for running benchmarks

if __name__ == '__main__':
    if os.path.isabs(sys.argv[1]):
        query_blob = json.load(open(sys.argv[1]))
    else:
        query_prefix = 'src/webserver/soid_files/query_blobs/experiments/'
        query_blob = json.load(open(query_prefix + sys.argv[1]))

    print(f"Soid Results:")
    info, res, models, resources = invoke_soid(query_blob)

    print(f"Result: {res} Resources: {resources}")
    model_prefix = "src/webserver/soid_files/klee/models/"
    if models:
	if not os.path.exists(model_prefix):
            os.makedirs(model_prefix)
	print(f"Model in {model_prefix}")
	model_file = open((model_prefix + "model.out"), 'w', encoding="utf-8")
	model_file.write(f"{models['raw']}")
	model_file.close()
