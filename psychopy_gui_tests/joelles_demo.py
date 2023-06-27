import pyautogui
import random
import time

bubbleX = 92
bubbleY = 34

chatX = 307
chatY = 70

trickX = 441
trickY = 82

pyautogui.moveTo(bubbleX, bubbleY)

# put in loop
for i in range(4):
    # create a variable that is randomly picked within 5 of variable bubbleX
    randBubbleX = random.randrange(bubbleX-3, bubbleX+3)
    randBubbleY = random.randrange(bubbleY-5, bubbleY+5)
    randTrickX = random.randrange(trickX-3, trickX+3)
    randTrickY = random.randrange(trickY-3, trickY+3)
    pyautogui.click(duration=0.5)
    # set random time between 0 and 1.5 seconds with normal distribution around 1
    timeOne = random.normalvariate(1.2, 0.5)
    timeTwo = random.normalvariate(1.2, 0.5)
    pyautogui.moveTo(chatX, chatY, duration=timeOne, tween=pyautogui.easeInOutQuad)
    pyautogui.moveTo(randTrickX, randTrickY, duration=timeTwo, tween=pyautogui.easeInOutQuad)
    pyautogui.click()
    # system rest 1 second 
    time.sleep(timeTwo)
    if random.random() < 0.5:
        pyautogui.moveTo(150, 167, duration=1, tween=pyautogui.easeInOutQuad)
    pyautogui.moveTo(randBubbleX, randBubbleY, duration=timeOne, tween=pyautogui.easeInOutQuad)

