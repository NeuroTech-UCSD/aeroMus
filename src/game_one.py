from psychopy import visual, event,core
from psychopy.hardware import keyboard

# Set up the window
win = visual.Window(size=(600, 500), fullscr=False, allowGUI=True)

# Set up the square and square
square = visual.Rect(win, width=0.15, height=0.15, fillColor='yellow')
circle = visual.Circle(win, radius=0.05, fillColor='blue',pos=(0,0))
cvalue =1
# Start the mouse
mouse = event.Mouse(win=win)
kb = keyboard.Keyboard() #declare keyboard

# Main loop
while True:
    # Check for quit event
    if 'escape' in event.getKeys():
        break

    # Get the current mouse position
    mouse_pos = mouse.getPos()

    # Move the square to the mouse position
    square.pos = mouse_pos

    # Check for mouse button events
    mouse_events = mouse.getPressed()
    if mouse_events[0]:  # Left mouse button is pressed
        square.fillColor = 'white'
    elif mouse_events[2] and cvalue == 1:
        circle.fillColor = 'blue'
        cvalue = 2
        mouse.clickReset()
    elif mouse_events[2] and cvalue == 2:
        circle.fillColor = 'red'
        cvalue = 1
        mouse.clickReset()
    else:
        square.fillColor = 'yellow'
        
    
    # Check for arrow key events
    keys = kb.getKeys(['a','d','w','s'], waitRelease=False)
    if 'a' in keys:
        circle.pos -= [.1, 0]
    elif 'd' in keys:
        circle.pos += [.1, 0]
    elif 'w' in keys:
        circle.pos += [0, .1]
    elif 's' in keys:
        circle.pos -= [0, .1]
    
 
    circle.draw()  
# Draw the square
    square.draw()
    cvText = visual.TextStim(win, text= str(cvalue), pos=circle.pos, color='white', height = 0.05)
    cvText.draw()
    win.flip()
    core.wait(0.01)

# Close the window
win.close()