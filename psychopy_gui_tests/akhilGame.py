from psychopy.hardware import keyboard
from psychopy import visual, event, core

win = visual.Window(size=(800, 600), fullscr=False)
circle = visual.Circle(win, radius=0.1, fillColor='mouse')
mouseText = visual.TextStim(win, text="mouse", pos=circle.pos, color='black', height = 0.05)
square = visual.Rect(win, width = 0.1, height = 0.1, pos=(0,0), fillColor='yellow')
cheeseText = visual.TextStim(win, text="cheese", pos=square.pos, color='black', height = 0.04)
mouse = event.Mouse(win=win)
kb = keyboard.Keyboard()
currPressed = []
timer = core.Clock()

def checkClick(stim, textStim):
    if mouse.isPressedIn(stim, buttons=[1]) and timer.getTime() < 10:
        square.fillColor = 'white'
        print("you ate the cheese")
    elif mouse.isPressedIn(stim, buttons=[1]) and timer.getTime() > 10:
        circle.fillColor = 'black'
        textStim.color = 'white'
        textStim.text = 'Dead mouse'
        print("you ate spoiled cheese & died")

while True:
    leftClick = False
    middleClick = False
    rightClick = False

    kb.clock.reset()
    keys = kb.getKeys(waitRelease=False, clear=False)
    if 'escape' in keys:
        break
    currPressed = []
    mouse_pos = mouse.getPos()

    for key in keys:
        currPressed.append(key)

    for key in currPressed:
        if not key.duration:
            if key == 'up' and (square.pos[1] + 0.01 < 1):
                square.pos += [0, 0.01] 
            elif key == 'down' and (square.pos[1] - 0.01 > -1):
                square.pos += [0, -0.01] 
            if key == 'left' and (square.pos[0] -0.01 > -1):
                square.pos += [-0.01, 0] 
            elif key == 'right' and (square.pos[0] + 0.01 < 1):
                square.pos += [0.01, 0] 
            if key == 'b':
                square.fillColor = 'green'
            if key == 'g':
                square.fillColor = 'yellow'
            if key == 'q':
                leftClick = True
            if key == 'w':
                middleClick = True
            if key == 'e':
                rightClick = True

    button = mouse.getPressed()
    if mouse.isPressedIn(circle, buttons=[0]) or leftClick == True:
        circle.fillColor = 'blue'
    elif mouse.isPressedIn(circle, buttons=[2]) or rightClick == True:
        circle.fillColor = 'red'        

    cheeseText.pos = square.pos
    circle.pos = mouse_pos
    mouseText.pos = mouse_pos

    checkClick(square, mouseText)
    square.draw()
    cheeseText.draw()
    circle.draw()
    mouseText.draw()

    if(timer.getTime() >= 10):
        square.fillColor = 'green'
        cheeseText.setText('spoiled cheese')

    win.flip()
    core.wait(0.01)

win.close()