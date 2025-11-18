#!/usr/bin/env python3

import os
from colors import Ansi
import time 

# Logo
logo = r""" ______     ___     
/_  __/__  / _ \___ 
 / / / _ \/ // / _ \
/_/  \___/____/\___/
"""

# Archivo que almacena las tareas
lista_tareas = 'task_list.txt'

# Función para limpiar la pantalla luego de cada interacción
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

# Opciones principales
def menu_options():
    print(f"{Ansi.CYAN}{logo}{Ansi.RESET}")
    print("1. Añadir una tarea")
    print("2. Completar tarea")
    print("3. Eliminar una tarea")
    print("4. Salir")

# Función para añadir tareas
def add_task():

    while True:

        clear_screen()
        print(f"{Ansi.CYAN}{logo}{Ansi.RESET}")
        print(f"Añadir una tarea")
        
        tarea = input("\nMenú anterior: '!b'\nIntroduzca una nueva tarea: ")
        if tarea.lower() == "!b":
            break

        if tarea:
            with open(lista_tareas, 'a') as archivo:
                archivo.write(f"[ ] {tarea}\n")
            # print(f"\nTarea añadida.")
        else:
            print(f"\nLa tarea no puede estar vacía.")
            input("Pulse ENTER para continuar...")

# Función para completar tareas 
def complete_task():
    while True:

        clear_screen()
        print(f"{Ansi.CYAN}{logo}{Ansi.RESET}")
        print("Marcar una tarea como completada")

        with open(lista_tareas, 'r') as archivo:
            tareas = archivo.readlines()

        print("\nLista de tareas:")
        for idx, tarea in enumerate(tareas, 1):
            print(f"{idx}. {tarea.strip()}")

        seleccion = input("\nMenú anterior: '!b'\nSelecciona la tarea a completar: ")
        if seleccion.lower() == "!b":
            break

        if seleccion.isdigit() and 1 <= int(seleccion) <= len(tareas):
            idx = int(seleccion) -1
            tareas[idx] = tareas[idx].replace("[ ]", "[X]")

            with open(lista_tareas, 'w') as archivo:
                archivo.writelines(tareas)
            print(f"\nTarea completada")
            time.sleep(0.4)
        else:
            print("\nNúmero inválido")
            input("Pulse ENTER para continuar...")

# Función para eliminar tareas 
def delete_task():

    while True:

        clear_screen()
        print(f"{Ansi.CYAN}{logo}{Ansi.RESET}")
        print("Eliminar una tarea")

        try:
            with open(lista_tareas, 'r') as archivo:
                tareas = archivo.readlines()

            if not tareas:
                print(f"\nNo hay tareas para eliminar.")
                input("Pulse ENTER para continuar...")

            print("\nLista de tareas:")
            for idx, tarea in enumerate(tareas, 1):
                print(f"{idx}. {tarea.strip()}")

            seleccion = input("\nMenú anterior: '!b'\nSelecciona la tarea a eliminar: ")
            if seleccion.lower() == "!b":
                break

            if seleccion.isdigit() and 1 <= int(seleccion) <= len(tareas):
                idx = int(seleccion) - 1
                tarea_eliminada = tareas.pop(idx)
                
                with open(lista_tareas, 'w') as archivo:
                    archivo.writelines(tareas)
                print(f"\nTarea eliminada.")
                time.sleep(0.4)
            else:
                print("\nNúmero inválido.")
                input("Pulse ENTER para continuar...")

        except FileNotFoundError:
            print("El archivo de tareas no existe todavía.")
            input("Pulse ENTER para continuar...")

# Menú principal 
def menu():

    while True:

        clear_screen()
        menu_options()
        opcion = input("\nElija una opción: ").strip()

        if opcion == "1":
            add_task()

        elif opcion == "2":
            complete_task()

        elif opcion == "3":
            delete_task()

        elif opcion == "4" or opcion.lower() == "!b":
            print("\n¡Hasta la próxima!")
            break

        else:
            print("\nOpción no válida")
            input("Presione ENTER para continuar...")


if __name__ == "__main__":
    menu()
