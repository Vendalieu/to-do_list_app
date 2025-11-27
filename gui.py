import tkinter
from tkinter import messagebox, ttk # Importerer alle nødvendige biblioteker
from task_manager import TaskManager
from file_handler import load_tasks_from_file, save_tasks_to_file

class TodoApp:
    '''Hovedklassen for To-Do List applikasjonen'''
    
    def __init__(self, root):
        self.root = root # Referanse til hovedvinduet
        self.root.title("To-Do List App") # Setter tittelen på vinduet
        self.root.geometry("550x500") # Setter opp størelsen på vinduet
        
        loaded_tasks_data = load_tasks_from_file() # Laster oppgaver fra fil ved oppstart
        
        self.task_manager = TaskManager(loaded_tasks_data) # Oppretter en TaskManager med de lastede oppgavene
        self.create_widgets() # Kaller metoden for å lage GUI-komponenter
        self.update_task_list() # Oppdaterer oppgavelisten i GUI
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing) # Håndterer vindu-lukk hendelsen
        
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
        add_button = tkinter.Button(control_frame, text="Add Task", command=self.add_task) # Lager en knapp for å legge til oppgave
        add_button.pack(side=tkinter.LEFT, padx=5)
        
        complete_button = tkinter.Button(control_frame, text="Toggle Complete", command=self.toggle_task) # Lager en knapp for å bytte fullføringsstatus
        complete_button.pack(side=tkinter.LEFT, padx=10)
        
        edit_button = tkinter.Button(control_frame, text="Edit", command=self.edit_task) # Lager en knapp for å redigere oppgave
        edit_button.pack(side=tkinter.LEFT, padx=10)
        
        delete_button = tkinter.Button(control_frame, text="Delete", command=self.delete_task) # Lager en knapp for å slette oppgave
        delete_button.pack(side=tkinter.LEFT, padx=10)
        
        save_button = tkinter.Button(control_frame, text="Save", command=self.save_tasks) # Lager en knapp for å lagre oppgaver
        save_button.pack(side=tkinter.LEFT, padx=10)
        
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
            self.save_tasks(silent=True) # Automatisk lagring etter å ha lagt til en oppgave
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
        
    def edit_task(self):
        '''Redigerer den valgte oppgaven'''
        
        task = self.get_selected_task() # Henter den valgte oppgaven
        if task:
            edit_window = tkinter.Toplevel(self.root) # Lager et nytt vindu for redigering
            edit_window.title("Edit Task")
            edit_window.geometry("300x225")
            edit_window.transient(self.root) # Gjør det til et modalt vindu
            edit_window.grab_set() # Fokuserer på det nye vinduet
            
            ttk.Label(edit_window, text="Title:", font=("Arial", 11)).pack(pady=(20, 5))
            
            title_var = tkinter.StringVar(value=task.title)
            title_entry = ttk.Entry(edit_window, textvariable=title_var, font=("Arial", 12), width=40)
            title_entry.pack(pady=5)
            title_entry.select_range(0, tkinter.END)
            title_entry.focus()
            
            ttk.Label(edit_window, text="Priority:", font=("Arial", 11)).pack(pady=(15, 5))
            
            priority_var = tkinter.StringVar(value=task.priority)
            priority_combo = ttk.Combobox(edit_window, textvariable=priority_var, values=["High", "Medium", "Low"], state="readonly", width=15)
            priority_combo.pack(pady=5)
            
            def save_edits():
                new_title = title_var.get().strip()
                if not new_title:
                    messagebox.showwarning("Input Error", "Oppgavetittelen kan ikke være tom.")
                    return
                
                task.title = new_title
                task.priority = priority_var.get()
                self.update_task_list()
                self.save_tasks(silent=True)
                edit_window.destroy()
                messagebox.showinfo("Success", "Oppgaven er oppdatert.")
            
            edit_button_frame = ttk.Frame(edit_window)
            edit_button_frame.pack(pady=20)
                
            save_edit_button = ttk.Button(edit_button_frame, text="Save Changes", command=save_edits)
            save_edit_button.pack()
        
    def toggle_task(self):
        '''Bytter fullføringsstatusen til den valgte oppgaven'''
        
        task = self.get_selected_task() # Henter den valgte oppgaven
        if task:
            success, msg = self.task_manager.toggle_completion(task.id) # Bytter status via TaskManager
            if success:
                self.update_task_list() # Oppdaterer oppgavelisten i GUI
                self.save_tasks(silent=True) # Automatisk lagring etter endring
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
                    self.save_tasks(silent=True) # Automatisk lagring etter sletting
                    messagebox.showinfo("Success", msg) # Viser suksessmelding
                else:
                    messagebox.showerror("Error", msg) # Viser feilmelding hvis noe gikk galt
    
    def save_tasks(self, silent=False):
        '''Lagrer oppgavelisten til fil'''
        
        success, msg = save_tasks_to_file(self.task_manager.tasks) # Lagrer oppgaver via file_handler
        if not silent:
            if success:
                messagebox.showinfo("Success", msg) # Viser suksessmelding
            else:
                messagebox.showerror("Error", msg) # Viser feilmelding hvis noe gikk galt
        else:
            print(msg) # For stille lagring, bare skriv ut meldingen i konsollen
    
    def update_task_list(self):
        """Updates the task list displayed in the treeview"""
        
        # clears the existing items in the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        self.tree.tag_configure('completed', background='#d3d3d3') # Setter bakgrunnsfarge for fullførte oppgaver
        self.tree.tag_configure('low_priority', background='#d0f0c0') # Lys grønn for lav prioritet
        self.tree.tag_configure('medium_priority', background='#fef3bd') # Lys gul for medium prioritet
        self.tree.tag_configure('high_priority', background='#f4c2c2') # Lys rød for høy prioritet
    
        # adds tasks in order
        for i, task in enumerate(self.task_manager.get_all_tasks()):
            status = "Completed" if task.complated else "Active"
        
            priority_display = {
                "High": "High",
                "Medium": "Medium", 
                "Low": "Low"
            }.get(task.priority, task.priority) 
        
            item_values = (
            task.title,
            priority_display,
            status,
            task.created_date
            ) # Setter verdier for hver kolonne
            
            tags = []
            if task.complated:
                tags.append('completed') # Add completed tag
        
            # Add priority tag
            if task.priority == "Low":
                tags.append('low_priority')
            elif task.priority == "Medium":
                tags.append('medium_priority')
            elif task.priority == "High":
                tags.append('high_priority')
        
            # Insert task with all applicable tags
            if tags:
                self.tree.insert("", tkinter.END, values=item_values, tags=tuple(tags))
            else:
                self.tree.insert("", tkinter.END, values=item_values)
                
        
            
    def on_closing(self):
        '''Håndterer vindu-lukk hendelsen'''
        
        self.save_tasks(silent=True) # Automatisk lagring ved lukking
        self.root.destroy() # Lukker vinduet