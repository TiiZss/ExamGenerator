# Plantillas DOCX para ExamGenerator

Este directorio contiene plantillas de ejemplo para generar exámenes en formato DOCX.

## Uso de Plantillas

Las plantillas DOCX permiten personalizar el formato de los exámenes con:
- Logos institucionales
- Encabezados personalizados
- Estilos específicos
- Formatos de tabla
- Pie de página

## Placeholders Disponibles

Usa estos placeholders en tu plantilla DOCX y serán reemplazados automáticamente:

| Placeholder | Descripción | Ejemplo |
|------------|-------------|---------|
| `{{EXAM_NUMBER}}` | Número del examen | 1, 2, 3... |
| `{{EXAM_PREFIX}}` | Prefijo del examen | Parcial, Final |
| `{{EXAM_TITLE}}` | Título completo | Parcial 1 |
| `{{DATE}}` | Fecha de generación | 11 de enero de 2026 |
| `{{COURSE}}` | Nombre del curso | Matemáticas |
| `{{NUM_QUESTIONS}}` | Número de preguntas | 10 |
| `{{EXAM_TIME}}` | Tiempo del examen | 10 minutos |
| `{{CONTENT}}` | Contenido del examen | (preguntas) |
| `{{QUESTIONS}}` | Alias de CONTENT | (preguntas) |
| `{{EXAM_CONTENT}}` | Alias de CONTENT | (preguntas) |

## Cómo Crear una Plantilla

1. Crea un documento DOCX en Word
2. Diseña el encabezado, logo y formato deseado
3. Inserta los placeholders donde quieras que aparezca información dinámica
4. En el lugar donde quieras las preguntas, escribe: `{{CONTENT}}`
5. Guarda el archivo como `.docx`

## Ejemplo de Plantilla

```
═══════════════════════════════════════════════════
    UNIVERSIDAD EJEMPLO
    FACULTAD DE CIENCIAS
═══════════════════════════════════════════════════

Examen: {{EXAM_TITLE}}
Fecha: {{DATE}}
Curso: {{COURSE}}
Tiempo: {{EXAM_TIME}}
Preguntas: {{NUM_QUESTIONS}}

───────────────────────────────────────────────────

{{CONTENT}}

───────────────────────────────────────────────────
Firma: ___________________
```

## Plantilla de Ejemplo Incluida

- `plantilla_ejemplo.docx` - Plantilla básica con formato profesional

## Notas

- Los placeholders distinguen entre mayúsculas y minúsculas
- Usa `{{CONTENT}}` para insertar las preguntas del examen
- Las respuestas SIEMPRE se generan en archivos separados
- Puedes usar estilos personalizados que se aplicarán a las preguntas
