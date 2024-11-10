import sys
import time

# Kode warna ANSI untuk terminal
color1 = "\033[91m"  # Merah
color2 = "\033[94m"  # Biru
reset_color = "\033[0m"  # Reset warna ke default

# Animasi ASCII
def print_dual_color_ascii(ascii_art, duration=5, delay=0.5):
    ascii_lines = ascii_art.splitlines()
    num_lines = len(ascii_lines)
    start_time = time.time()

    for line in ascii_lines:
        print(line)

    # Loop animasi
    while time.time() - start_time < duration:
        for color in [color1, color2]:  
            for _ in range(num_lines):
                sys.stdout.write("\033[F")

            for line in ascii_lines:
                sys.stdout.write(f"{color}{line}{reset_color}\n")
            sys.stdout.flush()
            time.sleep(delay)

# Animasi loading cube
def print_loading_animation(message, duration=5):
    animation = "|/-\\"
    print(message, end="", flush=True)
    for i in range(duration * 4):  
        time.sleep(0.25)
        sys.stdout.write(f"\r{message} {animation[i % len(animation)]}")
        sys.stdout.flush()
    sys.stdout.write("\r" + " " * (len(message) + 2) + "\r")