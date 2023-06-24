from psychopy.hardware import keyboard
from psychopy import visual, event, core

#create the window, and the cursor stimulus (circle). Makes the circle white, and puts 'mouse' on top of it in black text
win = visual.Window(size=(800, 600), fullscr=False, color='white')
cursorStim = visual.Circle(win, radius=0.05, fillColor='white')
cursorText = visual.TextStim(win, text="mouse", pos=cursorStim.pos, color='black', height = 0.03)

#create the cheese block, fill in color yellow. Has text "cheese" on top of it in black.
cheese = visual.Rect(win, width = 0.1, height = 0.1, pos=(0,0), fillColor='yellow')
cheeseText = visual.TextStim(win, text="cheese", pos=cheese.pos, color='black', height = 0.04)

#creates another rectangle. This is to reset if the cheese goes bad. The rectangle will be green and have "reset" on top of it
resetBlock = visual.Rect(win, width = 0.1, height = 0.1, pos=(0.5,-0.3), fillColor='green')
resetBlockTxt = visual.TextStim(win, text="reset", pos=resetBlock.pos, color='black', height = 0.03)

#the text that will display on the screen after cheese has been clicked
endText = visual.TextStim(win, text='', pos=cursorStim.pos + (.1,.1), color='black', height=0.05)

#creates mouse, keyboard, currPressed, and timer. Also badCheeseTim which is num of seconds before cheese goes bad
mouse = event.Mouse(win=win)
kb = keyboard.Keyboard()
currPressed = []
timer = core.Clock()
badCheeseTime = 5

#this function executes if cheese was middle clicked on. If cheese was good, it will do that stuff
#if the cheese was bad, you get a different result, including the mouse turning black & dying
#leftClick == True does not work. Place holder for figuring out way to make program act like the mouse was clicked
def checkClick(stim, endMessage):
    if leftClick == True or mouse.isPressedIn(stim, buttons=[1]) and timer.getTime() < badCheeseTime:
        endMessage.text = 'you ate the cheese'
        cheese.fillColor = 'white'
        cursorText.text = 'satisfied mouse'
        endMessage.draw()
        resetWin()
    elif leftClick == True or mouse.isPressedIn(stim, buttons=[1]) and timer.getTime() > badCheeseTime:
        endMessage.text = 'you ate the spoiled cheese & died'
        endMessage.draw()
        cursorStim.fillColor = 'black'
        cursorText.color = 'white'
        cursorText.text = 'Dead mouse'
        resetWin()

#this function is meant to reset the window
def resetWin():
    core.wait(0.5)
    cursorStim.fillColor = 'white'
    cursorText.text = 'mouse'
    cursorText.color = 'black'
    cheeseText.text = 'cheese'
    cheese.fillColor = 'yellow'
    win.flip()
    core.wait(1.5)
    timer.reset()


while True:
    #booleans to subsitute for click. Not really that helpful for the clickable stimulus part
    leftClick = False
    middleClick = False
    rightClick = False

    kb.clock.reset()

    #waitrealease is false and clear is false so we can make the action occur as long as we hold it down.
    #if escape is pressed, the sim will end. CurrPressed is also reset
    keys = kb.getKeys(waitRelease=False, clear=False)
    if 'escape' in keys:
        break
    currPressed = []
    mouse_pos = mouse.getPos()

    #this is to be able to go diagonally
    for key in keys:
        currPressed.append(key)

    #while the key is pressed, it will continue to change the position in the desired direction
    #once released, it will stop moving.
    #Also has my attempt at making something like a key press have the same affect as a click (need a better idea.)
    for key in currPressed:
        if not key.duration:
            if key == 'up' and (cheese.pos[1] + 0.01 < 1):
                cheese.pos += [0, 0.01] 
            elif key == 'down' and (cheese.pos[1] - 0.01 > -1):
                cheese.pos += [0, -0.01] 
            if key == 'left' and (cheese.pos[0] -0.01 > -1):
                cheese.pos += [-0.01, 0] 
            elif key == 'right' and (cheese.pos[0] + 0.01 < 1):
                cheese.pos += [0.01, 0] 
            if key == 'q':
                leftClick = True
            if key == 'w':
                middleClick = True
            if key == 'e':
                rightClick = True

    #checks if the mouse has been clicked. If it was left clicked, then fills blue.
    #if right clicked, it is red. Also makes change if q or e were pressed.
    button = mouse.getPressed()
    if mouse.isPressedIn(cursorStim, buttons=[0]) or leftClick == True:
        cursorStim.fillColor = 'blue'
    elif mouse.isPressedIn(cursorStim, buttons=[2]) or rightClick == True:
        cursorStim.fillColor = 'red'        

    #updates position of the text blocks, so they dont get lost behind the stim. Also
    #the position of the cursor to make sure it follows mouse
    cheeseText.pos = cheese.pos
    cursorStim.pos = mouse_pos
    cursorText.pos = mouse_pos

    #calls check click if cheese was middle clicked on
    checkClick(cheese, endText)
    #draws the stims at new positions
    cheese.draw()
    cheeseText.draw()
    cursorStim.draw()
    cursorText.draw()

    #if timer reaches badCheeseTime, the cheese becomes green and says "spoiled cheese"
    #the reset block is then drawn. If user left clicks on reset block, it will restart
    if(timer.getTime() >= badCheeseTime):
        cheese.fillColor = 'green'
        cheeseText.setText('spoiled cheese')
        resetBlock.draw()
        resetBlockTxt.draw()
        if leftClick == True or mouse.isPressedIn(resetBlock, buttons=[1]):
            resetWin()
    win.flip()
    core.wait(0.01)

win.close()