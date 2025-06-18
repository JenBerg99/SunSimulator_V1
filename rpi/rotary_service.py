from gpiozero import Button
from time import sleep
from threading import Thread
from rpi.lcd.I2CLCD1602 import print_toLCD
from cache import cache
import time

last_internal_update = 0

# GPIO pin definitions
PIN_CLK = 18     # Rotary encoder CLK pin
PIN_DT = 15      # Rotary encoder DT pin
PIN_BTN = 14     # Rotary encoder push button pin

# Setup GPIO buttons
clk = Button(PIN_CLK, pull_up=True)
dt = Button(PIN_DT, pull_up=True)
btn = Button(PIN_BTN, pull_up=True)

# Initial encoder state and variables
last_state = (clk.value << 1) | dt.value
step_accumulator = 0
mode_index = -1  # -1 = inactive, 0 = Red, 1 = Green, 2 = Blue, 3 = Brightness
running = True   # Used to stop the loop on shutdown


def read_encoder():
    """
    Reads the rotary encoder and applies changes based on current mode.
    Supports modifying R, G, B channels or overall brightness.
    """
    global step_accumulator, last_state, mode_index

    # Combine current pin states into 2-bit value
    state = (clk.value << 1) | dt.value

    if state != last_state:
        # Create 4-bit transition value
        transition = (last_state << 2) | state

        # Detect rotation direction
        if transition in [0b1101, 0b0100, 0b0010, 0b1011]:
            step_accumulator += 1
        elif transition in [0b1110, 0b0111, 0b0001, 0b1000]:
            step_accumulator -= 1

        last_state = state

        # Apply change only after 2 valid steps
        if abs(step_accumulator) >= 2 and mode_index in [0, 1, 2, 3]:
            model = cache.get_sunlight_properties()

            if mode_index in [0, 1, 2]:  # Adjust RGB channels
                rgb = list(model.rgb_color)
                if step_accumulator > 0:
                    rgb[mode_index] = min(255, rgb[mode_index] + 2)
                else:
                    rgb[mode_index] = max(0, rgb[mode_index] - 2)
                model.rgb_color = tuple(rgb)
                print(f"RGB updated: R={rgb[0]}, G={rgb[1]}, B={rgb[2]}")
                
                mode_names = ["Red", "Green", "Blue"]
                current_mode = mode_names[mode_index]
                print_toLCD(current_mode, f"{rgb[mode_index]}")

            elif mode_index == 3:  # Adjust brightness
                brightness = model.brightness_percent
                if step_accumulator > 0:
                    brightness = min(100, brightness + 2)
                else:
                    brightness = max(1, brightness - 2)
                model.brightness_percent = brightness
                print(f"Brightness updated: {brightness:.0f}%")

                print_toLCD("Brightness", f"{brightness:.0f}%")

            # Save updated model back to cache            
            global last_internal_update 
            last_internal_update = time.time()
            cache.set_sunlight_properties(model)            
            step_accumulator = 0


def cycle_mode():
    """
    Cycles through available control modes:
    Red → Green → Blue → Brightness → Inactive → Red ...
    """   
    global mode_index 
    mode_index = (mode_index + 1) % 5  # 0-3 = active modes, 4 = inactive
    modes = ["Red", "Green", "Blue", "Brightness", "Inactive"]
    print(f"Mode: {modes[mode_index]}")
    print_mode()

# Attach button press to mode switcher
btn.when_pressed = cycle_mode

def print_mode():
    global mode_index
    modes = ["Red", "Green", "Blue", "Brightness", "Inactive"]

    model = cache.get_sunlight_properties()
    rgb = model.rgb_color
    brightness = model.brightness_percent

    if mode_index == 4: #interactive
        print_toLCD(f"R:{rgb[0]}G:{rgb[1]}B:{rgb[2]}", f"Brightness: {brightness:.0f}%")
    else:
        current_mode = modes[mode_index]
        value = (rgb[mode_index] if mode_index in [0,1,2] else f"{brightness:.0f}%")
        print_toLCD(current_mode, f"{value}")

def on_cache_update(update_model):
    global last_internal_update

    print(last_internal_update)
    print(time.time() - last_internal_update )

    if (time.time() - last_internal_update) < 0.2:        
        return

    global mode_index
    mode_index = 4
    print_mode()
    

def rotary_loop():
    """
    Background loop that continuously reads the encoder.
    """
    print("Rotary encoder monitoring started.")
    global mode_index
    mode_index = 4
    print_mode()
    
    while running:
        read_encoder()
        sleep(0.001)  # Small delay to reduce CPU usage


def start_rotary_thread():
    """
    Starts the rotary encoder loop in a background thread.
    """
    cache.register_observer(on_cache_update)
    t = Thread(target=rotary_loop, daemon=True)
    t.start()


def stop_rotary():
    """
    Stops the rotary encoder loop.
    """
    global running
    running = False
    print("Rotary encoder monitoring stopped.")