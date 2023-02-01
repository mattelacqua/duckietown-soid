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

    query = Soid('GUI Query', counterfactual.single) # counterfactual.single for 'exists queries' : counterfactual.verification for 'for all queries'


    environment = query_blob['environment']
    agents = query_blob['agents']

    # Sort out the variables
    environment = []
    state = []

    # For each of the agents, lets preprocess for easier lambda stuff later
    for i in range(environment['num_agents']):
        
        
        # If we are on the first agent, who is the agent who's perspective matters
        agent = agents[f'agent{i}']
        if i == 0:
            # Go through all of the counterfactuals

            for counterfactual in agent['counterfactuals']:
                tagged_cf = {
                    'id': agent['id'],
                    'is_cf': True,
                    'cf': counterfactual,
                    'is_val': False,
                    'val_type': '',
                    'val': None,
                }

                # Environmental counterfactuals
                if counterfactual['is_pos_x']:
                    environment.apppend(tagged_cf)
                if counterfactual['is_pos_z']:
                    environment.apppend(tagged_cf)
                if counterfactual['is_angle']:
                    environment.apppend(tagged_cf)
                if counterfactual['is_speed']:
                    environment.apppend(tagged_cf)

                # State counterfactuals
                if counterfactual['is_forward_step']:
                    state.apppend(tagged_cf)
                if counterfactual['is_turnchoice']:
                    state.apppend(tagged_cf)
                if counterfactual['is_signalchoice']:
                    state.apppend(tagged_cf)
            
            # Add agent0's lookahead, initial_direction, intersection_Arrival, patience, step count to STATE
            # lookahead
            state.append({
                'id': agent['id'],
                'is_cf': False,
                'cf': None,
                'is_val': True,
                'val_type': 'lookahead',
                'val': agent['concrete']['lookahead'],
            })
            # inital_direction
            state.append({
                'id': agent['id'],
                'is_cf': False,
                'cf': None,
                'is_val': True,
                'val_type': 'initial_direction',
                'val': agent['state']['initial_direction'],
            })
            # intersection_arrival
            state.append({
                'id': agent['id'],
                'is_cf': False,
                'cf': None,
                'is_val': True,
                'val_type': 'intersection_arrival',
                'val': agent['state']['intersection_arrival'],
            })            
            # patience
            state.append({
                'id': agent['id'],
                'is_cf': False,
                'cf': None,
                'is_val': True,
                'val_type': 'patience',
                'val': agent['state']['patience'],
            })            
            # step_count
            state.append({
                'id': agent['id'],
                'is_cf': False,
                'cf': None,
                'is_val': True,
                'val_type': 'step_count',
                'val': agent['state']['step_count'],
            })            

        if i > 0:
            for counterfactual in agents[f'agent{i}']['counterfactuals']:
                # Each of their counterfactuals will be environment
                tagged_cf = {
                    'id': agents[f'agent{i}']['id'],
                    'cf': counterfactual,
                }
                environment.apppend(tagged_cf)
            # Add non=agent0's lookahead, initial_direction, intersection_Arrival, patience, step count to ENVIORNMENT
            # lookahead
            environment.append({
                'id': agent['id'],
                'is_cf': False,
                'cf': None,
                'is_val': True,
                'val_type': 'lookahead',
                'val': agent['concrete']['lookahead'],
            })
            # inital_direction
            environment.append({
                'id': agent['id'],
                'is_cf': False,
                'cf': None,
                'is_val': True,
                'val_type': 'initial_direction',
                'val': agent['state']['initial_direction'],
            })
            # intersection_arrival
            environment.append({
                'id': agent['id'],
                'is_cf': False,
                'cf': None,
                'is_val': True,
                'val_type': 'intersection_arrival',
                'val': agent['state']['intersection_arrival'],
            })            
            # patience
            environment.append({
                'id': agent['id'],
                'is_cf': False,
                'cf': None,
                'is_val': True,
                'val_type': 'patience',
                'val': agent['state']['patience'],
            })            
            # step_count
            environment.append({
                'id': agent['id'],
                'is_cf': False,
                'cf': None,
                'is_val': True,
                'val_type': 'step_count',
                'val': agent['state']['step_count'],
            })

    @soid.register
    def declare():

        # declare Environment
        E = {}
        for tagged_cf in environment:
            a_id = int(tagged_cf['id'])
            if tagged_cf['is_cf']:
                counterfactual = tagged_cf['counterfactual']
                if counterfactual['is_pos_x']:
                    E[f'agent{a_id}.pos_x'] = soidlib.types.float(f'agent{a_id}.pos_x', pp=None, raw=None)
                if counterfactual['is_pos_z']:
                    E[f'agent{a_id}.pos_z'] = soidlib.types.float(f'agent{a_id}.pos_z', pp=None, raw=None)
                if counterfactual['is_angle']:
                    E[f'agent{a_id}.angle'] = soidlib.types.float(f'agent{a_id}.angle', pp=None, raw=None)
                if counterfactual['is_forward_step']:
                    E[f'agent{a_id}.forward_step'] = soidlib.types.float(f'agent{a_id}.forward_step', pp=None, raw=None)
                if counterfactual['is_speed']:
                    E[f'agent{a_id}.speed'] = soidlib.types.float(f'agent{a_id}.speed', pp=None, raw=None)
                if counterfactual['is_turnchoice']:
                    E[f'agent{a_id}.turn_choice'] = soidlib.types.int(f'agent{a_id}.turn_choice', pp=None, raw=None)
                if counterfactual['is_signalchoice']:
                    E[f'agent{a_id}.signal_choice'] = soidlib.types.int(f'agent{a_id}.signal_choice', pp=None, raw=None)
            elif tagged_cf['is_val']:
                if val_type == 'lookahead':
                    E[f'agent{a_id}.lookahead'] = soidlib.types.float(f'agent{a_id}.lookahead', pp=None, raw=None)
                if val_type == 'intersection_arrival':
                    E[f'agent{a_id}.intersection_arrival'] = soidlib.types.int(f'agent{a_id}.intersection_arrival', pp=None, raw=None)
                if val_type == 'initial_direction':
                    E[f'agent{a_id}.initial_direction'] = soidlib.types.int(f'agent{a_id}.initial_direction', pp=None, raw=None)
                if val_type == 'patience':
                    E[f'agent{a_id}.patience'] = soidlib.types.int(f'agent{a_id}.patience', pp=None, raw=None)
                if val_type == 'step_count':
                    E[f'agent{a_id}.step_count'] = soidlib.types.int(f'agent{a_id}.step_count', pp=None, raw=None)
        
        # declare state
        S = {}
        for tagged_cf in state:
            a_id = int(tagged_cf['id'])
            if tagged_cf['is_cf']:
                counterfactual = tagged_cf['counterfactual']
                if counterfactual['is_pos_x']:
                    S[f'agent{a_id}.pos_x'] = soidlib.types.float(f'agent{a_id}.pos_x', pp=None, raw=None)
                if counterfactual['is_pos_z']:
                    S[f'agent{a_id}.pos_z'] = soidlib.types.float(f'agent{a_id}.pos_z', pp=None, raw=None)
                if counterfactual['is_angle']:
                    S[f'agent{a_id}.angle'] = soidlib.types.float(f'agent{a_id}.angle', pp=None, raw=None)
                if counterfactual['is_forward_step']:
                    S[f'agent{a_id}.forward_step'] = soidlib.types.float(f'agent{a_id}.forward_step', pp=None, raw=None)
                if counterfactual['is_speed']:
                    S[f'agent{a_id}.speed'] = soidlib.types.float(f'agent{a_id}.speed', pp=None, raw=None)
                if counterfactual['is_turnchoice']:
                    S[f'agent{a_id}.turn_choice'] = soidlib.types.int(f'agent{a_id}.turn_choice', pp=None, raw=None)
                if counterfactual['is_signalchoice']:
                    S[f'agent{a_id}.signal_choice'] = soidlib.types.int(f'agent{a_id}.signal_choice', pp=None, raw=None)
            elif tagged_cf['is_val']:
                if val_type == 'lookahead':
                    S[f'agent{a_id}.lookahead'] = soidlib.types.float(f'agent{a_id}.lookahead', pp=None, raw=None)
                if val_type == 'intersection_arrival':
                    S[f'agent{a_id}.intersection_arrival'] = soidlib.types.int(f'agent{a_id}.intersection_arrival', pp=None, raw=None)
                if val_type == 'initial_direction':
                    S[f'agent{a_id}.initial_direction'] = soidlib.types.int(f'agent{a_id}.initial_direction', pp=None, raw=None)
                if val_type == 'patience':
                    S[f'agent{a_id}.patience'] = soidlib.types.int(f'agent{a_id}.patience', pp=None, raw=None)
                if val_type == 'step_count':
                    S[f'agent{a_id}.step_count'] = soidlib.types.int(f'agent{a_id}.step_count', pp=None, raw=None)
        
        # declare behaviors
        D = {}
        D[f'will_proceed'] = soidlib.types.bool(f'will_proceed', pp=None, raw=None)

    def get_constraint(declare_type, tagged_cf):
        if tagged_cf['is_cf']:
            counterfactual = tagged_cf['counterfactual']
            if counterfactual['is_value']:
                if counterfactual['is_pos_x']:
                    return Equal( declare_type[f"agent{tagged_cf['id']}.pos_x"], counterfactual['value'])
                if counterfactual['is_pos_z']:
                    return Equal( declare_type[f"agent{tagged_cf['id']}.pos_z"], counterfactual['value'])
                if counterfactual['is_angle']:
                    return Equal( declare_type[f"agent{tagged_cf['id']}.angle"], counterfactual['value'])
                if counterfactual['is_speed']:
                    return Equal( declare_type[f"agent{tagged_cf['id']}.speed"], counterfactual['value'])
                if counterfactual['is_forward_step']:
                    return Equal( declare_type[f"agent{tagged_cf['id']}.forward_step"], counterfactual['value'])
                if counterfactual['is_turnchoice']:
                    return Equal( declare_type[f"agent{tagged_cf['id']}.turn_choice"], counterfactual['value'])
                if counterfactual['is_signalchoice']:
                    return Equal( declare_type[f"agent{tagged_cf['id']}.signal_choice"], counterfactual['value'])
            if counterfactual['is_range']:
                low_bound = counterfactual['range']['low_bound']
                high_bound = counterfactual['range']['high_bound']
                turn_choices = counterfactual['range']['turn_choices']
                if counterfactual['is_pos_x']:
                    return  And( 
                            FP_GTE(declare_type[f"agent{tagged_cf['id']}.pos_x"], low_bound),
                            FP_LTE(declare_type[f"agent{tagged_cf['id']}.pos_x"], high_bound))
                if counterfactual['is_pos_z']:
                    return  And( 
                            FP_GTE(declare_type[f"agent{tagged_cf['id']}.pos_z"], low_bound),
                            FP_LTE(declare_type[f"agent{tagged_cf['id']}.pos_z"], high_bound))
                if counterfactual['is_angle']:
                    return  And( 
                            FP_GTE(declare_type[f"agent{tagged_cf['id']}.angle"], low_bound),
                            FP_LTE(declare_type[f"agent{tagged_cf['id']}.angle"], high_bound))
                if counterfactual['is_speed']:
                    return  And( 
                            FP_GTE(declare_type[f"agent{tagged_cf['id']}.speed"], low_bound),
                            FP_LTE(declare_type[f"agent{tagged_cf['id']}.speed"], high_bound))
                if counterfactual['is_forward_step']:
                    return  And( 
                            FP_GTE(declare_type[f"agent{tagged_cf['id']}.forward_step"], low_bound),
                            FP_LTE(declare_type[f"agent{tagged_cf['id']}.forward_step"], high_bound))
                if counterfactual['is_turnchoice']:
                    direction_formula = False
                    for direction in turn_choices:
                        direction_formula = Or (
                            Equal(declare_type[f"agent{tagged_cf['id']}.turn_choice"], direction),
                            direction_formula
                        )
                    return direction_formula
                if counterfactual['is_signalchoice']:
                    direction_formula = False
                    for direction in turn_choices:
                        direction_formula = Or (
                            Equal(declare_type[f"agent{tagged_cf['id']}.signal_choice"], direction),
                            direction_formula
                        )
                    return direction_formula
        if tagged_cf['is_val']:
            value = tagged_cf['val']
            if val_type == 'lookahead':
                return Equal(declare_type[f"agent{tagged_cf['id']}.lookahead"], value),
            if val_type == 'intersection_arrival':
                return Equal(declare_type[f"agent{tagged_cf['id']}.intersection_arrival"], value),
            if val_type == 'initial_direction':
                return Equal(declare_type[f"agent{tagged_cf['id']}.initial_direction"], value),
            if val_type == 'patience':
                return Equal(declare_type[f"agent{tagged_cf['id']}.patience"], value),
            if val_type == 'step_count':
                return Equal(declare_type[f"agent{tagged_cf['id']}.step_count"], value),

    def encode(declare_type, tagged_cf_list):
        formula = True
        for tagged_cf in tagged_cf_list:
            formula = And (
                get_constraint(declare_type, tagged_cf),
                formula)
        
        return formula

    @soid.register
    def environmental( E ):
        return encode(E, environment)

    @soid.register
    def state( S ):
        return encode(S, state)

    @soid.register
    def behavior(E, S, D ):
        return Equal(D.will_proceed, True) # This will tell us if we ever move

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