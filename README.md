# ExamGenerator: Script en python para generar exámenes aleatorios
![GitHub License](https://img.shields.io/github/license/TiiZss/ExamGenerator)
![GitHub Repo stars](https://img.shields.io/github/stars/TiiZss/ExamGenerator)
![GitHub Downloads (all assets, latest release)](https://img.shields.io/github/downloads/TiiZss/ExamGenerator/latest/total)
![GitHub top language](https://img.shields.io/github/languages/top/TiiZss/ExamGenerator)

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/donate/?business=AC5N3XX2KGY2S&no_recurring=0&item_name=Seguir+con+el+desarrollo+de+la+herramienta&currency_code=EUR)

Este script de Python te permite generar exámenes aleatorios y sus respectivas hojas de respuestas a partir de un archivo de texto con preguntas predefinidas. Es ideal para crear múltiples versiones de un mismo examen con preguntas y opciones barajadas.

## **✨ Características**

* **Carga de Preguntas Flexible:** Lee preguntas, opciones y respuestas de un archivo de texto con un formato sencillo.  
* **Generación de Múltiples Exámenes:** Crea el número de exámenes que necesites.  
* **Selección Aleatoria de Preguntas:** Si el número de preguntas solicitadas es menor que el total disponible, selecciona un subconjunto aleatorio.  
* **Opciones Barajadas:** Las opciones de respuesta para cada pregunta se barajan en cada examen generado.  
* **Generación de Respuestas:** Produce un archivo de respuestas separado para cada examen.  
* **Personalización del Nombre:** Permite añadir un prefijo al nombre de los archivos de examen y respuestas.  
* **Manejo Básico de Errores:** Incluye validaciones para el formato del archivo de preguntas y los argumentos de la línea de comandos.

## **🚀 Uso**

Para ejecutar el script, necesitas tener Python instalado. Luego, utiliza la siguiente sintaxis en tu terminal:
```
eg.py <ruta_del_archivo_de_preguntas.txt> <nombre_base_examen> <numero_total_de_examenes> <numero_de_preguntas_por_examen>
```
**Ejemplo:**
```
eg.py preguntas.txt SOC 30 20
```
Este comando generará 30 exámenes, cada uno con 20 preguntas seleccionadas aleatoriamente del archivo preguntas.txt. 
Los archivos se nombrarán examen_SOC_1.txt, examen_SOC_2.txt, etc., y sus respuestas correspondientes respuestas_examen_SOC_1.txt, etc.

### **Parámetros:**
| Parámetro | Descripción |
| ------ | ------ |
| **<ruta_del_archivo_de_preguntas.txt>**| La ruta al archivo de texto que contiene todas tus preguntas.  
| **<nombre_base_examen>**| Un prefijo para los nombres de los archivos de examen y respuestas (ej., "SOC", "Matematicas", "Final").  
| **<numero_total_de_examenes>**| La cantidad de exámenes que deseas generar.  
| **<numero_de_preguntas_por_examen>**| El número de preguntas que cada examen debe contener. Si es mayor que el total de preguntas disponibles, se usarán todas las preguntas disponibles.

## **📝 Formato del Archivo de Preguntas**

El archivo de preguntas (.txt) debe seguir un formato específico para que el script pueda interpretarlo correctamente. Cada bloque de pregunta/respuesta debe estar separado por una línea en blanco.

1. ¿Cuál es la capital de España?  
A) París  
B) Londres  
C) Madrid  
D) Roma  
ANSWER: C)

2. ¿Cuál es el río más largo del mundo?  
A) Nilo  
B) Amazonas  
C) Yangtsé  
D) Misisipi  
ANSWER: B)

(Y así sucesivamente...)

**Notas importantes sobre el formato:**

* Cada **pregunta** puede comenzar con un número y un punto (ej., 1.) o simplemente ser el texto de la pregunta.  
* Las **opciones** deben comenzar con una letra mayúscula seguida de un paréntesis o un punto y un espacio (ej., A), A.).  
* La **respuesta** debe estar en una línea separada, comenzando con ANSWER: seguido de la letra de la opción correcta y un paréntesis (ej., ANSWER: C)).  
* **Las líneas en blanco son cruciales** para separar bloques de preguntas.

## **📁 Archivos de Salida**

El script generará dos tipos de archivos por cada examen:

* **examen_<nombre_base_examen>_<numero_de_examen>.txt**: Contiene las preguntas con sus opciones barajadas.  
* **respuestas_examen_<nombre_base_examen>_<numero_de_examen>.txt**: Contiene las respuestas correctas para cada pregunta del examen correspondiente.
