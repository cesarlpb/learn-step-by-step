import os
import yaml
from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text
from rich.panel import Panel

def load_tutorial(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

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

def verify_step(step):
    if 'validate' in step:
        for file_path in step['validate']:
            if not os.path.exists(file_path):
                print(f"Verificación fallida: El archivo {file_path} no existe.")
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
    display_ascii_art()

    tutorial = load_tutorial('tutoriales/01.django.yaml')
    step_number = 1
    
    for step in tutorial['steps']:
        while True:
            display_step(step, step_number)
            print("\nOpciones:")
            print("1. Verificar")
            print("2. Siguiente paso")
            print("3. Pista")
            option = input("Selecciona una opción: ")
            
            if option == '1':
                if verify_step(step):
                    break
            elif option == '2':
                break
            elif option == '3':
                if 'command' in step:
                    print(f"Pista: Ejecuta el comando '{step['command']}'")
                elif 'instructions' in step:
                    print(f"Pista: {step['instructions']}")
            else:
                print("Opción no válida, por favor selecciona 1, 2 o 3.")
        
        step_number += 1

if __name__ == "__main__":
    main()
