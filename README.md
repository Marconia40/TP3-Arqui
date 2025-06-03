# TP3-Arqui - Sistema de Procesamiento MIPS con Pipeline, UART y GUI
## Descripción General

Este proyecto implementa un sistema completo que incluye:

-    Una CPU MIPS con arquitectura pipeline de 5 etapas

-    Un módulo UART para comunicación serial

-    Una unidad de depuración (Debug Unit)

-    Una interfaz gráfica (GUI) para control y visualización

El sistema permite cargar programas en lenguaje ensamblador MIPS, compilarlos, enviarlos a la placa FPGA a través de UART, y monitorear la ejecución en tiempo real.
## Componentes Principales
# 1. Pipeline MIPS

## Implementación de un procesador MIPS de 5 etapas:

-    IF: Fetch de instrucciones

-    ID: Decodificación y lectura de registros

-    EX: Ejecución (ALU)

-    MEM: Acceso a memoria

-    WB: Escritura en registros

## Características:

-    Manejo de hazards (data forwarding, stalls)

-    Memoria de instrucciones y datos separadas

-    Soporte para instrucciones R, I, J y HALT

# 2. Módulo UART

## Implementación de comunicación serial con:

-    Baud rate configurable (por defecto 19200)

-    Protocolo estándar: 1 start bit, 8 data bits, 1 stop bit

-    Soporte para transmisión y recepción

# 3. Debug Unit

## Permite depurar el procesador mediante:

-    Control de ejecución (continuo/paso a paso)

-    Lectura de registros y memoria

-    Programación de la memoria de instrucciones

-    Monitoreo del PC (Program Counter)

# 4. Interfaz Gráfica (GUI)

## Aplicación Python/Tkinter que proporciona:

-    Visualización del estado del pipeline

-    Editor de código ensamblador

-    Visualización de registros y memoria

-    Control de ejecución

-    Configuración de UART

# Requisitos del Sistema
## Hardware

###    Placa FPGA compatible (ej. Xilinx, Altera)

###    Cable USB-UART (ej. FTDI, CP2102)

###    Conexiones adecuadas entre FPGA y PC

## Software

###    Para la FPGA:

-        Herramientas de síntesis (Vivado, Quartus, etc.)

-       Archivos Verilog proporcionados

###    Para la GUI (PC):

Python 3.8+

Bibliotecas requeridas:
-        tkinter
-        pillow (PIL)
-        pyserial
-        numpy

### Instalación con pip:
- bash

    pip install pyserial pillow numpy

### Instalación y Configuración

-    Síntesis para FPGA:

        Agregar todos los archivos Verilog al proyecto

        Asignar pines según la placa utilizada

        Generar el bitstream y programar la FPGA

-    Configuración de la GUI:

        Clonar el repositorio o copiar los archivos Python

        Asegurarse de tener instaladas las dependencias

        Conectar el cable USB-UART a la PC

## Uso de la GUI
### 1. Configuración Inicial

#### Configuración UART

    Seleccionar el puerto COM correcto

    Configurar el baud rate (debe coincidir con la FPGA)

    Hacer clic en "Conectar"

### 2. Carga y Compilación de Programas

#### Carga de archivos

    Seleccionar archivo de código ensamblador (.txt)

    Hacer clic en "Compilar" para generar el código máquina

    Verificar que no hay errores en la compilación

### 3. Envío a la FPGA

    Hacer clic en "Enviar Programa"

    Esperar confirmación de envío exitoso

### 4. Control de Ejecución

#### Control de ejecución

    Ejecución Continua: Ejecuta el programa completo

    Paso a Paso: Ejecuta una instrucción por vez

    Reiniciar: Vuelve al estado inicial

### 5. Visualización

    Pipeline: Muestra las instrucciones en cada etapa

    Registros: Valores actuales de los registros

    Memoria: Contenido de la memoria de datos

    PC: Valor actual del Program Counter

## Comandos de Depuración

La Debug Unit responde a estos comandos por UART:
Comando     |	Valor   |	Descripción
- CMD_WRITE_IM  |	0x01    |	Escribir en memoria de instrucciones
- CMD_SEND_INFO |  	0x02    |    Solicitar estado del procesador
- CMD_STEP_BY_STEP  |	0x03    |	Modo paso a paso
- CMD_CONTINUE  |	0x04    |	Ejecución continua
- CMD_STEP  |	0x05    |	Ejecutar una instrucción