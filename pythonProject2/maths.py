import numpy as np
import math
import matplotlib.pyplot as plt

# Stałe w programie
L = 0.5  # Indukcyjność
R = 1  # Rezystancja
Ke = 0.1  # Stała elektromotoryczna
Kt = 0.1  # Stała momentu obrotowego
J = 0.01  # Moment bezwładności
k = 0.1  # Współczynnik tłumienia

N = 2  # Rząd systemu
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
y = np.zeros(total)  # Sygnał wyjściowy

def main():
    # Definiowanie macierzy A, B, C
    A = np.array([[-R / L - (Ke * Kt) / (J * L), Ke * k / J],
                  [Kt / (J * L), -k / J]])
    B = np.array([1 / L, 0])
    C = np.array([1, 0])
    D = 0

    # Rozmiar wektorów danych
    w = 2.0 * PI * Lo / T  # Częstotliwość sinusoidy L/T = F

    # Obliczenie pobudzenia – sinus, fala prostokątna oraz fala trójkątna
    for i in range(total):
        t = i * step
        sin[i] = amplitude * math.sin(w * t)  # Sygnał wejściowy sinus: u=M*sin(w*t)
        rec[i] = amplitude if sin[i] > 0 else -amplitude  # Sygnał wejściowy fala prostokątna
        tri[i] = 4 * amplitude * abs(((t * freq - 0.25) % 1) - 0.5) - amplitude  # Sygnał wejściowy trójkątny

    # Zerowe warunki początkowe
    xi_1 = np.zeros(N)

    # Główna pętla obliczeń - zamiast pobudzenia sinus (sin) można wstawić falę (rec) lub trójkąt (tri)
    for i in range(total):
        Ax = A @ xi_1
        Bu = B * tri[i]  # Można zmienić na sin[i] lub rec[i]
        Cx = C @ xi_1
        xi = (Ax + Bu) * step
        xi = xi_1 + xi
        xi_1 = xi
        y[i] = Cx  # + D * tri[i] można dodać jeśli D ≠ 0

    return sin, rec, tri, y

if __name__ == "__main__":
    results_us, results_uf, results_ut, results_y = main()
    time = np.linspace(0, T, total)
    plt.plot(time, results_y, label='y(t)')
    plt.xlabel('Czas (s)')
    plt.ylabel('y(t)')
    plt.title('Wykres y(t)')
    plt.legend()
    plt.grid(True)
    plt.show()
