import cyberpi
import mbuild
import mbot2
import time

# --- Configuration ---
SPEED = 45
# Adjust this time (in seconds) so the robot travels exactly 10 to 20 cm!
DRIVE_TIME = 1.5 

# Start-up sequence
cyberpi.console.println("Ready to go!")
cyberpi.led.show("green")
time.sleep(1) # Pause before starting

# --- Step 1: The Initial Drive ---
cyberpi.console.println("Driving forward...")
mbot2.forward(SPEED)
time.sleep(DRIVE_TIME) # Drives straight and ignores the floor for this many seconds

# --- Step 2: Line Following & Blue Hunt ---
cyberpi.console.println("Following line...")
cyberpi.led.show("white")

while True:
    # 1. Check for the Blue Stop Sign first
    sees_blue = (mbuild.quad_rgb_sensor.is_color("blue", "L1", 1) or 
                 mbuild.quad_rgb_sensor.is_color("blue", "R1", 1))
                 
    if sees_blue:
        mbot2.drive_speed(0, 0) # Slam on the brakes!
        cyberpi.console.println("Blue found! Stopped.")
        cyberpi.led.show("blue")
        cyberpi.audio.play("win")
        break # This exits the loop and ends the program safely

    # 2. Standard Line Following Logic
    l2 = mbuild.quad_rgb_sensor.is_line("L2", 1)
    l1 = mbuild.quad_rgb_sensor.is_line("L1", 1)
    r1 = mbuild.quad_rgb_sensor.is_line("R1", 1)
    r2 = mbuild.quad_rgb_sensor.is_line("R2", 1)

    if l1 or r1:
        mbot2.forward(SPEED)
    elif r2:
        mbot2.turn_right(SPEED)
    elif l2:
        mbot2.turn_left(SPEED)
    else:
        # If it loses the line slightly, creep forward to find it again
        mbot2.forward(SPEED - 10)

    # 3. Emergency Stop (Button B)
    if cyberpi.controller.is_press("b"):
        mbot2.drive_speed(0, 0)
        cyberpi.console.println("Emergency Stop")
        cyberpi.led.show("black")
        break

    # 4. The Heartbeat (Prevents lag)
    time.sleep(0.02)
