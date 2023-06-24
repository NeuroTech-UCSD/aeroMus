from psychopy.hardware import keyboard
from psychopy import visual, event, core

win = visual.Window(size=(800, 600), fullscr=False)
circle = visual.Circle(win, radius=0.1, fillColor='black')
mouseText = visual.TextStim(win, text="mouse", pos=circle.pos, color='white', height = 0.05)
square = visual.Rect(win, width = 0.1, height = 0.1, pos=(0,0), fillColor='yellow')
cheeseText = visual.TextStim(win, text="cheese", pos=square.pos, color='black', height = 0.04)
mouse = event.Mouse(win=win)
kb = keyboard.Keyboard()

while True:
    kb.clock.reset()
    keys = kb.getKeys(['right', 'left', 'up', 'down', 'b','g', 'escape'], waitRelease=True)
    if 'escape' in keys:
        break

    mouse_pos = mouse.getPos()
    button = mouse.getPressed()
    if mouse.isPressedIn(circle, buttons=[0]):
        circle.fillColor = 'blue'
    elif mouse.isPressedIn(circle, buttons=[1]):
        circle.fillColor = 'green'
    elif mouse.isPressedIn(circle, buttons=[2]):
        circle.fillColor = 'red'

    for key in keys:
        if key == 'up':
            square.pos += [0, 0.01]  # Move up
        elif key == 'down':
            square.pos += [0, -0.01]  # Move down
        elif key == 'left':
            square.pos += [-0.01, 0]  # Move left
        elif key == 'right':
            square.pos += [0.01, 0]  # Move right
        elif key == 'b':
            square.fillColor = 'green'
        elif key == 'g':
            square.fillColor = 'yellow'

    cheeseText.pos = square.pos
    circle.pos = mouse_pos
    mouseText.pos = mouse_pos

    square.draw()
    cheeseText.draw()
    circle.draw()
    mouseText.draw()

    win.flip()
    core.wait(0.01)

win.close()
