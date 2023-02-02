import soid 
from soid.soidlib import *
import json
# Generate the soid query
def generate_soid_query(query_info):
    """
    generate the soid query

    """

    oracle = soid.Oracle()
    klee_prefix = "src/webserver/soid_files/klee/"
    make = klee_prefix + 'makefile'

    query = soid.soidlib.Soid('GUI Query', soid.soidlib.counterfactual.single) # counterfactual.single for 'exists queries' : counterfactual.verification for 'for all queries'


    q_environment = query_blob['environment']
    agents = query_blob['agents']

    # Sort out the variables
    t_environment = []
    t_state = []

    # For each of the agents, lets preprocess for easier lambda stuff later
    for i in range(int(q_environment['num_agents'])):
        
        
        # If we are on the first agent, who is the agent who's perspective matters
        agent = agents[f'agent{i}']
        print(agent)
        if i == 0:
            # Go through all of the counterfactuals

            for counterfactual in agent['symbolic']:
                tagged_cf = {
                    'id': agent['concrete']['id'],
                    'is_cf': True,
                    'cf': counterfactual,
                    'is_val': False,
                    'val_type': '',
                    'val': None,
                }

                # Environmental counterfactuals
                if counterfactual['is_pos_x']:
                    t_environment.append(tagged_cf)
                if counterfactual['is_pos_z']:
                    t_environment.append(tagged_cf)
                if counterfactual['is_angle']:
                    t_environment.append(tagged_cf)
                if counterfactual['is_speed']:
                    t_environment.apppend(tagged_cf)

                # State counterfactuals
                if counterfactual['is_forward_step']:
                    t_state.append(tagged_cf)
                if counterfactual['is_turnchoice']:
                    t_state.append(tagged_cf)
                if counterfactual['is_signalchoice']:
                    t_state.append(tagged_cf)
            
            # Add agent0's lookahead, initial_direction, intersection_Arrival, patience, step count to STATE
            # lookahead
            t_state.append({
                'id': agent['concrete']['id'],
                'is_cf': False,
                'cf': None,
                'is_val': True,
                'val_type': 'lookahead',
                'val': agent['concrete']['lookahead'],
            })
            # inital_direction
            t_state.append({
                'id': agent['concrete']['id'],
                'is_cf': False,
                'cf': None,
                'is_val': True,
                'val_type': 'initial_direction',
                'val': agent['state']['initial_direction'],
            })
            # intersection_arrival
            t_state.append({
                'id': agent['concrete']['id'],
                'is_cf': False,
                'cf': None,
                'is_val': True,
                'val_type': 'intersection_arrival',
                'val': agent['state']['intersection_arrival'],
            })            
            # patience
            t_state.append({
                'id': agent['concrete']['id'],
                'is_cf': False,
                'cf': None,
                'is_val': True,
                'val_type': 'patience',
                'val': agent['state']['patience'],
            })            
            # step_count
            t_state.append({
                'id': agent['concrete']['id'],
                'is_cf': False,
                'cf': None,
                'is_val': True,
                'val_type': 'step_count',
                'val': agent['state']['step_count'],
            })            

        if i > 0:
            for counterfactual in agents[f'agent{i}']['symbolic']:
                # Each of their counterfactuals will be environment
                tagged_cf = {
                    'id': agents[f'agent{i}']['concrete']['id'],
                    'is_cf': True,
                    'cf': counterfactual,
                    'is_val': False,
                    'val_type': '',
                    'val': None,
                }
                t_environment.append(tagged_cf)
            # Add non=agent0's lookahead, initial_direction, intersection_Arrival, patience, step count to ENVIORNMENT
            # lookahead
            t_environment.append({
                'id': agent['concrete']['id'],
                'is_cf': False,
                'cf': None,
                'is_val': True,
                'val_type': 'lookahead',
                'val': agent['concrete']['lookahead'],
            })
            # inital_direction
            t_environment.append({
                'id': agent['concrete']['id'],
                'is_cf': False,
                'cf': None,
                'is_val': True,
                'val_type': 'initial_direction',
                'val': agent['state']['initial_direction'],
            })
            # intersection_arrival
            t_environment.append({
                'id': agent['concrete']['id'],
                'is_cf': False,
                'cf': None,
                'is_val': True,
                'val_type': 'intersection_arrival',
                'val': agent['state']['intersection_arrival'],
            })            
            # patience
            t_environment.append({
                'id': agent['concrete']['id'],
                'is_cf': False,
                'cf': None,
                'is_val': True,
                'val_type': 'patience',
                'val': agent['state']['patience'],
            })            
            # step_count
            t_environment.append({
                'id': agent['concrete']['id'],
                'is_cf': False,
                'cf': None,
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
                    E[f'agent{a_id}_turn_choice'] = soid.soidlib.types.int(f'agent{a_id}_turn_choice', pp=None, raw=None)
                if counterfactual['is_signalchoice']:
                    E[f'agent{a_id}_signal_choice'] = soid.soidlib.types.int(f'agent{a_id}_signal_choice', pp=None, raw=None)
            elif tagged_cf['is_val']:
                val_type = tagged_cf['val_type']
                if val_type == 'lookahead':
                    E[f'agent{a_id}_lookahead'] = soid.soidlib.types.float(f'agent{a_id}_lookahead', pp=None, raw=None)
                if val_type == 'intersection_arrival':
                    E[f'agent{a_id}_intersection_arrival'] = soid.soidlib.types.int(f'agent{a_id}_intersection_arrival', pp=None, raw=None)
                if val_type == 'initial_direction':
                    E[f'agent{a_id}_initial_direction'] = soid.soidlib.types.int(f'agent{a_id}_initial_direction', pp=None, raw=None)
                if val_type == 'patience':
                    E[f'agent{a_id}_patience'] = soid.soidlib.types.int(f'agent{a_id}_patience', pp=None, raw=None)
                if val_type == 'step_count':
                    E[f'agent{a_id}_step_count'] = soid.soidlib.types.int(f'agent{a_id}_step_count', pp=None, raw=None)
        
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
                    S[f'agent{a_id}_turn_choice'] = soid.soidlib.types.int(f'agent{a_id}_turn_choice', pp=None, raw=None)
                if counterfactual['is_signalchoice']:
                    S[f'agent{a_id}_signal_choice'] = soid.soidlib.types.int(f'agent{a_id}_signal_choice', pp=None, raw=None)
            elif tagged_cf['is_val']:
                val_type = tagged_cf['val_type']
                if val_type == 'lookahead':
                    S[f'agent{a_id}_lookahead'] = soid.soidlib.types.float(f'agent{a_id}_lookahead', pp=None, raw=None)
                if val_type == 'intersection_arrival':
                    S[f'agent{a_id}_intersection_arrival'] = soid.soidlib.types.int(f'agent{a_id}_intersection_arrival', pp=None, raw=None)
                if val_type == 'initial_direction':
                    S[f'agent{a_id}_initial_direction'] = soid.soidlib.types.int(f'agent{a_id}_initial_direction', pp=None, raw=None)
                if val_type == 'patience':
                    S[f'agent{a_id}_patience'] = soid.soidlib.types.int(f'agent{a_id}_patience', pp=None, raw=None)
                if val_type == 'step_count':
                    S[f'agent{a_id}_step_count'] = soid.soidlib.types.int(f'agent{a_id}_step_count', pp=None, raw=None)
        
        # declare behaviors
        D = {}
        D[f'will_proceed'] = soid.soidlib.types.bool(f'will_proceed', pp=None, raw=None)
        
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

    def encode(declare_type, tagged_cf_list):
        formula = None
        for tagged_cf in tagged_cf_list:
            constraint = get_constraint(declare_type, tagged_cf)
            #print(f" Constraint {constraint}")
            #print(f" Constraint.sort {constraint.sort()}")
            if formula == None:
                formula = constraint
                continue

            formula = And (
                get_constraint(declare_type, tagged_cf),
                formula)
            print(f" Formula {formula.sort()}")
            
        print(formula)
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
    # Ignore info
    # Res is the result
    # Models is empty or models[0] is the model
    # resources is the timing of the query
    return res, models, resources


if __name__ == '__main__':
    query_blob = json.load(open('src/webserver/soid_files/query_blobs/query_blob'))
    print(query_blob)
    result, models, resources = generate_soid_query(query_blob)