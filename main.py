import numpy as np
import math
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def wykresl():
    # Definicja stałych, parametrów modelu i macierzy
    k = float(pole_k.get())
    a = float(pole_a.get())
    m = float(pole_m.get())
    pA = float(pole_pA.get())

    b0 = pA * k
    b1 = 0
    a0 = pA * k * m
    a1 = a

    A = np.array([[0, 1], [-a0, -a1]])
    B = np.array([[0], [1]])
    C = np.array([b0, b1])
    D = np.array([0])

    # Sprawdzanie stabilności
    s = 0
    if a>0 and pA*m*k>0 :
        s = 1
        stabilnosc.config(text="Układ spełnia warunki stabilności")
    else:
        s = 2
        stabilnosc.config(text="Układ nie spełnia warunków stabilności")

    # Definicja parametrów symulacji
    h = 0.001
    T = 50.0
    czas = T/h
    czas=int(czas)
    L = 2.5
    PI = 3.14159265
    M = 8.0
    w = 2.0 * PI * L / T

    # Generowanie sygnałów wejściowych
    us = [M * math.sin(w * i * h) for i in range(czas)]
    uf = [M if us[i] > 0 else -M for i in range(czas)]
    uskok = [M for i in range(czas)]

    so = selected_option.get()
    if so == "Sygnał prostokątny":
        ukoncowe = uf
    elif so == "Sinusoida":
        ukoncowe = us
    elif so == "Uskok jednoskowy":
        ukoncowe = uskok
    else:
        ukoncowe = uf

    # Zerowe warunki początkowe
    xi_1 = np.zeros((2, 1))
    xi = np.zeros((2, 1))

    # Symulacja modelu
    y = []
    for i in range(czas):
        Ax = np.dot(A, xi_1)
        Bu = np.dot(B, ukoncowe[i])
        xi = Ax + Bu
        xi *= h
        xi += xi_1
        xi_1 = xi
        Cx = np.dot(C, xi)
        Du = np.dot(D, ukoncowe[i])
        print(Cx)
        y.append(Cx + Du)

    czas1 = np.linspace(0, T, czas)

    # czyszczenie poprzednich wykresów
    for widget in ramka_wykresy.winfo_children():
        widget.destroy()
    for widget in ramka_wykresy2.winfo_children():
        widget.destroy()
    # rysowanie wykresu wejścia
    wyk1 = plt.figure(figsize=(5, 4), dpi=100)
    au = wyk1.add_subplot(111)
    au.plot(czas1, ukoncowe, color='red')
    au.set_xlabel('Czas [s]')
    au.set_ylabel('Wartość')
    au.set_title('Wykres funkcji wejścia')
    canvas = FigureCanvasTkAgg(wyk1, master=ramka_wykresy)
    canvas.get_tk_widget().pack()
    canvas.draw()

    # rysowanie wykresu wyjścia
    wyk2 = plt.figure(figsize=(5, 4), dpi=100)
    ax = wyk2.add_subplot(111)
    ax.plot(czas1, y, color='red')
    ax.set_xlabel('Czas [s]')
    ax.set_ylabel('Wartość')
    ax.set_title('Wykres funkcji wyjścia')
    canvas = FigureCanvasTkAgg(wyk2, master=ramka_wykresy2)
    canvas.get_tk_widget().pack()
    canvas.draw()


# utworzenie okna głównego
root = tk.Tk()
root.title('Układ zamknięty z korektorem')
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))  # ustawia na cały ekran
root.wm_state("zoomed")  # ustawia na tryb maksymalizacji

# utworzenie widgetów
etykieta_k = tk.Label(root, text='Parametr k:')
pole_k = tk.Entry(root)
etykieta_a = tk.Label(root, text='Parametr a:')
pole_a = tk.Entry(root)
etykieta_m = tk.Label(root, text='Parametr m:')
pole_m = tk.Entry(root)
etykieta_AA = tk.Label(root, text='Parametr A:')
pole_pA = tk.Entry(root)
ramka_wykresy = tk.Frame(root)
ramka_wykresy2 = tk.Frame(root)

# rozwiajana lista
options = ["Sygnał prostokątny", "Uskok jednoskowy", "Sinusoida"]
selected_option = tk.StringVar(root)
selected_option.set(options[0])

# rozmieszczenie widgetów
etykieta_opcja = tk.Label(root, text='Wybierz rodzaj sygnału:')
etykieta_opcja.grid(row=0, column=0, padx=5, pady=5, sticky='w')
option_menu = tk.OptionMenu(root, selected_option, *options)
option_menu.grid(row=0, column=1, padx=5, pady=5, sticky='w')
option_menu.config(width=20)

etykieta_k = tk.Label(root, text='Parametr k:')
etykieta_k.grid(row=1, column=0, padx=5, pady=5, sticky='w')
pole_k = tk.Entry(root)
pole_k.grid(row=1, column=1, padx=5, pady=5, sticky='w')

etykieta_a = tk.Label(root, text='Parametr a:')
etykieta_a.grid(row=2, column=0, padx=5, pady=5, sticky='w')
pole_a = tk.Entry(root)
pole_a.grid(row=2, column=1, padx=5, pady=5, sticky='w')

etykieta_m = tk.Label(root, text='Parametr m:')
etykieta_m.grid(row=3, column=0, padx=5, pady=5, sticky='w')
pole_m = tk.Entry(root)
pole_m.grid(row=3, column=1, padx=5, pady=5, sticky='w')

etykieta_pA = tk.Label(root, text='Parametr A:')
etykieta_pA.grid(row=4, column=0, padx=5, pady=5, sticky='w')
pole_pA = tk.Entry(root)
pole_pA.grid(row=4, column=1, padx=5, pady=5, sticky='w')

przycisk_wykresl = tk.Button(root, text='Wykreśl', command=wykresl)
przycisk_wykresl.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky='w')

stabilnosc = tk.Label(root, text='')
stabilnosc.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky='w')

ramka_wykresy = tk.Frame(root)
ramka_wykresy.grid(row=7, column=2, columnspan=2, padx=5, pady=5, sticky='w')

ramka_wykresy2 = tk.Frame(root)
ramka_wykresy2.grid(row=7, column=4, columnspan=2, padx=5, pady=5, sticky='w')

root.mainloop()