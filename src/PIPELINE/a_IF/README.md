# ETAPA INSTRUCTION FETCH

Es la primer fase del pipeline. El modulo es el encargado de buscar en memoria la instruccion a ejecutar (en la memoria de instrucciones) y prepararla para su decodificacion. Tambien es el encargado de decidir cual es la direccion de la proxima instruccion a ejecutarse.
La etapa esta compuesta por varios modulos interconectados que permiten el paso fluido de datos hacia la siguiente etapa.

#### Entradas
Seniales de control del PC:
- i_clock : senial de reloj del sistema
- i_pc_en : habilita el contador del programa
- i_pc_reset : reinicia el contador del programa
- i_stall : Si esta en 1 detiene el PC
Seniales de control de memoria:
- i_read_en : Habilita la lectura de la memoria de instrucciones
- i_instrmem_en : Habilita el acceso a memoria de instrucciones
- i_write_en : Habilita la escritura den la memoria de instrucciones
- i_write_data [7:0] : Datos a escribir en memoria (DEBUG)
- i_write_addr [7:0] : Direccion donde se escribe en memoria
Direcciones de control de flujo:
- i_branch_addr [31:0] : Direccion de destino de branch
- i_jump_addr [31:0] : Direccion destino de jump (J y JAL)
- i_last_reg [31:0] : Direccion destino de jump register (JR y JALR)
Seniales de control de flujo:
- i_branch : En 1 si hay un branch, 0 en caso contrario
- i_jal : En 1 si hay jump, 0 si no
- i_jalr : En 1 si hay jump register, 0 si no

#### Salidas
- o_pc [31:0] : Direccion actual del Program Counter
- o_next_pc [31:0] : Direccion del siguiente program counter (PC + 4)
- o_instr [31:0] : Instruccion obtenida desde la memoria

## MODULOS
### program_counter.v (PC)
Es el responsable de mantener la direccion de la instruccion actual y actualizarla para apuntar a la siguiente instruccion en cada ciclo de reloj.

#### Entradas
- i_enable : utilizado para habilitar el modulo
- i_clock : senial de reloj del sistema
- i_reset : Reinicia el contador del programa
- i_pc_stall : Senial de parada que decide si el PC se actualiza o no

#### Salidas
- o_pc : Direccion de la siguiente instruccion a ejecutar

#### Funcionamiento
Si i_enable esta actuvo, la salida o_pc se actualiza con el valor de i_pc_next.

### inst_mem.v
Representa la memoria donde se almacenan las instrucciones del programa.

#### Entradas
- i_address : Direccion de la instruccion a leer
- i_clock : Senial de sincronizacion con el sistema

#### Salidas
- o_instruction : Instruccion leida en la direccion i_address

#### Funcionamiento
Lee la instruccion almacenada en i_address en la memoria ROM y la envia como salida en o_instruction.

### latch.v
Almacena temporalmente la instrucción obtenida de la memoria para enviarla a la siguiente etapa del pipeline.

#### Entradas
- i_reset : Borra el contenido del latch
- i_clock : Sincronizacion con el sistema
- i_enable : Habilita el almacenamiento de datos
- i_data : Instrucción desde la memoria

#### Salidas
- o_data : Instrucción lista para la siguiente etapa

#### Funcionamiento
Cuando i_enable esta activo, o_data almacena el valor de i_data.