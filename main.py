#!/usr/bin/env python3
import pycozmo
import pygame
import time
import numpy as np

# Define some colors.
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')

# Define some constants for joystick deadbands and max speeds
max_wheel_speed = 150.0
max_head_speed = 3.0
max_lift_speed = 5.0
wheel_deadband = 0.1
head_deadband = 0.05
lift_deadband = 0.05

# Initialize our cozmo image
cozmo_image = np.zeros((240,320,3), np.uint8)

# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint(object):
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font("freesansbold.ttf", 14)

    def tprint(self, screen, textString):
        textBitmap = self.font.render(textString, True, WHITE)
        screen.blit(textBitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


# This takes a forward speed of -1.0 to 1.0 and a rotation/turning 
# speed of -1.0 to 1.0. It returns left wheel and right wheel (in 
# that order) speeds that are range -max_wheel_speed to max_wheel_speed
# The return values are converted from double to float to match
# what the pycozmo drive_wheels command exprects.
def translate_speed(fwd, turn):
    if fwd == 0.0 and turn == 0.0:
        left_wheel_speed = 0.0
        right_wheel_speed = 0.0
    elif fwd == 0.0:
        left_wheel_speed = turn*max_wheel_speed
        right_wheel_speed = -turn*max_wheel_speed
    elif turn == 0.0:
        left_wheel_speed = fwd*max_wheel_speed
        right_wheel_speed = fwd*max_wheel_speed
    else:
        avg_speed = fwd*max_wheel_speed
        turn_speed = turn*max_wheel_speed/2
        left_wheel_speed = avg_speed + turn_speed
        right_wheel_speed = avg_speed - turn_speed
    return float(left_wheel_speed), float(right_wheel_speed)
    


def on_camera_image(cli, new_im):
    """ Handle new images, coming from the robot. """
    del cli
    global cozmo_image
    cozmo_image = np.array(new_im)


def main(run_cozmo = True, use_debug = False):
    global cozmo_image
    pygame.init()
    # Set the width and height of the screen (width, height).
    screen = pygame.display.set_mode((320, 240))
    
    pygame.display.set_caption("Cozmo Drive")
    # Loop until the user clicks the close button.
    done = False
    # Used to manage how fast the screen updates.
    clock = pygame.time.Clock()
    # Initialize the joysticks.
    pygame.joystick.init()
    # Get ready to print.
    textPrint = TextPrint()
    if(use_debug):
        textPrint.tprint(screen, "Starting system!")
        pygame.display.update()

    try:
        cli = None
        if(run_cozmo):
            if(use_debug):
                textPrint.tprint(screen, "Connecting to Cozmo...")
                pygame.display.update()
            # Connect to cozmo
            cli = pycozmo.client.Client(
            protocol_log_messages=None,
            auto_initialize=True,
            enable_animations=True,
            enable_procedural_face=True)
            cli.start()
            cli.connect()
            cli.wait_for_robot()
            cli.enable_camera(enable=True, color=True)
            cli.load_anims()
            cli.set_lift_height(0)
            cli.set_head_angle(0)
            time.sleep(2.0)
            cli.add_handler(pycozmo.event.EvtNewRawCameraImage, on_camera_image)
        forward_speed = 0.0
        turn_speed = 0.0
        head_speed = 0.0
        lift_speed = 0.0
        expression = -1
        make_sound = False

        # -------- Main Program Loop -----------
        while not done:
            screen.fill(WHITE)
            textPrint.reset()
            pygame.surfarray.blit_array(screen,np.rot90(cozmo_image)) 
                       
            # Initializing our joysticks every time so we can get the values in the event queue
            # and handle hot swapping
            for i in range(pygame.joystick.get_count()):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()

            for event in pygame.event.get(): # User did something.
                if event.type == pygame.QUIT: # If user clicked close.
                    done = True # Flag that we are done so we exit this loop.
                elif event.type == pygame.JOYBUTTONDOWN:
                    if(use_debug):
                        textPrint.tprint(screen, "Joystick button {} pressed.".format(event.button))
                    if event.button < 4:
                        expression = event.button
                    elif event.button == 4 or event.button == 5:
                        make_sound = True
                    elif event.button == 7:
                        done = True
                elif event.type == pygame.JOYBUTTONUP:
                    if(use_debug):
                        textPrint.tprint(screen, "Joystick button {} released.".format(event.button))
                elif event.type == pygame.JOYAXISMOTION:
                    if(use_debug):
                        textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(event.axis, event.value))
                    if event.axis == 1:
                        if -wheel_deadband < event.value < wheel_deadband:
                            forward_speed = 0.0
                        else:
                            forward_speed = -event.value
                    elif event.axis == 0:
                        if -wheel_deadband < event.value < wheel_deadband:
                            turn_speed = 0.0
                        else:
                            turn_speed = -event.value
                    elif event.axis == 3:
                        if -head_deadband < event.value < head_deadband:
                            head_speed = 0.0
                        else:
                            head_speed = -event.value * max_head_speed
                    elif event.axis == 2:
                        if -lift_deadband < event.value < lift_deadband:
                            lift_speed = 0.0
                        else:
                            lift_speed = -event.value * max_lift_speed


            if(run_cozmo):
                # Move head
                cli.move_head(head_speed)
                # Move arm
                cli.move_lift(lift_speed)
                # Run expression
                if expression == 0:
                    # TODO: client call to display happy face
                    expression = -1     # This resets so we don't keep restarting the expression every call
                elif expression == 1:
                    # TODO: client call to display angry face
                    expression = -1     # This resets so we don't keep restarting the expression every call
                elif expression == 2:
                    # TODO: client call to display sad face
                    expression = -1     # This resets so we don't keep restarting the expression every call
                elif expression == 3:
                    # TODO: client call to display random face
                    expression = -1     # This resets so we don't keep restarting the expression every call
                # Make sound
                if make_sound:
                    # TODO: client call to play the sound.
                    # Should it do a grab from a couple random sounds? Currently both bumpers come to this if
                    #cli.play_audio("boopboop.wav")
                    make_sound = False  # This resets so we don't keep restarting the audio every call
                    
                # Translate x-y speed to left wheel, right wheel speed
                lwheel,rwheel = translate_speed(forward_speed,turn_speed)
                if(use_debug):
                    textPrint.tprint(screen, "Left wheel: {}".format(lwheel))
                    textPrint.tprint(screen, "Right wheel: {}".format(rwheel))
                # Feed the wheel speeds to cozmo
                cli.drive_wheels(lwheel, rwheel)

            pygame.display.update()
            # Limit to 20 frames per second.
            clock.tick(20)
        if(run_cozmo):
            cli.stop_all_motors()
            cli.disconnect()
            cli.stop()
    finally:
        pygame.quit()



if __name__ == "__main__":
    import sys
    #cozmo_image = None
    # run_event_loop(print_add, print_remove, key_received)
    run_cozmo = True
    use_debug = False
    print_help = False

    # Get what to test
    if len(sys.argv) >= 2:
        commands = sys.argv[1:len(sys.argv)-1]
    else:
        commands = [""]
        #command = str(sys.argv[1])
    
    for arg in commands:
        if str(arg) == "nocozmo":
            run_cozmo = False
        elif str(arg) == "debug" or str(arg) == "-v":
            use_debug = True
        elif str(arg) == "help" or str(arg) == "-h" or\
             str(arg) == "--h" or str(arg) == "?":
            print_help = True

    if print_help:
        print("This program allows for joystick control of a Cozmo robot.")
        print("It displays the robot camera feed if available and allows for")
        print("wheel drive control with the left joystick, head angle control")
        print("by up-down axis on the right joystick, and lift arm height ")
        print("control by the left-right axis on the right joystick. Cozmo")
        print("expressions can be displayed using the four face buttons, and")
        print("audio can be played using the bumper triggers.")
        print("")
        print("This system can be test run without a cozmo by calling this code")
        print("with the nocozmo command. This system can display debug text")
        print("by using the debug command or -v argument.", flush=True)
    else:
        main(run_cozmo, use_debug)
        
        