import vgamepad as vg
import time

gamepad = None
#controllerParams
debounceTime = 0.02
minPressTime = 0.02


#buttons
a_button = vg.XUSB_BUTTON.XUSB_GAMEPAD_A
b_button = vg.XUSB_BUTTON.XUSB_GAMEPAD_B
y_button = vg.XUSB_BUTTON.XUSB_GAMEPAD_Y
lb_button = vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER
rb_button = vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER
dpad_left = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT
dpad_right = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT
dpad_down = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN
dpad_up = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP

gamepad = vg.VX360Gamepad()

#basic control functions
def pressKey(button,duration):
    global gamepad
    gamepad.press_button(button)
    gamepad.update()
    time.sleep(duration)
    gamepad.release_button(button)
    gamepad.update()

def lTrigger(value):# values between 0 and 255
    global gamepad
    gamepad.left_trigger(value=value)
    gamepad.update()
    
def rTrigger(value):# values between 0 and 255
    global gamepad
    gamepad.right_trigger(value=value)
    gamepad.update()
    
def lThumbStick(xValue,yValue):# values between -32768 and 32767
    global gamepad
    gamepad.left_joystick(x_value=xValue, y_value=yValue) 
    gamepad.update()
    
def rThumbStick(xValue,yValue):# values between -32768 and 32767
    global gamepad
    gamepad.right_joystick(x_value=xValue, y_value=yValue) 
    gamepad.update()

def updateGamepad():
    global gamepad
    if gamepad == None:
        gamepad = vg.VX360Gamepad()