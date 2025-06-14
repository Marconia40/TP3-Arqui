import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image, ImageTk
from uart import Uart
from compiler import compilar
import serial.tools.list_ports

# Constantes del protocolo
COMMAND_1 = "Escribir programa"
COMMAND_2 = "Ejecucion continua"
COMMAND_3 = "Step by step"
COMMAND_4 = "Obtener INFO"
COMMAND_5 = "Send step"

commands = {1: COMMAND_1,
            2: COMMAND_2,
            3: COMMAND_3,
            4: COMMAND_4,
            5: COMMAND_5}

mem_data_SIZE = 128  # 128 bytes of depth
REGISTER_BANK_SIZE = 128  # 32 * 4 bytes
PC_SIZE = 4  # 4 bytes
INS_MEM_SIZE = 256  # lineas

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
        self.current_pc = 0
        self.cycle_count = 0
        self.last_command = 0
        self.sent_step = 0
        self.maximum_steps = None
        
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
        
        # Panel de código ensamblador y PC (arriba, más pequeño)
        self.create_code_pc_panel()
        
        # Panel de controles de ejecución
        self.create_execution_controls()
        
        # Panel de registros y memoria (principal)
        self.create_register_memory_panel()
        
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
        
        # Botón obtener info
        self.info_btn = ttk.Button(file_frame, text="Obtener INFO", command=self.obtener_info)
        self.info_btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    def create_code_pc_panel(self):
        """Panel compacto para código ensamblador y PC"""
        code_pc_frame = ttk.LabelFrame(self.main_frame, text="Código Ensamblador y Estado")
        code_pc_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Configurar el frame con dos columnas
        code_pc_frame.grid_columnconfigure(0, weight=3)
        code_pc_frame.grid_columnconfigure(1, weight=1)
        
        # Panel de código (izquierda)
        code_frame = ttk.Frame(code_pc_frame)
        code_frame.grid(row=0, column=0, sticky="nsew", padx=(5, 2))
        
        self.code_text = tk.Text(code_frame, wrap=tk.NONE, font=('Courier New', 9), height=8)
        self.code_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        code_scroll = ttk.Scrollbar(code_frame, orient=tk.VERTICAL, command=self.code_text.yview)
        code_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.code_text.config(yscrollcommand=code_scroll.set)
        
        # Panel de PC y estado (derecha)
        pc_frame = ttk.Frame(code_pc_frame)
        pc_frame.grid(row=0, column=1, sticky="nsew", padx=(2, 5))
        
        ttk.Label(pc_frame, text="Program Counter:", style='Header.TLabel').pack(pady=(5, 0))
        self.pc_label = ttk.Label(pc_frame, text="0x00000000", font=('Courier New', 12))
        self.pc_label.pack(pady=5)
        
        ttk.Label(pc_frame, text="Ciclo:", style='Header.TLabel').pack(pady=(10, 0))
        self.cycle_label = ttk.Label(pc_frame, text="0", font=('Arial', 12))
        self.cycle_label.pack(pady=5)
        
        ttk.Label(pc_frame, text="Estado:", style='Header.TLabel').pack(pady=(10, 0))
        self.state_label = ttk.Label(pc_frame, text="Listo", font=('Arial', 10))
        self.state_label.pack(pady=5)
    
    def create_execution_controls(self):
        """Panel de controles de ejecución"""
        control_frame = ttk.LabelFrame(self.main_frame, text="Controles de Ejecución")
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Botones de control
        self.run_btn = ttk.Button(control_frame, text="Ejecución Continua", command=self.run_continuous)
        self.run_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.step_btn = ttk.Button(control_frame, text="Paso a Paso", command=self.run_step)
        self.step_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.reset_btn = ttk.Button(control_frame, text="Reiniciar", command=self.reset_simulation)
        self.reset_btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    def create_register_memory_panel(self):
        """Panel principal con registros y memoria"""
        reg_mem_frame = ttk.Frame(self.main_frame)
        reg_mem_frame.pack(fill=tk.BOTH, expand=True)
        
        # Panel de registros (izquierda)
        reg_frame = ttk.LabelFrame(reg_mem_frame, text="Registros y Estado")
        reg_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.reg_text = tk.Text(reg_frame, wrap=tk.NONE, font=('Courier New', 10))
        self.reg_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        reg_scroll = ttk.Scrollbar(reg_frame, orient=tk.VERTICAL, command=self.reg_text.yview)
        reg_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.reg_text.config(yscrollcommand=reg_scroll.set)
        
        # Panel de memoria (derecha)
        mem_frame = ttk.LabelFrame(reg_mem_frame, text="Memoria de Datos")
        mem_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.mem_text = tk.Text(mem_frame, wrap=tk.NONE, font=('Courier New', 10))
        self.mem_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        mem_scroll = ttk.Scrollbar(mem_frame, orient=tk.VERTICAL, command=self.mem_text.yview)
        mem_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.mem_text.config(yscrollcommand=mem_scroll.set)
    
    def connect_uart(self):
        port = self.port_var.get()
        baudrate = self.baudrate_var.get()
        
        try:
            self.uart = Uart(port, int(baudrate))
            if self.uart:
                message = f"UART Creada en puerto {port} a {baudrate} baudios"
                messagebox.showinfo("UART Creada", message)
                self.status_bar.config(text=f"Conectado a {port} - {baudrate} baudios")
            else:
                messagebox.showerror("Error", "No se pudo crear la UART.")
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"Error al crear la UART: {str(e)}")
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
        if not self.compiled_code:
            messagebox.showerror("Error", "No se han compilado las instrucciones previamente.")
            return
        
        if not self.uart:
            messagebox.showerror("Error", "No hay conexión UART establecida")
            return
            
        command = 1  # Enviar programa
        self.last_command = command

        # Se convierte el archivo con instrucciones a 'binario'
        n_instructions = len(self.compiled_code)
        n_bytes = [self.split_instruction(self.compiled_code[i]) for i in range(0, n_instructions, 1)]
        
        self.uart.send_command(command)
        if self.uart.send_file(n_bytes):
            success_msg = f"Instrucciones enviadas correctamente. Total de instrucciones: {n_instructions}"
            messagebox.showinfo("Éxito", success_msg)
            self.status_bar.config(text=f"Programa enviado - {n_instructions} instrucciones")
            self.maximum_steps = n_instructions + 3
        print("Sent: ", commands.get(command))
    
    def split_instruction(self, instruction):
        if len(instruction) != 32:
            raise ValueError("La instrucción debe tener 32 bits")
        return [instruction[i:i+8] for i in range(0, 32, 8)]
    
    def run_continuous(self):
        if not self.uart:
            messagebox.showerror("Error", "No hay conexión UART establecida")
            return
            
        command = 2
        self.uart.send_command(command)  # EJECUCION CONTINUA
        self.last_command = command
        print("Sent: ", commands.get(command))
        
        PC, BR, MEM = self.uart.receive_all(PC_SIZE, REGISTER_BANK_SIZE, mem_data_SIZE)
        self.update_register_view(BR)
        self.update_memory_view(MEM)
        self.update_pc_view(PC)
        self.status_bar.config(text="Ejecución continua completada")
    
    def run_step(self):
        if not self.uart:
            messagebox.showerror("Error", "No hay conexión UART establecida")
            return
            
        if self.last_command == 1:  # Escribir programa
            command = 3
            self.uart.send_command(command)  # MODO STEP
            print("Sent: ", commands.get(command))
        
        command = 5
        self.sent_step += 1
        self.uart.send_command(command)  # EJECUCION STEP
        self.last_command = command

        print("Sent: ", commands.get(command))

        PC, BR, MEM = self.uart.receive_all(PC_SIZE, REGISTER_BANK_SIZE, mem_data_SIZE)
        self.update_register_view(BR)
        self.update_memory_view(MEM)
        self.update_pc_view(PC)
        
        self.cycle_count += 1
        self.cycle_label.config(text=f"{self.cycle_count}")
        self.status_bar.config(text=f"Paso {self.sent_step} ejecutado")
    
    def obtener_info(self):
        result = tk.messagebox.askquestion("Advertencia", "No se puede obtener información si ya se envió el programa. ¿Quieres enviar igualmente?")

        if result == 'yes':
            print("Usuario ha elegido Override")

            command = 4
            self.uart.send_command(command)
            print("Sent: ", commands.get(command))

            PC, BR, MEM = self.uart.receive_all(PC_SIZE, REGISTER_BANK_SIZE, mem_data_SIZE)
            self.update_register_view(BR)
            self.update_memory_view(MEM)
            self.update_pc_view(PC)
        else:
            print("Usuario ha optado por no hacer Override")
        return
    
    def reset_simulation(self):
        self.cycle_count = 0
        self.sent_step = 0
        self.cycle_label.config(text="0")
        self.status_bar.config(text="Simulación reiniciada")
    
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
        try:
            # Buscar la línea que contiene el PC en formato hexadecimal
            lines = pc_data.split('\n')
            for line in lines:
                if 'Hex:' in line:
                    self.pc_label.config(text=line.split('Hex:')[1].strip())
                    break
        except:
            self.pc_label.config(text="0x00000000")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = PipelineGUI()
    gui.run()
