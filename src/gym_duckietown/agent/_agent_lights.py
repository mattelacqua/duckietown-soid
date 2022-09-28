import random
#--------------------------
# Lights
#--------------------------

# Turn on Specific Light
def turn_on_light(self, light):
    self.lights[light][3] = True

# Turn off Specific Light
def turn_off_light(self, light):
    self.lights[light][3] = False

# Set light
def set_light(self, light, on):
    if on:
        self.lights[light][3] = True
    else:
        self.lights[light][3] = False

# Lights to Dict
def lights_to_dictlist(self):
    light_list = []
    for light in self.lights.items():
        light_list.append({"light": light[0], "on":self.lights[light[0]][3]})
    return light_list

# Signal for a turn
def signal_for_turn(self, turn):
    choices = ['Right', 'Left', 'Straight'] 
    if not turn:
        turn = random.choice(choices)

    if turn == "Right":
        self.turn_on_light("front_right")
        self.turn_on_light("back_right")
        self.turn_off_light("front_left")
        self.turn_off_light("back_left")
        self.turn_off_light("center")
    elif turn == "Left":
        self.turn_off_light("front_right")
        self.turn_off_light("back_right")
        self.turn_on_light("front_left")
        self.turn_on_light("back_left")
        self.turn_off_light("center")
    elif turn == "Straight":
        self.turn_off_light("front_right")
        self.turn_off_light("back_right")
        self.turn_off_light("front_left")
        self.turn_off_light("back_left")
        self.turn_off_light("center")
