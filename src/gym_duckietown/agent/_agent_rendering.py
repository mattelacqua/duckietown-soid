from .. import logger
from ..agents import dl
from ..dl_utils import *

#--------------------------
# Rendering  / Stepping
#--------------------------
# Render the step and call the inner return
def render_step(self, env, action, learning=False):
    state, reward, done, info = env.step(action, self, learning)
    if env.verbose:
        logger.info(self.agent_id +": step_count = %s, reward=%.3f" % (self.step_count, reward))
    if learning:
        return state, reward, done, info
    else:
        return self.render_step_inner(env, done)


# Render if possible, otherwise end if invalid
def render_step_inner(self, env, done):
    # if hit obstacle, return and stop
    # otherwise, keep going and render in the proper cam mode
    if done:
        logger.error(self.agent_id + ": Failed. Check Log")
        env.reset()
        return False
    else:
        return True

# Check if we are in the middle of completing an action
def completing_action(self):
    # Preprocess for C
    dl.completing_action.argtypes = [c_int]
    if self.actions:
        # Preprocess for C
        action = self.actions[0][1]
        return dl.completing_action(action)

    else:
        return dl.completing_action(Action.NO_ACTION)

# Get next action
def get_next_action(self):
    return self.actions.pop(0)

# Get next action
def add_actions(self, actions):
    return self.actions.extend(actions)