import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



def plot_waveform():
    # Get the selected waveform from the ComboBox
    selected_waveform = waveform_var.get()

    # Create the figure and the axis
    fig, ax = plt.subplots()
    sampling_f = 100  # liczba probek na jeden okres sygnalu
    signal_duration = 5
    a = 20
    f = 0.5
    # Generate the data based on the selected waveform
    t = np.linspace(0, signal_duration, sampling_f * signal_duration)
    if selected_waveform == "Sine Wave":
        xdosin = np.linspace(0, 2 * np.pi * signal_duration, sampling_f * signal_duration)
        y = a * np.sin(f * xdosin)

    elif selected_waveform == "Triangle Wave":
        p = t * f  # period
        y = a * (2 * np.abs(2 * ((p - 0.25) % 1) - 1) - 1)

    elif selected_waveform == "Rectangle Wave":
        xdosin = np.linspace(0, 2 * np.pi * signal_duration, sampling_f * signal_duration)
        y = a * np.sign(np.sin(f * xdosin))

    # Plot the waveform
    ax.plot(t, y)
    ax.set_title(selected_waveform)
    ax.set_xlabel("t")
    ax.set_ylabel("Amplitude")

    # Clear the previous plot and embed the new plot in the Tkinter window
    for widget in frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)


# Create the main Tkinter window
window = tk.Tk()
window.title("Waveform Plotter")

# Create a frame for the plot
frame = ttk.Frame(window)
frame.grid(row=0, column=2, rowspan=3, columnspan=3)

# Create a ComboBox for waveform selection
waveform_var = tk.StringVar(value="Sine Wave")
waveform_combobox = ttk.Combobox(window, textvariable=waveform_var)
waveform_combobox['values'] = ("Sine Wave", "Triangle Wave", "Rectangle Wave")
waveform_combobox.grid(row=0, column=0)

# Add a button to trigger the plot
button = ttk.Button(window, text="Plot Waveform", command=plot_waveform)
button.grid(row=1, column=0)
entry = ttk.Entry()
entry.grid(row=2, column=0)
# Start the Tkinter event loop
window.mainloop()
