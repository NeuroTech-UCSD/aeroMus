from psychopy.hardware import keyboard
from psychopy import visual, event, core

# create the window, a circle object (cursorObject) which is controlled by the mouse,
# and a rectangle object (keysObject) which is controlled by the arrow keys.
win = visual.Window(size=(800, 600), fullscr=False)
cursorObject = visual.Circle(win, radius=0.1, fillColor='black')
cursorText = visual.TextStim(win, text="mouse", pos=cursorObject.pos, color='white', height = 0.05)
keysObject = visual.Rect(win, width = 0.1, height = 0.1, pos=(0,0), fillColor='yellow')
keysObjectText = visual.TextStim(win, text="cheese", pos=keysObject.pos, color='black', height = 0.04)
mouse = event.Mouse(win=win)
kb = keyboard.Keyboard()
currPressed = []

while True:
    # booleans which are set to true if certain key is pressed
    leftClick = False
    middleClick = False
    rightClick = False

    # reset the clock & get keyboard input. If escape is pressed, close the window
    kb.clock.reset()
    keys = kb.getKeys(waitRelease=False, clear=False)
    if 'escape' in keys:
        break
    currPressed = []
    mouse_pos = mouse.getPos()

    # Store key presses in list currPressed
    for key in keys:
        currPressed.append(key)

    # depending on key pressed, move (or set specific boolean to true) based on key pressed
    for key in currPressed:
        if not key.duration:
            if key == 'up' and (keysObject.pos[1] + 0.01 < 1):
                keysObject.pos += [0, 0.01] 
            elif key == 'down' and (keysObject.pos[1] - 0.01 > -1):
                keysObject.pos += [0, -0.01] 
            if key == 'left' and (keysObject.pos[0] -0.01 > -1):
                keysObject.pos += [-0.01, 0] 
            elif key == 'right' and (keysObject.pos[0] + 0.01 < 1):
                keysObject.pos += [0.01, 0]
            elif key == 'q':
                leftClick = True
            elif key == 'w':
                middleClick = True
            elif key == 'e':
                rightClick = True

    #clicking while on top of object or pressing a key (regardless of location) change color of cursorObject
    button = mouse.getPressed()
    if mouse.isPressedIn(cursorObject, buttons=[0]) or leftClick == True:
        cursorObject.fillColor = 'blue'
    elif middleClick == True or mouse.isPressedIn(keysObject, buttons=[1]):
            cursorObject.fillColor = 'green'
    elif mouse.isPressedIn(cursorObject, buttons=[2]) or rightClick == True:
        cursorObject.fillColor = 'red'        

    # updates the position of the objects and text
    keysObjectText.pos = keysObject.pos
    cursorObject.pos = mouse_pos
    cursorText.pos = mouse_pos

    # draws the objects and text
    keysObject.draw()
    keysObjectText.draw()
    cursorObject.draw()
    cursorText.draw()

    win.flip()
    core.wait(0.01)

win.close()