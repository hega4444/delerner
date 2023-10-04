import sys
import termios
import tty

def get_key():
    # Save the current terminal settings
    old_settings = termios.tcgetattr(sys.stdin)

    try:
        # Set the terminal to raw mode
        tty.setraw(sys.stdin)
        # Read a single character from stdin
        key = sys.stdin.read(1)
        return key
    finally:
        # Restore the terminal settings
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

"""
# Example usage
while True:
    key = get_key()
    if key == 'q':
        break
    else:
        print(f'You pressed: {key}')
"""
