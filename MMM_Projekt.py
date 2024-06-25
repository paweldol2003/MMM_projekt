
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

CZESTOTLIWOSC_PROBKOWANIA = 100              #liczba probek na jeden okres sygnalu 
czas_trwania_sygnalu = 5                                  
amplituda = 20                   
czestotliwosc = 0.5
faza = 0
czas = np.linspace(0, czas_trwania_sygnalu, CZESTOTLIWOSC_PROBKOWANIA * czas_trwania_sygnalu)


def sinusoida():
    xdosin = np.linspace(0, 2*np.pi*czas_trwania_sygnalu, CZESTOTLIWOSC_PROBKOWANIA*czas_trwania_sygnalu)
    y=amplituda * np.sin(czestotliwosc * xdosin + faza)
    return y

def prostokat():
    xdosin = np.linspace(0, 2*np.pi*czas_trwania_sygnalu, CZESTOTLIWOSC_PROBKOWANIA*czas_trwania_sygnalu)
    y=amplituda * np.sign(np.sin(czestotliwosc * xdosin))
    return y

def trojkat():
    okres = czas*czestotliwosc
    y = amplituda * (2 * np.abs(2 * ((okres - 0.25) % 1) - 1) - 1)
    return y
    
def wykres(y):
    plt.plot(czas, y)
    plt.xlabel('CZAS')
    plt.ylabel('Os Y')
    plt.title('Sygnal wejsciowy')
    plt.show()
    
    
def rodzaj_sygnalu_wejsciowego(wybor):
    
    if wybor == 1: y = sinusoida()         
    elif wybor == 2: y = prostokat()        
    elif wybor == 3: y = trojkat()    
    wykres (y)      
        


#Ustawienia okna i przyciski
root = tk.Tk()
root.title("Symulator silnika elektrycznego")

amplituda_opis = ttk.Label(root, text="Wybierz rodzaj sygnalu wejsciowego")
amplituda_opis.grid(row=0, column=0, pady=(20, 5))
sinusoida_przycisk = ttk.Button(root, text="SINUSOIDA", command=lambda: rodzaj_sygnalu_wejsciowego(1))
sinusoida_przycisk.grid(row=1, column=0, pady=(5, 5), padx=10)
prostokat_przycisk = ttk.Button(root, text="PROSTOKATNY", command=lambda: rodzaj_sygnalu_wejsciowego(2))
prostokat_przycisk.grid(row=1, column=1, pady=(5, 5), padx=10)
trojkat_przycisk = ttk.Button(root, text="TROJKATNY", command=lambda: rodzaj_sygnalu_wejsciowego(3))
trojkat_przycisk.grid(row=1, column=2, pady=(5, 5), padx=10)

amplituda_opis = ttk.Label(root, text="AMPLITUDA")
amplituda_opis.grid(row=4, column=0, pady=(20, 5))
amplituda_pole_tektstowe = ttk.Entry(root, style="TEntry")
amplituda_pole_tektstowe.grid(row=5, column=0, pady=(5, 5), padx=10)
amplituda_przycisk_ok = ttk.Button(root, text="OK")
amplituda_przycisk_ok.grid(row=5, column=1, pady=(5, 5), padx=10)

czestotliwosc_opis = ttk.Label(root, text="CZESTOTLIWOSC")
czestotliwosc_opis.grid(row=8, column=0, pady=(20, 5))
czestotliwosc_pole_tektstowe = ttk.Entry(root, style="TEntry")
czestotliwosc_pole_tektstowe.grid(row=9, column=0, pady=(5, 5), padx=10)
czestotliwosc_przycisk_ok = ttk.Button(root, text="OK")
czestotliwosc_przycisk_ok.grid(row=9, column=1, pady=(5, 5), padx=10)

#Faza jest potrzebna? imo nie
faza_opis = ttk.Label(root, text="FAZA")
faza_opis.grid(row=12, column=0, pady=(20, 5))
faza_pole_tektstowe = ttk.Entry(root, style="TEntry")
faza_pole_tektstowe.grid(row=13, column=0, pady=(5, 5), padx=10)
faza_przycisk_ok = ttk.Button(root, text="OK")
faza_przycisk_ok.grid(row=13, column=1, pady=(5, 5), padx=10)



root.mainloop()