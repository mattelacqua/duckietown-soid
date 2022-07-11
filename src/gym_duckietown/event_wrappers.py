import webbrowser
import pyglet
import pyglet
from pyglet.window import key, mouse
 
# Handle Key Presses 
def on_key_press(symbol, modifiers, env):
    """
    This handler processes keyboard commands that
    control the simulation
    """
    if symbol == key.BACKSPACE or symbol == key.SLASH:
        env.reset()
        env.render()
    elif symbol == key.PAGEUP:
        env.unwrapped.cam_angle[0] = 0
    elif symbol == key.ESCAPE:
        env.close()
        sys.exit(0)


def on_mouse_press(x, y, button, modifiers, update, pause):
    """
    This handler processes keyboard commands that
    control the simulation
    """
    webbrowser.open('http://127.0.0.1:5000', new=1)
    pyglet.clock.unschedule(update)
    pyglet.clock.schedule_once(pause, 0.0)

    # Take a screenshot
    # UNCOMMENT IF NEEDED - Skimage dependency
    # elif symbol == key.RETURN:
    #     print('saving screenshot')
    #     img = env.render('rgb_array')
    #     save_img('screenshot.png', img)


