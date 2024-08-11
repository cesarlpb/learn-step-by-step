import os
import json
import yaml
import shutil
from rich.console import Console
from rich.text import Text

PROGRESS_FILE = 'progress.json'

def load_tutorial(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def save_progress(tutorial_file, step_number):
    progress = {
        'tutorial_file': tutorial_file,
        'step_number': step_number
    }
    with open(PROGRESS_FILE, 'w') as file:
        json.dump(progress, file)

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as file:
            return json.load(file)
    return None

def display_ascii_art():
    console = Console()
    ascii_art = """
       _                  _        _                   _             _              _       
      /\ \               /\ \     / /\                /\ \     _    /\ \           /\ \     
     /  \ \____          \ \ \   / /  \              /  \ \   /\_\ /  \ \         /  \ \    
    / /\ \_____\         /\ \_\ / / /\ \            / /\ \ \_/ / // /\ \_\       / /\ \ \   
   / / /\/___  /        / /\/_// / /\ \ \          / / /\ \___/ // / /\/_/      / / /\ \ \  
  / / /   / / /_       / / /  / / /  \ \ \        / / /  \/____// / / ______   / / /  \ \_\ 
 / / /   / / //\ \    / / /  / / /___/ /\ \      / / /    / / // / / /\_____\ / / /   / / / 
/ / /   / / / \ \_\  / / /  / / /_____/ /\ \    / / /    / / // / /  \/____ // / /   / / /  
\ \ \__/ / /  / / /_/ / /  / /_________/\ \ \  / / /    / / // / /_____/ / // / /___/ / /   
 \ \___\/ /  / / /__\/ /  / / /_       __\ \_\/ / /    / / // / /______\/ // / /____\/ /    
  \/_____/   \/_______/   \_\___\     /____/_/\/_/     \/_/ \/___________/ \/_________/                                                                                                 
    """
    
    colors = ["red", "yellow", "green", "cyan", "blue", "magenta"]
    text = Text(ascii_art)
    text.stylize("bold")
    
    for i, line in enumerate(ascii_art.split("\n")):
        color = colors[i % len(colors)]
        console.print(Text(line, style=color))

def display_step(step, step_number):
    print(f"\nPaso {step_number}: {step['step']}")
    if 'command' in step:
        print(f"Ejecuta el siguiente comando:\n{step['command']}")
    elif 'instructions' in step:
        print(f"Instrucciones:\n{step['instructions']}")

def verify_step(step, sandbox_path):
    if 'validate' in step:
        for file_path in step['validate']:
            full_path = os.path.join(sandbox_path, file_path)
            if not os.path.exists(full_path):
                print(f"Verificación fallida: El archivo {full_path} no existe.")
                return False
        if 'validation_script' in step:
            try:
                exec(step['validation_script'])
                print("Verificación exitosa.")
                return True
            except AssertionError as e:
                print(f"Verificación fallida: {str(e)}")
                return False
        print("Verificación exitosa.")
        return True
    else:
        print("No hay pasos de verificación definidos.")
        return True

def main():
    TUTORIALS_PATH = os.getenv('TUTORIALS_PATH', './tutoriales')
    SANDBOX_PATH = os.getenv('SANDBOX_PATH', './sandbox')
    
    display_ascii_art()
    
    progress = load_progress()
    if progress:
        print("Progreso encontrado. ¿Quieres continuar desde donde lo dejaste?")
        print("1. Sí")
        print("2. No, empezar desde el principio")
        choice = input("Selecciona una opción: ")
        if choice == '1':
            tutorial_file = progress['tutorial_file']
            step_number = progress['step_number']
        else:
            tutorial_file = '01.django.yaml'
            step_number = 1
    else:
        tutorial_file = '01.django.yaml'
        step_number = 1

    tutorial_path = os.path.join(TUTORIALS_PATH, tutorial_file)
    tutorial = load_tutorial(tutorial_path)
    tutorial_title = tutorial_file.split('.')[0]
    sandbox_path = os.path.join(SANDBOX_PATH, tutorial_title)

    while step_number <= len(tutorial['steps']):
        step = tutorial['steps'][step_number - 1]
        while True:
            display_step(step, step_number)
            print("\nOpciones:")
            print("1. Verificar")
            print("2. Siguiente paso")
            print("3. Pista")
            print("x. Salir")
            option = input("Selecciona una opción: ")

            if option == '1':
                if verify_step(step, sandbox_path):
                    save_progress(tutorial_file, step_number)
                    break
            elif option == '2':
                save_progress(tutorial_file, step_number)
                break
            elif option == '3':
                if 'command' in step:
                    print(f"Pista: Ejecuta el comando '{step['command']}'")
                elif 'instructions' in step:
                    print(f"Pista: {step['instructions']}")
            elif option == 'x':
                save_progress(tutorial_file, step_number)
                print("Progreso guardado. ¡Hasta la próxima!")
                return
            else:
                print("Opción no válida, por favor selecciona 1, 2, 3 o x.")
        
        step_number += 1

    print("¡Felicidades! Has completado el tutorial.")

    delete_sandbox = input(f"¿Quieres borrar la carpeta de trabajo {sandbox_path}? (y/n): ")
    if delete_sandbox.lower() == 'y':
        shutil.rmtree(sandbox_path)
        print(f"Carpeta {sandbox_path} borrada exitosamente.")

if __name__ == "__main__":
    main()