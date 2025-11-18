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
            "created_date": self.created_date.strftime("%Y-%m-%d %H:%M:%S")
        }
        
class TaskManager:
    '''klasse for å administrere oppgaver'''