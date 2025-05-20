import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image, ImageTk
from uart import Uart
from compiler import compilar
import serial.tools.list_ports

class PipelineGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pipeline MIPS - Visualizador")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Configuración de estilos
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        
        # Variables de estado
        self.uart = None
        self.selected_file = None
        self.compiled_code = []
        self.pipeline_stages = ["IF", "ID", "EX", "MEM", "WB"]
        self.current_pc = 0
        self.cycle_count = 0
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel superior (configuración y controles)
        self.top_panel = ttk.Frame(self.main_frame)
        self.top_panel.pack(fill=tk.X, pady=(0, 10))
        
        # Panel de configuración UART
        self.create_uart_panel()
        
        # Panel de archivo y compilación
        self.create_file_panel()
        
        # Panel de visualización del pipeline
        self.create_pipeline_panel()
        
        # Panel de código y memoria
        self.create_code_memory_panel()
        
        # Panel de registros y estado
        self.create_register_panel()
        
        # Barra de estado
        self.status_bar = ttk.Label(self.main_frame, text="Listo", relief=tk.SUNKEN)
        self.status_bar.pack(fill=tk.X, pady=(5, 0))
    
    def create_uart_panel(self):
        uart_frame = ttk.LabelFrame(self.top_panel, text="Configuración UART")
        uart_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Lista de puertos disponibles
        ports = ["COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7"]
        self.port_var = tk.StringVar(value=ports[0] if ports else "")
        
        ttk.Label(uart_frame, text="Puerto:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.port_combobox = ttk.Combobox(uart_frame, textvariable=self.port_var, values=ports)
        self.port_combobox.grid(row=0, column=1, padx=5, pady=5)
        
        # Baudrate
        self.baudrate_var = tk.StringVar(value="19200")
        ttk.Label(uart_frame, text="Baudrate:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.baudrate_combobox = ttk.Combobox(uart_frame, textvariable=self.baudrate_var, 
                                            values=["9600", "19200", "38400", "57600", "115200"])
        self.baudrate_combobox.grid(row=0, column=3, padx=5, pady=5)
        
        # Botón conectar
        self.connect_btn = ttk.Button(uart_frame, text="Conectar", command=self.connect_uart)
        self.connect_btn.grid(row=0, column=4, padx=5, pady=5)
    
    def create_file_panel(self):
        file_frame = ttk.LabelFrame(self.top_panel, text="Archivo y Compilación")
        file_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Botón seleccionar archivo
        self.select_btn = ttk.Button(file_frame, text="Seleccionar Archivo", command=self.select_file)
        self.select_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Etiqueta de archivo seleccionado
        self.file_label = ttk.Label(file_frame, text="Ningún archivo seleccionado")
        self.file_label.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        # Botón compilar
        self.compile_btn = ttk.Button(file_frame, text="Compilar", command=self.compile_file)
        self.compile_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Botón enviar programa
        self.send_btn = ttk.Button(file_frame, text="Enviar Programa", command=self.send_program)
        self.send_btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    def create_pipeline_panel(self):
        pipeline_frame = ttk.LabelFrame(self.main_frame, text="Visualización del Pipeline")
        pipeline_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Canvas para visualizar el pipeline
        self.pipeline_canvas = tk.Canvas(pipeline_frame, bg='white', height=150)
        self.pipeline_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Dibujar las etapas del pipeline
        self.draw_pipeline_stages()
        
        # Controles de ejecución
        control_frame = ttk.Frame(pipeline_frame)
        control_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.run_btn = ttk.Button(control_frame, text="Ejecución Continua", command=self.run_continuous)
        self.run_btn.pack(side=tk.LEFT, padx=5)
        
        self.step_btn = ttk.Button(control_frame, text="Paso a Paso", command=self.run_step)
        self.step_btn.pack(side=tk.LEFT, padx=5)
        
        self.reset_btn = ttk.Button(control_frame, text="Reiniciar", command=self.reset_simulation)
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Contador de ciclos
        self.cycle_label = ttk.Label(control_frame, text="Ciclo: 0")
        self.cycle_label.pack(side=tk.RIGHT, padx=5)
    
    def draw_pipeline_stages(self):
        width = self.pipeline_canvas.winfo_width()
        height = self.pipeline_canvas.winfo_height()
        
        if width < 10 or height < 10:  # Evitar dibujar si el canvas es muy pequeño
            return
            
        stage_width = width / 5
        padding = 10
        
        self.pipeline_canvas.delete("all")
        
        # Dibujar las etapas del pipeline
        for i, stage in enumerate(self.pipeline_stages):
            x0 = i * stage_width + padding
            x1 = (i + 1) * stage_width - padding
            y0 = padding
            y1 = height - padding
            
            # Dibujar rectángulo de la etapa
            self.pipeline_canvas.create_rectangle(x0, y0, x1, y1, fill='#e0e0e0', outline='black')
            
            # Etiqueta de la etapa
            self.pipeline_canvas.create_text((x0 + x1)/2, y0 + 20, text=stage, font=('Arial', 12, 'bold'))
            
            # Espacio para la instrucción actual
            self.pipeline_canvas.create_text((x0 + x1)/2, (y0 + y1)/2, text="", tags=f"stage_{i}_text", font=('Arial', 10))
        
        # Actualizar el canvas cuando cambie el tamaño
        self.pipeline_canvas.bind("<Configure>", lambda e: self.draw_pipeline_stages())
    
    def create_code_memory_panel(self):
        code_mem_frame = ttk.Frame(self.main_frame)
        code_mem_frame.pack(fill=tk.BOTH, expand=True)
        
        # Panel de código
        code_frame = ttk.LabelFrame(code_mem_frame, text="Código Ensamblador")
        code_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.code_text = tk.Text(code_frame, wrap=tk.NONE, font=('Courier New', 10))
        self.code_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        code_scroll = ttk.Scrollbar(code_frame, orient=tk.VERTICAL, command=self.code_text.yview)
        code_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.code_text.config(yscrollcommand=code_scroll.set)
        
        # Panel de memoria
        mem_frame = ttk.LabelFrame(code_mem_frame, text="Memoria de Datos")
        mem_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.mem_text = tk.Text(mem_frame, wrap=tk.NONE, font=('Courier New', 10))
        self.mem_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        mem_scroll = ttk.Scrollbar(mem_frame, orient=tk.VERTICAL, command=self.mem_text.yview)
        mem_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.mem_text.config(yscrollcommand=mem_scroll.set)
    
    def create_register_panel(self):
        reg_frame = ttk.LabelFrame(self.main_frame, text="Registros y Estado")
        reg_frame.pack(fill=tk.BOTH, pady=(10, 0))
        
        # Panel de registros
        self.reg_text = tk.Text(reg_frame, wrap=tk.NONE, font=('Courier New', 10), height=8)
        self.reg_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        reg_scroll = ttk.Scrollbar(reg_frame, orient=tk.VERTICAL, command=self.reg_text.yview)
        reg_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.reg_text.config(yscrollcommand=reg_scroll.set)
        
        # Panel de PC y estado
        pc_frame = ttk.Frame(reg_frame)
        pc_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        
        ttk.Label(pc_frame, text="Program Counter:", style='Header.TLabel').pack(pady=(5, 0))
        self.pc_label = ttk.Label(pc_frame, text="0x00000000", font=('Courier New', 12))
        self.pc_label.pack()
        
        ttk.Label(pc_frame, text="Estado:", style='Header.TLabel').pack(pady=(10, 0))
        self.state_label = ttk.Label(pc_frame, text="Listo", font=('Arial', 10))
        self.state_label.pack()
    
    def connect_uart(self):
        port = self.port_var.get()
        baudrate = self.baudrate_var.get()
        
        try:
            self.uart = Uart(port, int(baudrate))
            messagebox.showinfo("Conexión Exitosa", f"Conectado a {port} a {baudrate} baudios")
            self.status_bar.config(text=f"Conectado a {port} - {baudrate} baudios")
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar: {str(e)}")
            self.status_bar.config(text="Error de conexión")
    
    def select_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
            initialdir=os.getcwd()
        )
        
        if file_path:
            self.selected_file = file_path
            self.file_label.config(text=os.path.basename(file_path))
            
            # Mostrar el contenido del archivo
            with open(file_path, 'r') as f:
                content = f.read()
                self.code_text.config(state=tk.NORMAL)
                self.code_text.delete(1.0, tk.END)
                self.code_text.insert(tk.END, content)
                self.code_text.config(state=tk.DISABLED)
    
    def compile_file(self):
        if not self.selected_file:
            messagebox.showwarning("Advertencia", "Seleccione un archivo primero")
            return
            
        try:
            self.compiled_code = compilar(self.selected_file)
            messagebox.showinfo("Compilación Exitosa", "El código se compiló correctamente")
            self.status_bar.config(text="Compilación exitosa")
        except Exception as e:
            messagebox.showerror("Error de Compilación", f"Error al compilar: {str(e)}")
            self.status_bar.config(text="Error en compilación")
    
    def send_program(self):
        if not self.uart:
            messagebox.showerror("Error", "No hay conexión UART establecida")
            return
            
        if not self.compiled_code:
            messagebox.showwarning("Advertencia", "Compile el programa primero")
            return
            
        try:
            # Convertir instrucciones a formato de bytes
            n_instructions = len(self.compiled_code)
            n_bytes = [self.split_instruction(self.compiled_code[i]) for i in range(n_instructions)]
            
            # Enviar comando de escritura de programa
            self.uart.send_command(1)
            
            if self.uart.send_file(n_bytes):
                messagebox.showinfo("Éxito", f"Programa enviado - {n_instructions} instrucciones")
                self.status_bar.config(text=f"Programa enviado - {n_instructions} instrucciones")
                self.max_steps = n_instructions + 3
        except Exception as e:
            messagebox.showerror("Error", f"Error al enviar programa: {str(e)}")
            self.status_bar.config(text="Error al enviar programa")
    
    def split_instruction(self, instruction):
        if len(instruction) != 32:
            raise ValueError("La instrucción debe tener 32 bits")
        return [instruction[i:i+8] for i in range(0, 32, 8)]
    
    def run_continuous(self):
        if not self.uart:
            messagebox.showerror("Error", "No hay conexión UART establecida")
            return
            
        self.uart.send_command(2)  # Comando de ejecución continua
        self.update_status()
    
    def run_step(self):
        if not self.uart:
            messagebox.showerror("Error", "No hay conexión UART establecida")
            return
            
        self.uart.send_command(5)  # Comando de paso a paso
        self.cycle_count += 1
        self.cycle_label.config(text=f"Ciclo: {self.cycle_count}")
        self.update_status()
    
    def reset_simulation(self):
        if not self.uart:
            messagebox.showerror("Error", "No hay conexión UART establecida")
            return
            
        self.cycle_count = 0
        self.cycle_label.config(text="Ciclo: 0")
        # Aquí deberías enviar un comando de reinicio al hardware
        # self.uart.send_command(X) donde X es el código de reinicio
        self.update_pipeline_visualization([])
        self.status_bar.config(text="Simulación reiniciada")
    
    def update_status(self):
        if not self.uart:
            return
            
        # Obtener datos del estado actual del pipeline
        PC, BR, MEM = self.uart.receive_all(4, 128, 128)  # Tamaños fijos para PC, registros y memoria
        
        # Actualizar visualizaciones
        self.update_register_view(BR)
        self.update_memory_view(MEM)
        self.update_pc_view(PC)
        
        # Aquí deberías analizar los datos para actualizar la visualización del pipeline
        # Esto es un placeholder - necesitarías implementar la lógica específica
        pipeline_state = self.analyze_pipeline_state(PC, BR, MEM)
        self.update_pipeline_visualization(pipeline_state)
    
    def update_register_view(self, register_data):
        self.reg_text.config(state=tk.NORMAL)
        self.reg_text.delete(1.0, tk.END)
        self.reg_text.insert(tk.END, register_data)
        self.reg_text.config(state=tk.DISABLED)
    
    def update_memory_view(self, memory_data):
        self.mem_text.config(state=tk.NORMAL)
        self.mem_text.delete(1.0, tk.END)
        self.mem_text.insert(tk.END, memory_data)
        self.mem_text.config(state=tk.DISABLED)
    
    def update_pc_view(self, pc_data):
        self.pc_label.config(text=pc_data.split('\t')[1])  # Asume formato "Hex:0x..."
    
    def analyze_pipeline_state(self, pc, registers, memory):
        # Esta función debería analizar los datos recibidos para determinar
        # qué instrucción está en cada etapa del pipeline
        
        # Placeholder - devuelve datos de ejemplo
        return [
            {"stage": "IF", "instr": "lw $t0, 0($sp)", "pc": "0x00400000"},
            {"stage": "ID", "instr": "add $t1, $t0, $zero", "pc": "0x00400004"},
            {"stage": "EX", "instr": "sw $t1, 4($sp)", "pc": "0x00400008"},
            {"stage": "MEM", "instr": "addi $sp, $sp, 8", "pc": "0x0040000C"},
            {"stage": "WB", "instr": "nop", "pc": "0x00000000"}
        ]
    
    def update_pipeline_visualization(self, pipeline_state):
        for i, stage in enumerate(self.pipeline_stages):
            tag = f"stage_{i}_text"
            self.pipeline_canvas.delete(tag)
            
            width = self.pipeline_canvas.winfo_width()
            height = self.pipeline_canvas.winfo_height()
            stage_width = width / 5
            padding = 10
            
            x0 = i * stage_width + padding
            x1 = (i + 1) * stage_width - padding
            y0 = padding
            y1 = height - padding
            
            text = ""
            if pipeline_state and i < len(pipeline_state):
                state = pipeline_state[i]
                text = f"{state['instr']}\nPC: {state['pc']}"
            
            self.pipeline_canvas.create_text((x0 + x1)/2, (y0 + y1)/2, 
                                           text=text, tags=tag, 
                                           font=('Arial', 9), justify=tk.CENTER)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = PipelineGUI()
    gui.run()
