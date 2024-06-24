import numpy as np
import math
import matplotlib.pyplot as plt


# inputs

def sin_wave(a, f, signal_duration, sampling_f):
    xdosin = np.linspace(0, 2 * np.pi * signal_duration, sampling_f * signal_duration)
    y = a * np.sin(f * xdosin)
    return y


def rectangle_wave(a, f, signal_duration, sampling_f):
    xdosin = np.linspace(0, 2 * np.pi * signal_duration, sampling_f * signal_duration)
    y = a * np.sign(np.sin(f * xdosin))
    return y


def triangle_wave(a, f, signal_duration, sampling_f):
    t = t = np.linspace(0, signal_duration, sampling_f * signal_duration)
    period = t * f
    y = a * (2 * np.abs(2 * ((period - 0.25) % 1) - 1) - 1)
    return y


# stałe w programie


N = 2  # rząd systemu
h = 0.01  # krok obliczeń
T = 10.0  # całkowity czas symulacji – przedział [0 , T]
L = 2.5  # liczba okresów sygnału sinus w przedziale T
M = 8.0  # amplituda sygnału sinus
PI = 3.14159265  # liczba PI


# nowe typy – macierz kwadratowa (NxN) i wektor (Nx1)
class Vect:
    def __init__(self):
        self.n = np.zeros(N)

    def __add__(self, other):
        result = Vect()
        result.n = self.n + other.n
        return result

    def __mul__(self, scalar):
        result = Vect()
        result.n = self.n * scalar
        return result

    def dot(self, other):
        return np.dot(self.n, other.n)


class Matr:
    def __init__(self):
        self.n = np.zeros((N, N))

    def __mul__(self, vect):
        result = Vect()
        result.n = np.dot(self.n, vect.n)
        return result


# zmienne globalne w programie
total = int(T / h) + 1
us = np.zeros(total)  # sygnał wejściowy sinus
uf = np.zeros(total)  # sygnał wejściowy fala prostokątna
ut = np.zeros(total)  # sygnał wejściowy trójkątny
y = np.zeros(total)  # sygnał wyjściowy


# program główny
def main():
    A = Matr()
    B = Vect()
    C = Vect()

    # wczytanie parametrów modelu
    R = float(input("\n R = "))
    Lc = float(input("\n L = "))
    Ke = float(input("\n Ke = "))
    Kt = float(input("\n Kt = "))
    J = float(input("\n J = "))
    k = float(input("\n k = "))

    a0 = (-R / Lc - (Ke * Kt) / J * Lc)
    a1 = Ke * k / J
    a2 = Kt / J * Lc
    a3 = -k / J
    b0 = 1 / Lc
    # zapisanie macierzy i wektorów modelu
    A.n[0][0], A.n[0][1] = a0, a1
    A.n[1][0], A.n[1][1] = a2, a3

    B.n[0], B.n[1] = b0, 0
    C.n[0], C.n[1] = 1, 0
    D = 0

    # rozmiar wektorów danych
    w = 2.0 * PI * L / T  # częstotliwość sinusoidy L/T = F

    # obliczenie pobudzenia – sinus, fala prostokątna oraz fala trójkątna
    for i in range(total):
        t = i * h
        us[i] = M * math.sin(w * t)  # sygnał wejściowy sinus: u=M*sin(w*t)
        uf[i] = M if us[i] > 0 else -M  # sygnał wejściowy fala prostokątna
        ut[i] = ut[i] = 4 * M * T / L * abs((t - 1 / 4 * T / L) % 4 - 1 / 2 * T / L) - M  # sygnał wejściowy trójkątny

    # zerowe warunki początkowe
    xi_1 = Vect()

    # główna pętla obliczeń - zamiast pobudzenia sinus (us) można wstawić falę (uf) lub trójkąt (ut)
    for i in range(total):
        Ax = A * xi_1
        Bu = B * us[i]  # można zmienić na uf[i] lub ut[i]
        Cx = C.dot(xi_1)
        Du = D * us[i]  # można zmienić na uf[i] lub ut[i]
        xi = (Ax + Bu) * h
        xi = xi_1 + xi
        xi_1 = xi
        y[i] = Cx + Du

    # zapisanie wyników u(t) (sinus, prostokąt, trójkąt) i y(t) do tablic
    results_us = us.tolist()
    results_uf = uf.tolist()
    results_ut = ut.tolist()
    results_y = y.tolist()

    return results_us, results_uf, results_ut, results_y


if __name__ == "__main__":
    results_us, results_uf, results_ut, results_y = main()
    # print("Results u(t) sinus:", results_us)
    #print("Results u(t) prostokąt:", results_uf)
    #print("Results u(t) trójkąt:", results_ut)
    print("Results y(t):", results_y)
    time = np.linspace(0, T, total)
    plt.plot(time, results_y, label='y(t)')
    plt.xlabel('Czas (s)')
    plt.ylabel('y(t)')
    plt.title('Wykres y(t)')
    plt.legend()
    plt.grid(True)
    plt.show()



