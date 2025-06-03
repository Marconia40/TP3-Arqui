# DEBUG UNIT
El módulo debug_unit.v es una unidad de depuración (debug) que actúa como interfaz entre un sistema de procesamiento (pipeline) y una UART, permitiendo controlar y monitorear el sistema durante su ejecución.

## 🔹 Propósito General
Este módulo permite:
- Cargar instrucciones en la memoria de instrucciones (IM) vía UART
- Controlar la ejecución del pipeline (ejecución paso a paso, continua, etc.)
- Leer y enviar datos del sistema (PC, memoria de datos, banco de registros) para depuración

## 🔹 Parámetros Principales
    NB_STATE    = 10,      // Bits para estados FSM
    NB_DATA     = 8,       // Ancho de datos (bytes)
    NB_ADDR     = 32,      // Ancho de direcciones
    NB_ADDR_RB  = 5,       // Bits para direccionar banco de registros (2^5=32 registros)
    NB_BYTE_CTR = 2,       // Contador de bytes (4 bytes por palabra)
    NB_ADDR_DM  = 5,       // Bits para direccionar memoria de datos
    DM_DEPTH    = 32,      // Profundidad memoria de datos
    RB_DEPTH    = 32,      // Número de registros
    NB_PC_CTR   = 2;       // Contador para bytes del PC

## 🔹 Interfaces Principales
### Entradas:
- Control: i_clock, i_reset, i_halt (señal de parada del pipeline)
- UART: i_rx_done, i_tx_done, i_rx_data (comunicación serial)
- Datos del sistema: i_pc_value, i_mem_data, i_bank_reg_data

### Salidas:
- Control de memoria: enables y señales de lectura/escritura para IM y DM
- Control de banco de registros: enables y direcciones
- UART: o_tx_data, o_tx_start para transmisión
- Control general: o_pipeline_enable, o_state (estado actual)

# 🔹 Máquina de Estados Finitos
La unidad implementa una maquina finita con los siguientes estados (definidos en parameters.vh):

**INITIAL**: Estado inicial, espera comandos por UART

**WRITE_IM**: Escribe instrucciones en la memoria de instrucciones

**READY**: Sistema listo para ejecución

**START**: Ejecución continua del pipeline

**STEP_BY_STEP**: Modo paso a paso

**SEND_PC**: Envía valor del PC por UART

**READ_BR/SEND_BR**: Lee y envía valores del banco de registros

**READ_MEM/SEND_MEM**: Lee y envía valores de la memoria de datos

## 🔹 Funcionamiento Detallado
1. Escritura de Instrucciones (WRITE_IM)
    
    a.   Cuando se recibe el comando CMD_WRITE_IM por UART:
        i.   Habilita escritura en IM (im_write_enable = 1)
        ii.   Usa im_count como dirección y i_rx_data como dato
        iii.   Después de escribir 254 instrucciones, vuelve a READY

2. Control de Ejecución
    
    a.  Ejecución continua (START):
        i.  Habilita todos los módulos (IM, DM, banco de registros, PC)
        ii.  Permite que el pipeline ejecute hasta i_halt

    b.  Paso a paso (STEP_BY_STEP):
        i.  Espera comando CMD_STEP para ejecutar una instrucción
        ii. Después de cada paso, envía estado actual (SEND_PC, SEND_MEM, SEND_BR)

3. Envío de Datos para Depuración
    
    a. PC (SEND_PC):
        i.  Envía los 4 bytes del PC secuencialmente por UART
        ii. Usa count_pc para seleccionar qué byte enviar

    b.  Memoria de Datos (READ_MEM/SEND_MEM):
        i.  Lee toda la memoria (32 palabras) y envía cada byte
        ii. count_mem_data_tx_done es la dirección, count_mem_byte selecciona el byte

    c.  Banco de Registros (READ_BR/SEND_BR):
        i.  Similar a memoria, pero para los 32 registros

## 🔹 Registros y Controles Internos
-   Registros de estado: state, prev_state (guarda estado anterior)
-   Contadores:
    1.  im_count: Dirección para escribir en IM
    2.  count_mem_data_tx_done: Dirección memoria de datos
    3.  count_bank_reg_tx_done: Dirección banco de registros
    4.  count_pc, count_mem_byte, count_bank_reg_byte: Para seleccionar bytes

## 🔹 Flujo de Datos
**Recepción UART →** i_rx_done activa transiciones de estado

**Procesamiento →** Según estado actual y comandos recibidos

**Transmisión UART →** tx_start inicia envío de datos depurados

## 🔹 Consideraciones de Diseño
- **Sincronización**: Todos los cambios ocurren en flanco negativo de reloj (negedge i_clock)
- **Reset**: Limpia todos los registros y contadores
- **Modo Debug**: Cuando se está enviando datos (SEND_*), deshabilita el pipeline