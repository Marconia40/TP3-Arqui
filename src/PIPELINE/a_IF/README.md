# INSTRUCTION FETCH

Este modulo se encarga de buscar la siguiente instruccion a ejecutar desde la memoria de instrucciones y tambien se encarga de determinar cual sera la direccion de la siguiente instruccion.

### Parametros
- PC_SIZE: Tamanio de la direccion del contador del programa
- INST_SIZE: Tamanio de las instrucciones
- INSTMEM_SIZE: Tamanio de la memoria de instrucciones
- MEM_SIZE: Tamanio de los datos de la memoria

### Entradas
- i_clock: senial de reloj
- i_branch, i_jal, i_jalr: Seniales de operaciones de branch o salto.
- i_pc_en: Habilita el program counter
- i_pc_reset: Resetea el program counter
- i_read_en: Habilita la lectura de la memoria de instrucciones
- i_instmem_en: Habilita la memoria de instrucciones
- i_write_en: Habilita la escritura en memoria de instrucciones
- i_write_data, i_write_addr: Dato y direccion a escribir en memoria
- i_branch_addr, i_jump_addr, i_last_reg: Direcciones que se utilizan para determinar la proxima instruccion cuando ocurre un salto o branch
- i_stall: Senial STALL para detener el contador del programa en conflictos

### Salidas
- o_pc: Direccion del contador de programa
- o_next_pc: Direccion de la siguiente instruccion (PC+4)
- o_instr: Instruccion recuperada de la memoria de instrucciones

## program_counter.v

Este es un submodulo que utiliza esta etapa, el cual es un contador de programa que almacena la direccion de la siguiente instruccion a utilizar.

### Entradas
- i_enable: habilita el modulo
- i_clock: Senial de reloj que controla el modulo
- i_reset: Resetea el PC
- i_mux_pc: Se utiliza para actualizar el PC.
- i_pc_stall: senial que detiene el PC.

### Salida
- o_pc: direccion de la siguiente instruccion

## inst_mem.v

Este submodulo implementa la memoria de instrucciones

### Parametros
- MEM_SIZE: Tamanio de los datos en memoria
- MEM_LARGE: Tamanio de la memoria
- ADDR_SIZE: Tamanio de la direccion en memoria
- ADDR_RW: Tamanio de la direccion de lectura/escritura
- INST_SIZE: Tamanio de las instrucciones

### Entradas
- i_clock: senial de reloj que controla el modulo
- i_read_en: Habilita la lectura
- i_write_en: Habilita la escritura
- i_write_data, i_write_addr: Dato y Direccion donde escribir en memoria
- i_read_addr: Direccion donde se lee la instruccion

### Salidas
- o_read_data: dato leido desde la memoria de instrucciones

## catch.v

Este submodulo se encargara de retener el valor de la siguiente instruccion (PC+4)

### Entradas
- i_clock: senial de reloj que controla el modulo
- i_next_pc: direccion proveniente del adder (PC+4)

### Salidas
- o_next_pc: PC = 4

