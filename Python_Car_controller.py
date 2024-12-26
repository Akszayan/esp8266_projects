import tkinter as tk      
from tkinter import ttk
import socket

# Global variables
connected = False
sock = None
motor_speed = 512  # Default motor speed
current_command = None  # Tracks the current movement command
speed_label = None  # Global variable to hold the speed label


def connect_to_car(ip_entry, port_entry, status_label):
    global connected, sock
    if not connected:
        try:
            ip = ip_entry.get()
            port = int(port_entry.get())
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            connected = True
            status_label.config(text="Connected", fg="green")
        except Exception as e:
            status_label.config(text=f"Connection failed: {e}", fg="red")

def send_command(command):
    global connected
    if connected:
        try:
            sock.sendall(f"{command};\n".encode())
        except Exception as e:
            print(f"Error sending command: {e}")

def move(command):
    global current_command
    current_command = command
    # Send the current command and the speed
    send_command(f"{command} Speed:{motor_speed}")
    print(f"{command} with speed {motor_speed}")

def move_forward(event=None):
    move("F")

def move_backward(event=None):
    move("B")

def turn_left(event=None):
    move("L")

def turn_right(event=None):
    move("R")

def stop_movement(event=None):
    global current_command
    current_command = None
    send_command("S")
    print("Stopping")

def adjust_speed(value):
    global motor_speed
    try:
        motor_speed = int(float(value))  # Convert slider value to integer
        if current_command:
            send_command(f"{current_command} Speed:{motor_speed}")
        print(f"Speed set to {motor_speed}")
        # Update the speed label in the GUI
        speed_label.config(text=f"Speed: {motor_speed}")
    except ValueError as e:
        print(f"Invalid slider value: {value}, Error: {e}")

def on_key_press(event):
    if event.keysym == 'Up':
        move("F")
    elif event.keysym == 'Down':
        move("B")
    elif event.keysym == 'Left':
        move("L")
    elif event.keysym == 'Right':
        move("R")
    elif event.keysym == 'space':
        stop_movement()

def on_key_release(event):
    stop_movement()  # Stop when key is released

def start_gui():
    global speed_label  # Referencing the global speed_label variable

    root = tk.Tk()
    root.title("RC Car Controller")

    # Set a background color
    root.config(bg="#1E1E1E")
    root.geometry("600x500")

    # Connection frame
    connection_frame = tk.Frame(root, pady=20, bg="#2C2F36", bd=2, relief="solid")
    connection_frame.pack(padx=20, pady=20, fill="x")
    
    tk.Label(connection_frame, text="IP Address:", bg="#2C2F36", fg="white", font=("Arial", 12)).grid(row=0, column=0, padx=5)
    ip_entry = tk.Entry(connection_frame, width=15, font=("Arial", 12))
    ip_entry.grid(row=0, column=1, padx=5)
    ip_entry.insert(0, "192.168.137.155")
    
    tk.Label(connection_frame, text="Port:", bg="#2C2F36", fg="white", font=("Arial", 12)).grid(row=0, column=2, padx=5)
    port_entry = tk.Entry(connection_frame, width=5, font=("Arial", 12))
    port_entry.grid(row=0, column=3, padx=5)
    port_entry.insert(0, "8080")
    
    connect_button = tk.Button(
        connection_frame,
        text="Connect",
        command=lambda: connect_to_car(ip_entry, port_entry, status_label),
        font=("Arial", 12),
        bg="#4CAF50",
        fg="white",
        relief="raised"
    )
    connect_button.grid(row=0, column=4, padx=10)

    # Status label
    status_label = tk.Label(connection_frame, text="Not Connected", fg="red", font=("Arial", 12))
    status_label.grid(row=1, columnspan=5)

    # Movement frame
    movement_frame = tk.Frame(root, pady=20, bg="#2C2F36")
    movement_frame.pack(fill="x", padx=20)
    
    tk.Button(movement_frame, text="Forward", command=move_forward, width=15, height=2, font=("Arial", 12), bg="#2196F3", fg="white").grid(row=0, column=1, pady=10)
    tk.Button(movement_frame, text="Backward", command=move_backward, width=15, height=2, font=("Arial", 12), bg="#FF5722", fg="white").grid(row=2, column=1, pady=10)
    tk.Button(movement_frame, text="Left", command=turn_left, width=15, height=2, font=("Arial", 12), bg="#FFC107", fg="white").grid(row=1, column=0, pady=10)
    tk.Button(movement_frame, text="Right", command=turn_right, width=15, height=2, font=("Arial", 12), bg="#FFC107", fg="white").grid(row=1, column=2, pady=10)
    tk.Button(movement_frame, text="Stop", command=stop_movement, bg="red", fg="white", width=15, height=2, font=("Arial", 12), relief="raised").grid(row=1, column=1, pady=10)

    # Speed control frame
    speed_frame = tk.Frame(root, pady=20, bg="#2C2F36")
    speed_frame.pack(fill="x", padx=20)
    tk.Label(speed_frame, text="Speed Control:", bg="#2C2F36", fg="white", font=("Arial", 12)).pack(side=tk.LEFT)
    
    speed_slider = ttk.Scale(speed_frame, from_=0, to=1023, orient="horizontal", command=adjust_speed, length=300)
    speed_slider.set(512)
    speed_slider.pack(side=tk.LEFT, padx=10)

    # Current state display
    state_frame = tk.Frame(root, pady=20, bg="#2C2F36", bd=2, relief="solid")
    state_frame.pack(padx=20, pady=20, fill="x")
    
    # Movement status
    movement_label = tk.Label(state_frame, text="Movement: Stopped", bg="#2C2F36", fg="white", font=("Arial", 12))
    movement_label.grid(row=0, column=0, padx=5, pady=5)
    
    # Speed status (this is the updated speed label)
    speed_label = tk.Label(state_frame, text=f"Speed: {motor_speed}", bg="#2C2F36", fg="white", font=("Arial", 12))
    speed_label.grid(row=1, column=0, padx=5, pady=5)

    # Key bindings
    root.bind("<Up>", on_key_press)
    root.bind("<Down>", on_key_press)
    root.bind("<Left>", on_key_press)
    root.bind("<Right>", on_key_press)
    root.bind("<space>", on_key_press)  # Spacebar to stop

    # Key release bindings to stop movement
    root.bind("<KeyRelease-Up>", on_key_release)
    root.bind("<KeyRelease-Down>", on_key_release)
    root.bind("<KeyRelease-Left>", on_key_release)
    root.bind("<KeyRelease-Right>", on_key_release)
    root.bind("<KeyRelease-space>", on_key_release)  # Spacebar to stop

    root.mainloop()

# Start GUI
if __name__ == "__main__":
    start_gui()
