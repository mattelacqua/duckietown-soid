# Generate the soid query
def generate_soid_query(query_info):
    return None
    """
    generate the soid query


    """
    import soid 
    from soid.soidlib import *

    oracle = soid.Oracle()
    klee_prefix = "src/webserver/soid_files/klee/"
    make = klee_prefix + 'makefile'

    query = soid.Soid('GUI Query', counterfactual.single) # counterfactual.single for 'exists queries' : counterfactual.verification for 'for all queries'

    """
    See the declare in https://gitlab.com/rose-yale/soid/-/blob/main/examples/car/queries/car.py for how this works.
    Essentially this is what links soid -> the klee file. We are declaring only what we say is symbolic

    E = {} is for environmental Variables
    S = {} is for the states (so these are all of the symbolic variables we used for klee)
    D(is P in example, but its old) = {} Is for the variable we want to test at the end result (which if you look at Klee.c is going to be our proceed_ret value.)

    an outline of the declaration line is:
        E[<Name we want to use in soid>] = soidlib.types.<***type (see below)***>(f'<name of variable in soid>', pp = None, raw = None)
        
        ***Sam is adding support for floats and doubles now, so put a placemarker variable like 

        For pp and raw, pp we can ignore for now ( i think, set to none on all) and then raw = variable name in klee). You can leave the raw = None and pp = None and it will search for whatever name comes after the soidlib.types.
    """

    @soid.register
    def declare():
        E = {"""Declare the environmental symbolic things, not really sure what from ours will go in because alot is static."""}
        S = {"""This will include agent things"""}
        P = {"""This will just have the proceed_ret value"""}

        """
        Hints for E and S
        For each agent the possible symbolic variables are:
            pos_x, pos_z
            angle
            speed
            forward_step
            turn_choice
            signal_choice
        
        This is done from the perspective of Agent0. So, its state would consist of things it has control over at the moment (if you were driving)
            forward_step (acceleration)
            turn_choice
            signal_choice
        
        The environment would be 
            Agent0's pos_x, posz
            Agent0's angle
            Agent0's speed
            For every other agent:
                pos_x, pos_z
                angle
                speed
                forward_step
                turn_choice
                signal_choice

        *** Note that these might not exist, e.g. if we don't have any counterfactuals / symbolic values for any other agents, then environment will be much smaller.

        *** You may want to preprocess into a dataformat that makes sense to you. It could be having lists that point to the info in the json blob to keep track of:
            e.g. environment_blob_info = []
                    environment_blob_info.append(<counterfactual for agent0 posx, posz, angle, speed>)
                    for every agent that isnt agent 0
                        environment_blob_info.extend(<all counterfactuals for agent>)
            this will be useful so you have fast access when you are doing the constraint adding below.
        """
        agents = None

    """
    Now we have to register the actual constraints now that the variables are linked. See https://gitlab.com/rose-yale/soid/-/blob/main/examples/car/queries/causal_signaling.py. We just build the constraints. List of available keywords to us (Like And, Equal, etc are: https://gitlab.com/rose-yale/soid/-/blob/main/soid/soidlib/soidlib.py line 264. Getting Sam to add Or, LT, LTE, GT, GTE) You can use filler names for now.

    """
    @soid.register
    def environmental( E ):
        """Here you will have to have something that generates this structure, like looping through the possible constraints that use variables E that we defined above. You may want something like this function to help:

            def encode( E, config ):
                formula = None
                for thing in config:
                    formula = And(Equal(E[ thing[0] ], thing[1]), formula)
                return formula
            
            Treat config like a list of the variables in E and the constraints that come with them. You can do something similar in the following two as well.
        """

    @soid.register
    def state( S ):
        """
        Here you will have to have something that generates this structure, like looping through the possible constraints that use variables S that we defined above
        """

    @soid.register
    def behavior(E, S, D ):
        """
        Here you will have to have something that generates this structure, like looping through the possible constraints that use variables D that we defined above
        """
        return Equal(D.will_proceed, True) # This will tell us if we ever move

    
    # invoke soid
    (info, res, models, resources ) = soid.invoke(oracle, make, query)
    # Ignore info
    # Res is the result
    # Models is empty or models[0] is the model
    # resources is the timing of the query
    return res, models, resources

