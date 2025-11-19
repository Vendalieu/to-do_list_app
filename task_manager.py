from datetime import datetime # Programmet må vite dagens dato for å vite når oppgaven ble opprettet, når den ble fullført, fristen osv.

class Task:
    '''Mal for oppretting av oppgaver'''
    def __init__(self, title, priority="Medium"):
        self.id = datetime.now().strftime("%Y%m%d%H%M%S")  # Automatisk generere en unik ID for en oppgave basert på opprettelsesdatoen
        self.title = title # Angivelse av oppgavens navn
        self.priority = priority # Angivelse av oppgavens prioritet (Lav, Medium, Høy). Standard er Medium
        self.complated = False # Angivelse av om oppgaven er ikke fullført
        self.created_date = datetime.now() # Angivelse av opprettelsesdatoen for oppgaven
        
    def toggle_completion(self):
        '''Bytter statusen til oppgaven mellom fullført og ikke fullført'''
        self.complated = not self.complated # "not" operatoren bytter verdien av "self.completed" mellom True og False
        
    def to_dict(self):
        '''Konverterer oppgaveobjektet til en ordbok for enkel lagring som JSON'''
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority,
            "complated": self.complated,
            "created_date": self.created_date.isoformat() # Konverterer datetime-objektet til en  streng
        }
        
class TaskManager:
    '''klasse for å administrere oppgaver'''
    def __init__(self):
        self.tasks = []  # Liste for å lagre oppgaveobjekter
    
    def add_task(self, title, priority="Medium"):
        '''Legger til en ny oppgave i oppgavelisten'''
        try:
            if not title.strip():
                return False, "Oppgavetittelen kan ikke være tom."
            
            new_task = Task(title, priority)
            self.tasks.append(new_task)
            return True, f"Oppgave '{title}' lagt til med prioritet '{priority}'."
        
        except Exception as e:
            return False, f"Feil oppstod: {str(e)}"
            
    def delete_task(self, task_id):
        '''Sletter en oppgave basert på dens ID'''
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                return True, f"Oppgave med ID {task_id} er slettet."
        return False, f"Oppgave med ID {task_id} ikke funnet."
    
    def toggle_completion(self, task_id):
        '''Bytter fullføringsstatusen til en oppgave basert på dens ID'''
        for task in self.tasks:
            if task.id == task_id: # Sjekker om oppgaven med den gitte IDen finnes
                task.toggle_completion()
                status = "fullført" if task.complated else "ikke fullført"
                return True, f"Oppgave med ID {task_id} er nå {status}."
        return False, f"Oppgave med ID {task_id} ikke funnet."
    
    def get_all_tasks(self):
        '''Returnerer en liste over alle oppgaver som ordbøker'''
        return self.tasks
    
    def get_task_by_id(self, task_id):
        '''Henter en oppgave basert på dens ID'''
        for task in self.tasks:
            if task.id == task_id: # Sjekker om oppgaven med den gitte IDen finnes
                return task
        return None