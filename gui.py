import tkinter
from tkinter import messagebox, ttk # Importerer alle nødvendige biblioteker
from task_manager import TaskManager

class TodoApp:
    '''Hovedklassen for To-Do List applikasjonen'''
    
    def __init__(self, root):
        self.root = root # Referanse til hovedvinduet
        self.root.title("To-Do List App") # Setter tittelen på vinduet
        self.root.geometry("700x500") # Setter opp størelsen på vinduet
        
        self.task_manager = TaskManager() # Oppretter en instans av TaskManager for å håndtere oppgaver
        self.create_widgets() # Kaller metoden for å lage GUI-komponenter
        self.add_sample_tasks() # Legger til noen eksempeloppgaver ved oppstart
        
    def create_widgets(self):
        '''Oppretter GUI-komponentene'''
        
        input_frame = tkinter.Frame(self.root) # Lager en ramme for inndatafelt og knapp
        input_frame.pack(pady=10)
        
        control_frame = tkinter.Frame(input_frame) # Lager en ramme for kontrollknapper
        control_frame.pack(fill=tkinter.X, pady=5)
        
        list_frame = tkinter.Frame(self.root) # Lager en ramme for oppgavelisten
        list_frame.pack(pady=10, padx=20, fill=tkinter.BOTH, expand=True)
        
        title_label = tkinter.Label(self.root, text="To-Do List", font=("Helvetica", 16, "bold")) # Lager en tittel for app
        title_label.pack(pady=10)
        
        self.task_entry = tkinter.Entry(input_frame, font=("Helvetica", 12)) # Lager et inndatafelt for oppgavetittel 
        self.task_entry.pack(side=tkinter.LEFT, fill=tkinter.X, expand=True)
        self.task_entry.bind("<Return>", lambda event: self.add_task()) # Binder Enter-tasten til å legge til oppgave
        
        self.priority_var = tkinter.StringVar(value="Medium") # Variabel for å holde valgt prioritetet
        priority_combo = ttk.Combobox(control_frame, textvariable=self.priority_var, values=["High", "Medium", "Low"], width=10, state="readonly") # Lager en nedtrekksmeny for prioritet
        priority_combo.pack(side=tkinter.LEFT, padx=(5, 20))
        
        add_button = tkinter.Button(control_frame, text="Add Task", command=self.add_task) # Lager en knapp for å legge til oppgave
        add_button.pack(side=tkinter.LEFT, padx=5)
        
        self.tree = ttk.Treeview(list_frame, columns=("Title", "Priority", "Status"), show="headings", height=15) # Lager en trevisning for å vise oppgavelisten
        
        self.tree.heading("Title", text="Title")
        self.tree.heading("Priority", text="Priority") # Setter overskrifter for kolonnene
        self.tree.heading("Status", text="Status")
        
        
        self.tree.column("Title", width=300)
        self.tree.column("Priority", width=100) # Setter kolonnebredder
        self.tree.column("Status", width=80)
        
        
        
        self.tree.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.tree, orient=tkinter.VERTICAL, command=self.tree.yview) # Lager en rullefelt for trevisningen
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.tree.configure(yscrollcommand=scrollbar.set) # Koble rullefeltet til trevisningen
        
        '''Buttons'''
        complete_button = tkinter.Button(control_frame, text="Toggle Complete", command=self.toggle_task) # Lager en knapp for å bytte fullføringsstatus
        complete_button.pack(side=tkinter.LEFT, padx=10)
        
        delete_button = tkinter.Button(control_frame, text="Delete Task", command=self.delete_task) # Lager en knapp for å slette oppgave
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
        
        priority = self.priority_var.get() # Henter valgt prioritet fra nedtrekksmenyen
        
        success, msg = self.task_manager.add_task(title, priority) # Prøver å legge til oppgaven via TaskManager
        
        if success:
            self.task_entry.delete(0, tkinter.END) # Tømmer inndatafeltet ved suksess
            self.update_task_list() # Oppdaterer oppgavelisten i GUI
            messagebox.showinfo("Success", msg) # Viser suksessmelding
        else:
            messagebox.showerror("Error", msg) # Viser feilmelding hvis noe gikk galt
            
    def get_selected_task(self):
        """Det er en hjelpefunksjon for å hente den valgte oppgaven fra trevisningen"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Error", "Please select a task from the list first!")
            return None
    
        try:
            # Получаем индекс выбранной строки
            selected_index = self.tree.index(selection[0])
        
            # Получаем ВСЕ задачи
            all_tasks = self.task_manager.get_all_tasks()
        
            # Проверяем, что индекс существует
            if 0 <= selected_index < len(all_tasks):
                selected_task = all_tasks[selected_index]
                print(f"DEBUG: Selected task at index {selected_index}: {selected_task.title}")
                return selected_task
            else:
                messagebox.showerror("Error", "Invalid task selection")
                return None
            
        except Exception as e:
            messagebox.showerror("Error", f"Task selection error: {str(e)}")
            return None
        
    def toggle_task(self):
        '''Bytter fullføringsstatusen til den valgte oppgaven'''
        
        task = self.get_selected_task() # Henter den valgte oppgaven
        if task:
            success, msg = self.task_manager.toggle_completion(task.id) # Bytter status via TaskManager
            if success:
                self.update_task_list() # Oppdaterer oppgavelisten i GUI
                messagebox.showinfo("Success", msg) # Viser suksessmelding
            else:
                messagebox.showerror("Error", msg) # Viser feilmelding hvis noe gikk galt
                    
    def delete_task(self):
        '''Sletter den valgte oppgaven'''
        
        task = self.get_selected_task() # Henter den valgte oppgaven
        if task:
            if messagebox.askyesno("Confirm", f"Slett oppgaven '{task.title}'?"): # Bekreftelse fra bruker
                success, msg = self.task_manager.delete_task(task.id) # Sletter oppgaven via TaskManager
                if success:
                    self.update_task_list() # Oppdaterer oppgavelisten i GUI
                    messagebox.showinfo("Success", msg) # Viser suksessmelding
                else:
                    messagebox.showerror("Error", msg) # Viser feilmelding hvis noe gikk galt
            
    def update_task_list(self):
        """Updates the task list displayed in the treeview"""
        # clears the existing items in the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
    
        # adds tasks in order
        for i, task in enumerate(self.task_manager.get_all_tasks()):
            status = "Completed" if task.complated else "Active"
        
            priority_display = {
                "High": "High",
                "Medium": "Medium", 
                "Low": "Low"
            }.get(task.priority, task.priority) 
        
            self.tree.insert("", tkinter.END, values=(
                task.title,
                priority_display,
                status
            )) # Inserts each task into the treeview with its details