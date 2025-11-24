import json
from datetime import datetime           # Importerer alle nødvendige biblioteker
from task_manager import Task

def save_tasks_to_file(tasks, filename="tasks.json"):
    '''Lagrer oppgavelisten til en JSON-fil'''
    try:
        if not tasks:
            return True, "Ingen oppgaver å lagre."
        
        tasks_data = []  # Konverterer hver oppgave til en 
        for task in tasks:
            task_dict = {
                "id": task.id,
                "title": task.title,
                "priority": task.priority,
                "complated": task.complated,
                "created_date": task.created_date.isoformat()
            }
            tasks_data.append(task_dict)
        
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(tasks_data, file, ensure_ascii=False, indent=2)  # Skriver ordbøkene til en JSON-fil
            
        return True, f"Oppgaver lagret i {filename}!"
    
    except Exception as e:
        return False, f"Feil ved lagring av oppgaver: {str(e)}"
    
def load_tasks_from_file(filename="tasks.json"):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            tasks_data = json.load(file)  # Leser oppgavedataene fra JSON-filen
    
        tasks = []
        for tasks_data in tasks_data:
            try:
                task=Task(title=tasks_data["title"], priority=tasks_data.get("priority", "Medium"))

                task.id = tasks_data["id"]
                task.complated = tasks_data["complated"]
                task.created_date = datetime.fromisoformat(tasks_data["created_date"])

                tasks.append(task)
            
            except Exception as e:
                print(f"Feil ved lasting av en oppgave: {str(e)}")
                continue
    
        print(f"Lastet {len(tasks)} oppgaver fra {filename}.")
        return tasks
    
    except FileNotFoundError:
        print(f"Filen {filename} ble ikke funnet. Starter med en tom oppgaveliste.")
        return []
    except json.JSONDecodeError:
        print(f"Feil ved lesing av {filename}. Filen kan være korrupt.")
        return []
    except Exception as e:
        print(f"Uventet feil ved lasting av oppgaver: {str(e)}")
        return []
