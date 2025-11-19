import json
from datetime import datetime           # Importerer alle nødvendige biblioteker
from task_manager import Task

def save_tasks_to_file(tasks, filename="tasks.json"):
    '''Lagrer oppgavelisten til en JSON-fil'''
    try:
        tasks_data = [task.to_dict() for task in tasks]  # Konverterer hver oppgave til en ordbok
        
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(tasks_data, file, ensure_ascii=False, indent=2)  # Skriver ordbøkene til en JSON-fil
            
        return True, "Oppgaver lagret!"
    
    except Exception as e:
        return False, f"Feil ved lagring av oppgaver: {str(e)}"