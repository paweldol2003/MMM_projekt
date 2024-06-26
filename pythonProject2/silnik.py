import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk


# Stałe w programie
L = 0.5  # Indukcyjność
R = 1  # Rezystancja
Ke = 0.1  # Stała elektromotoryczna
Kt = 0.1  # Stała momentu obrotowego
J = 0.01  # Moment bezwładności
k = 0.1  # Współczynnik tłumienia

N = 2  # Rząd układu
step = 0.01  # Krok obliczeń        
T = 10.0  # Całkowity czas symulacji – przedział [0 , T]
freq = 0.25  # Częstotliwość sygnału
Lo = T * freq  # Liczba okresów sygnału sinus w przedziale T
amplitude = 8.0  # Amplituda sygnału sinus
PI = 3.14159265  # Liczba PI

# Zmienne globalne w programie
total = int(T / step) + 1
sin = np.zeros(total)  # Sygnał wejściowy sinus
rec = np.zeros(total)  # Sygnał wejściowy fala prostokątna
tri = np.zeros(total)  # Sygnał wejściowy trójkątny
prad_wyjsciowy = np.zeros(total)
moment_wyjsciowy = np.zeros(total)

def main(L, R, Ke, Kt, J, k, amplitude, freq, T, signal_type):
    total = int(T / step) + 1

    # Definiowanie macierzy A, B, C
    A = np.array([[-R / L - (Ke * Kt) / (J * L),     Ke * k / J],
                  [Kt / (J * L),     -k / J]])
    B = np.array([1 / L, 0])
    Ci = np.array([1, 0])
    Cm = np.array([0, 1])
    D = 0

    # Obliczenie pobudzenia – sinus, fala prostokątna oraz fala trójkątna
    w = 2.0 * PI * freq  # Częstotliwość sinusoidy L/T = F
    for i in range(total):
        t = i * step
        sin[i] = amplitude * math.sin(w * t)  # Sygnał wejściowy sinus: u=M*sin(w*t)
        rec[i] = amplitude if sin[i] > 0 else -amplitude  # Sygnał wejściowy fala prostokątna
        tri[i] = 4 * amplitude * abs(((t * freq - 0.25) % 1) - 0.5) - amplitude  # Sygnał wejściowy trójkątny

    # Wybór sygnału wejściowego
    if signal_type == 'sin':
        input_signal = sin
    elif signal_type == 'rec':
        input_signal = rec
    elif signal_type == 'tri':
        input_signal = tri

    # Zerowe warunki początkowe
    xi_1 = np.zeros(N)

    # Główna pętla obliczeń
    for i in range(total):
        Ax = A @ xi_1
        Bu = B * input_signal[i]
        Cix = Ci @ xi_1
        Cmx = Cm @ xi_1
        xi = (Ax + Bu) * step
        xi = xi_1 + xi
        xi_1 = xi
        prad_wyjsciowy[i] = Cix  # + D * tri[i] można dodać jeśli D ≠ 0
        moment_wyjsciowy[i] = Cmx

    return sin, rec, tri, prad_wyjsciowy, moment_wyjsciowy, input_signal

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Symulacja silnika elektrycznego")
        
        self.create_widgets()
        
    def create_widgets(self):
        self.labels_entries = {}
        variables = {
            "Indukcyjność": L, "Rezystancja": R, "Stała elektromotryczna Ke": Ke, "Stała momentu obrotowego Kt": Kt,
            "Moment bezwładności": J, "Współczynnik tłumienia k": k, "Amplituda": amplitude,
            "Częstotliwość": freq, "Czas trwania sygnału": T
        }
        
        for i, (label, value) in enumerate(variables.items()):
            tk.Label(self, text=label).grid(row=i, column=0)
            entry = tk.Entry(self)
            entry.insert(0, value)
            entry.grid(row=i, column=1)
            self.labels_entries[label] = entry
        
        self.signal_type = tk.StringVar(value="sin")
        tk.Label(self, text="Sygnał wejściowy").grid(row=len(variables), column=0)
        tk.Radiobutton(self, text="Sinusoidalny", variable=self.signal_type, value="sin").grid(row=len(variables), column=1)
        tk.Radiobutton(self, text="Prostokątny", variable=self.signal_type, value="rec").grid(row=len(variables), column=2)
        tk.Radiobutton(self, text="Trójkątny", variable=self.signal_type, value="tri").grid(row=len(variables), column=3)

        tk.Button(self, text="Uruchom", command=self.run_simulation).grid(row=len(variables)+1, column=0, columnspan=4)
        
        self.fig, self.axs = plt.subplots(3, 1, figsize=(8, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=4, rowspan=len(variables)+2)
        
    def run_simulation(self):
        # Pobranie wartości z pól tekstowych
        L = float(self.labels_entries["Indukcyjność"].get())
        R = float(self.labels_entries["Rezystancja"].get())
        Ke = float(self.labels_entries["Stała elektromotryczna Ke"].get())
        Kt = float(self.labels_entries["Stała momentu obrotowego Kt"].get())
        J = float(self.labels_entries["Moment bezwładności"].get())
        k = float(self.labels_entries["Współczynnik tłumienia k"].get())
        amplitude = float(self.labels_entries["Amplituda"].get())
        freq = float(self.labels_entries["Częstotliwość"].get())
        T = float(self.labels_entries["Czas trwania sygnału"].get())
        signal_type = self.signal_type.get()
        
        # Uruchomienie symulacji
        sin, rec, tri, prad_wyjsciowy, moment_wyjsciowy, sygnal_wejsciowy = main(L, R, Ke, Kt, J, k, amplitude, freq, T, signal_type)
        
        # Aktualizacja wykresów
        time = np.linspace(0, T, len(prad_wyjsciowy))
        self.axs[0].cla()
        self.axs[1].cla()
        self.axs[2].cla()

        self.axs[0].plot(time, sygnal_wejsciowy, label="Sygnał wejściowy")
        self.axs[1].plot(time, prad_wyjsciowy, label="Prąd")
        self.axs[2].plot(time, moment_wyjsciowy, label="Moment")

        # Dodanie etykiet do osi
        self.axs[0].set_xlabel('Czas (s)')
        self.axs[0].set_ylabel('Amplituda')
        self.axs[1].set_xlabel('Czas (s)')
        self.axs[1].set_ylabel('Prąd (A)')
        self.axs[2].set_xlabel('Czas (s)')
        self.axs[2].set_ylabel('Moment (Nm)')
                               
        for ax in self.axs:
            ax.grid(True)
        
        self.fig.tight_layout()
        self.canvas.draw()


app = Application()
app.mainloop()
