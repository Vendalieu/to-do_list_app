import json
from datetime import datetime           # Importerer alle nødvendige biblioteker

def save_tasks_to_file(tasks, filename="tasks.json"):
    '''Lagrer oppgavelisten til en JSON-fil'''
    try:
        if not tasks:
            return True, "Ingen oppgaver å lagre."
        
        tasks_data = []  # Konverterer hver oppgave til en 
        for task in tasks:

            tasks_data.append(task.to_dict())  # Bruker to_dict-metoden for å konvertere oppgaven til en ordbok
        
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
                task_dict = {
                    "id": tasks_data["id"],
                    "title": tasks_data["title"],
                    "priority": tasks_data.get("priority", "Medium"),  # Standard til Medium hvis ikke spesifisert
                    "complated": tasks_data["complated"],
                    "created_date": datetime.fromisoformat(tasks_data["created_date"])
                }
                
                tasks.append(task_dict) # Legger til den lastede oppgaven i listen
                            
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

def export_to_txt(tasks, filename="tasks_export.txt"):
    '''Eksporterer oppgavelisten til en tekstfil'''
    
    try:
        if not tasks:
            return True, "Ingen oppgaver å eksportere."
        
        with open(filename, 'w', encoding='utf-8') as file:
            
            # Headliner for the text file
            file.write("=== TASK LIST EXPORT ===\n")
            file.write(f"Export date: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n")
            file.write("=" * 20 + "\n")
            file.write("\n")
            
            #Gruppere oppgaver
            active_tasks = [task for task in tasks if not task.complated]
            completed_tasks = [task for task in tasks if task.complated]
            
            #Skrive aktive oppgaver
            file.write("ACTIVE TASKS:\n")
            file.write("-" * 20 + "\n")
            for i, task in enumerate(active_tasks, 1):
                priority_symbol = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}.get(task.priority, "•")
                file.write(f"{i}. {priority_symbol} {task.title}\n")
            file.write("\n")
            
            #Skrive fullførte oppgaver
            file.write("COMPLETED TASKS:\n")
            file.write("-" * 20 + "\n")
            for i, task in enumerate(completed_tasks, 1):
                file.write(f"{i}. 🍻 {task.title}\n")
            file.write("\n")
            
            #Statistikk
            total_tasks = len(tasks)
            completed_count = len(completed_tasks)
            if total_tasks > 0: # Unngå deling på null
                completion_rate = (completed_count / total_tasks) * 100
                file.write(f"STATISTICS: {completed_count}/{total_tasks} completed ({completion_rate:.1f}%)\n")
            
            # Signature
            file.write("_" * 20 + "\n")
            file.write("Exported by To-Do List App - the best app ever\n")
        
        return True, f"Oppgaver eksportert til {filename}!"
    
    except Exception as e:
        return False, f"Feil ved eksportering av oppgaver: {str(e)}"