import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import messagebox
import time


# Function to handle the connection and sending message
def connect_and_send(str):
    # List available serial ports
    available_ports = list_ports()

    if not available_ports:
        messagebox.showerror("Error", "No serial ports found!")
        return

   # Create a custom popup window to select the serial port
    window = tk.Tk()
    window.title("Select Serial Port")

    # Create a label
    label = tk.Label(window, text="Available Ports (copy-paste enabled):")
    label.pack(pady=10)

    # Create a Text widget to show the available ports for copy-pasting
    port_text = tk.Text(window, height=6, width=50)
    port_text.insert(tk.END, '\n'.join(available_ports))  # Display the available ports
    port_text.config(state=tk.DISABLED)  # Make it non-editable, only for display (copy-paste allowed)
    port_text.pack(pady=10)

    # Label for the Entry box
    entry_label = tk.Label(window, text="Enter the Serial Port:")
    entry_label.pack(pady=5)
    port_entry = tk.Entry(window, width=50)
    port_entry.pack(pady=5)

    # Function to handle the connection after port is selected or entered
    def on_select():
        selected_port = port_entry.get().strip()
        if selected_port:
            window.destroy()  # Close the window after selection
            send_message(selected_port,str)
        else:
            messagebox.showwarning("Warning", "Please enter a valid port.")

    # Add a button to confirm the selection
    select_button = tk.Button(window, text="Select Port", command=on_select)
    select_button.pack(pady=10)

    # Run the main tkinter loop to show the window
    window.mainloop()

# Function to list available serial ports
def list_ports():
    ports = serial.tools.list_ports.comports()
    port_list = []
    for port in ports:
        port_list.append(port.device)
    return port_list

# Function to prompt the user for a message to send
def send_message(selected_port,message):
    try:
        # Open the selected serial port
        ser = serial.Serial(selected_port, 9600, timeout=1)
        time.sleep(2)  # Wait for connection to establish

        # Send the message
        ser.write(message.encode())  # Send string as bytes
        messagebox.showinfo("Success", f"Message sent: {message}")

        # Close the serial port
        ser.close()
    except serial.SerialException as e:
        messagebox.showerror("Error", f"Failed to connect: {e}")


if __name__=="__main__":

    # Start the serial connection and communication process
    connect_and_send()
