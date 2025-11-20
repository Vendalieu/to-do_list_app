import tkinter
from tkinter import messagebox, ttk # Importerer alle nødvendige biblioteker
from task_manager import TaskManager

class TodoApp:
    '''Hovedklassen for To-Do List applikasjonen'''
    def __init__(self, root):
        self.root = root # Referanse til hovedvinduet
        self.root.title("To-Do List App") # Setter tittelen på vinduet
        self.root.geometry("500x400") # Setter opp størelsen på vinduet
        
        self.task_manager = TaskManager() # Oppretter en instans av TaskManager for å håndtere oppgaver
        self.create_widgets() # Kaller metoden for å lage GUI-komponenter
        self.add_sample_tasks() # Legger til noen eksempeloppgaver ved oppstart
        
    def create_widgets(self):
        '''Oppretter GUI-komponentene'''
        input_frame = tkinter.Frame(self.root) # Lager en ramme for inndatafelt og knapp
        input_frame.pack(pady=10)
        
        list_frame = tkinter.Frame(self.root) # Lager en ramme for oppgavelisten
        list_frame.pack(pady=10, padx=20, fill=tkinter.BOTH, expand=True)
        
        button_frame = tkinter.Frame(self.root) # Lager en ramme for handlingsknapper
        button_frame.pack(pady=10)
        
        title_label = tkinter.Label(self.root, text="To-Do List", font=("Helvetica", 16, "bold")) # Lager en tittel for app
        title_label.pack(pady=10)
        
        self.task_entry = tkinter.Entry(input_frame, font=("Helvetica", 12)) # Lager et inndatafelt for oppgavetittel 
        self.task_entry.pack(side=tkinter.LEFT, fill=tkinter.X, expand=True)
        self.task_entry.bind("<Return>", lambda event: self.add_task()) # Binder Enter-tasten til å legge til oppgave
        
        self.priority_var = tkinter.StringVar(value="Medium") # Variabel for å holde valgt prioritetet
        priority_combo = ttk.Combobox(input_frame, textvariable=self.priority_var, values=["Low", "Medium", "High"], width=10) # Lager en nedtrekksmeny for prioritet
        priority_combo.pack(side=tkinter.LEFT, padx=(10, 0))
        
        add_button = tkinter.Button(input_frame, text="Add Task", command=self.add_task) # Lager en knapp for å legge til oppgave
        add_button.pack(side=tkinter.LEFT, padx=(10, 0))
        
        self.tree = ttk.Treeview(list_frame, columns=("Status", "Priority", "Title"), show="headings", height=15) # Lager en trevisning for å vise oppgavelisten
        
        self.tree.heading("Status", text="Status")
        self.tree.heading("Priority", text="Priority") # Setter overskrifter for kolonnene
        self.tree.heading("Title", text="Title")
        
        self.tree.column("Status", width=80)
        self.tree.column("Priority", width=100) # Setter kolonnebredder
        self.tree.column("Title", width=300)
        
        self.tree.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview) # Lager en rullefelt for trevisningen
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.tree.configure(yscrollcommand=scrollbar.set) # Koble rullefeltet til trevisningen
        
        '''Buttons'''
        complete_button = tkinter.Button(button_frame, text="Toggle Complete", command=self.toggle_completion) # Lager en knapp for å bytte fullføringsstatus
        complete_button.pack(side=tkinter.LEFT, padx=10)
        
        delete_button = tkinter.Button(button_frame, text="Delete Task", command=self.delete_task) # Lager en knapp for å slette oppgave
        delete_button.pack(side=tkinter.LEFT, padx=10)
        
    def add_sample_tasks(self):
        '''Legger til noen eksempeloppgaver ved oppstart'''
        sample_tasks = [
            ("Buy groceries", "High"),
            ("Walk the dog", "Medium"),
            ("Read a book", "Low")
        ]
        
        for title, priority in sample_tasks:
            self.task_manager.add_task(title, priority)
            
        self.update_task_list() # Oppdaterer oppgavelisten i GUI
        
    def add_task(self):
        '''Legger til en ny oppgave basert på brukerens inndata'''
        title = self.task_entry.get().strip() # Henter og renser oppgavetittelen fra inndatafeltet
        
        if not title:
            messagebox.showwarning("Input Error", "Oppgavetittelen kan ikke være tom.") # Viser advarsel hvis tittelen er tom
            return
        
        success, msg = self.task_manager.add_task(title, self) # Prøver å legge til oppgaven via TaskManager
        
        if success:
            self.task_entry.delete(0, tkinter.END) # Tømmer inndatafeltet ved suksess
            self.update_task_list() # Oppdaterer oppgavelisten i GUI
        else:
            messagebox.showerror("Error", msg) # Viser feilmelding hvis noe gikk galt