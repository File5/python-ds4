# Source:
# https://www.pygame.org/docs/ref/joystick.html
#
# This program was modified to control my Raspberry Pi robot
# with a PS-4 Controller
#
# Autor (modification):   Ingmar Stapel
# Datum:   20180724
# Version:   1.2
# Homepage:   http://custom-build-robots.com
import pygame

# Das Programm L298NHBridgePCA9685.py wird als Modul geladen. Es stellt
# die Funktionen fuer die Steuerung der H-Bruecke zur Verfuegung.
# import L298NHBridgePCA9685 as HBridge

event_axis_3 = 0
event_axis_4 = 0

offset = 0.25

speedleft = 0
speedright = 0

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)
    def printz(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
    def indent(self):
        self.x += 10
    def unindent(self):
        self.x -= 10


pygame.init()

# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Robot controller")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

# Get ready to print
textPrint = TextPrint()

# -------- Main Program Loop -----------
while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop

        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        #if event.type == pygame.JOYBUTTONDOWN:
        #    print("Joystick button pressed.")
        #if event.type == pygame.JOYBUTTONUP:
        #    print("Joystick button released.")


    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    textPrint.printz(screen, "Number of joysticks: {}".format(joystick_count) )
    textPrint.indent()

    # For each joystick connected to the robot:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        textPrint.printz(screen, "Joystick {}".format(i) )
        textPrint.indent()

        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        textPrint.printz(screen, "Joystick name: {}".format(name) )

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.printz(screen, "Number of axes: {}".format(axes) )
        textPrint.indent()

        for i in range( axes ):
            axis = joystick.get_axis( i )
            textPrint.printz(screen, "Axis {} value: {:>6.3f}".format(i, axis) )
        textPrint.unindent()

        buttons = joystick.get_numbuttons()
        textPrint.printz(screen, "Number of buttons: {}".format(buttons) )
        textPrint.indent()

        for i in range( buttons ):
            button = joystick.get_button( i )
            textPrint.printz(screen, "Button {:>2} value: {}".format(i,button) )
        textPrint.unindent()

        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.
        hats = joystick.get_numhats()
        textPrint.printz(screen, "Number of hats: {}".format(hats) )
        textPrint.indent()

        for i in range( hats ):
            hat = joystick.get_hat( i )
            textPrint.printz(screen, "Hat {} value: {}".format(i, str(hat)) )
        textPrint.unindent()

        textPrint.unindent()

    # Check for any queued events and then process each one
    events = pygame.event.get()

    for event in events:

        # Start modification to control my robot via PCA9685 servo controller...

        # Check if one of the joysticks has moved
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 3:
                # inverted the event.value for an easyer programming / understanding
                event_axis_3 = event.value * -1
            elif event.axis == 4:
                # inverted the event.value for an easyer programming / understanding
                event_axis_4 = event.value * -1


            # move backwards
            if event_axis_4 <= 0 and offset > event_axis_3 > -offset:
                speedleft = (event_axis_4)
                speedright = (event_axis_4)

            # move forwards
            elif event_axis_4 >= 0 and offset > event_axis_3 > -offset:
                speedleft = (event_axis_4)
                speedright = (event_axis_4)


            # turn left on spot
            elif event_axis_3 > offset and offset > event_axis_4 > -offset:
                speedleft = (event_axis_3*-1)
                speedright = (event_axis_3)

            # turn right on spot
            elif event_axis_3 < -offset and offset > event_axis_4 > -offset:
                speedleft = (event_axis_3*-1)
                speedright = (event_axis_3)


            # move forward right (Q1)
            elif event_axis_4 > offset and event_axis_3 < -offset:
                speedleft = (event_axis_4 - event_axis_3)
                speedright = (event_axis_4 + event_axis_3)

            # move backward right (Q2)
            elif event_axis_4 < -offset and event_axis_3 < -offset:
                speedleft = (event_axis_4 + event_axis_3)
                speedright = (event_axis_4 - event_axis_3)

            # move backward left (Q3)
            elif event_axis_4 < -offset and event_axis_3 > offset:
                speedleft = (event_axis_4 + event_axis_3)
                speedright = (event_axis_4 - event_axis_3)

            # move forward left (Q4)
            elif event_axis_4 > offset and event_axis_3 > offset:
                speedleft = (event_axis_4 - event_axis_3)
                speedright = (event_axis_4 + event_axis_3)

            # HBridge.setMotorLeft(round(speedleft, 2))
            # HBridge.setMotorRight(round(speedright, 2))

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()
