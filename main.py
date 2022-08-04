#!/usr/bin/env python3
import pycozmo
import pygame
import time
import numpy as np

# Define some colors.
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')

# Define some constants
max_wheel_speed = 150.0
max_head_speed = 3.0
max_lift_speed = 5.0
wheel_deadband = 0.1
head_deadband = 0.05
lift_deadband = 0.05

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


def translate_speed(fwd, turn):
    if fwd == 0.0 and turn == 0.0:
        return 0.0, 0.0
    elif fwd == 0.0:
        return turn*max_wheel_speed, -turn*max_wheel_speed
    elif turn == 0.0:
        return fwd*max_wheel_speed, fwd*max_wheel_speed
    else:
        avg_speed = fwd*max_wheel_speed
        turn_speed = turn*max_wheel_speed/2
        return avg_speed + turn_speed, avg_speed - turn_speed


def on_camera_image(cli, new_im):
    """ Handle new images, coming from the robot. """
    del cli
    global cozmo_image
    cozmo_image = np.array(new_im)


def main(run_cozmo = True):
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

    try:
        cli = None
        if(run_cozmo):
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
                       
            # Blah blah, initialize joysticks
            for i in range(pygame.joystick.get_count()):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()


            for event in pygame.event.get(): # User did something.
                if event.type == pygame.QUIT: # If user clicked close.
                    done = True # Flag that we are done so we exit this loop.
                elif event.type == pygame.JOYBUTTONDOWN:
                    #textPrint.tprint(screen, "Joystick button {} pressed.".format(event.button))
                    if event.button < 4:
                        expression = event.button
                    elif event.button == 4 or event.button == 5:
                        make_sound = True
                    elif event.button == 7:
                        done = True
                #elif event.type == pygame.JOYBUTTONUP:
                    #textPrint.tprint(screen, "Joystick button {} released.".format(event.button))
                elif event.type == pygame.JOYAXISMOTION:
                    #event.axis, event.value, joystick
                    #textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(event.axis, event.value))
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
                    # happy face
                    expression = -1
                elif expression == 1:
                    #angry face
                    expression = -1
                elif expression == 2:
                    # sad face
                    expression = -1
                elif expression == 3:
                    # rando face
                    expression = -1
                # Make sound
                if make_sound:
                    make_sound = False
                    #cli.play_audio("boopboop.wav")
                # Translate x-y speed to left wheel, right wheel speed
                #lwheel, rwheel = translate_speed(cozmo_speed)
                lwheel,rwheel = translate_speed(forward_speed,turn_speed)
                cli.drive_wheels(float(lwheel), float(rwheel))

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

    # Get what to test
    if len(sys.argv) >= 2:
        command = str(sys.argv[1])
    else:
        command = ""
        #command = str(sys.argv[1])
    
    if command != "nocozmo" and command != "":
        command = "-h"

    if command == "-h":
        print("This program allows for joystick control of a Cozmo robot.")
        print("It displays the robot camera feed if available and allows for")
        print("wheel drive control with the left joystick, head angle control")
        print("by up-down axis on the right joystick, and lift arm height ")
        print("control by the left-right axis on the right joystick. Cozmo")
        print("expressions can be displayed using the four face buttons, and")
        print("audio can be played using the bumper triggers.")
        print("")
        print("This system can be test run without a cozmo by calling this code")
        print("with the nocozmo command.", flush=True)
    elif command == "nocozmo":
        #Run as main program
        main(False)
    else:
        main()
        
        