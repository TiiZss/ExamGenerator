# Implementación de Plantillas DOCX en Interfaz Web

**Fecha:** 11 de Enero de 2026  
**Versión:** 12.20260111  
**Feature:** Soporte de plantillas DOCX en generación web

---

## 📋 Resumen de Cambios

Se ha agregado soporte completo para plantillas DOCX personalizadas en la interfaz web de ExamGenerator.

### Archivos Modificados

1. **examgenerator/web/templates/generate_exams.html**
   - Agregado selector de formato con evento onChange
   - Agregado checkbox "Usar plantilla DOCX personalizada"
   - Agregado campo de carga de archivo de plantilla
   - Agregado JavaScript para mostrar/ocultar campos dinámicamente
   - Agregada documentación inline de placeholders

2. **examgenerator/web/app.py**
   - Importado `create_exam_docx` del exporter
   - Agregada lógica para procesar checkbox `use_template`
   - Agregado manejo de archivo `template_file`
   - Agregada validación de plantilla DOCX
   - Agregada generación de exámenes DOCX con plantilla opcional

3. **templates/README.md** (NUEVO)
   - Documentación completa de placeholders
   - Guía de creación de plantillas
   - Ejemplos y mejores prácticas

---

## 🎨 Funcionalidad Implementada

### Interfaz de Usuario

1. **Campo de Formato**
   - Selector con opciones: TXT, DOCX, Ambos
   - Al seleccionar DOCX o Ambos → se muestra sección de plantilla

2. **Sección de Plantilla** (condicional)
   - Checkbox "Usar plantilla DOCX personalizada"
   - Información sobre placeholders disponibles
   - Campo de subida de archivo (solo si checkbox marcado)
   - Ayuda contextual y link a documentación

3. **JavaScript Interactivo**
   ```javascript
   toggleTemplateFields()    // Muestra/oculta sección según formato
   toggleTemplateUpload()    // Muestra/oculta campo de archivo
   ```

### Backend

1. **Procesamiento de Formulario**
   ```python
   use_template = request.form.get('use_template') == 'on'
   template_file = request.files.get('template_file')
   ```

2. **Validación de Plantilla**
   - Verifica extensión .docx
   - Valida tamaño de archivo
   - Guarda temporalmente con nombre seguro

3. **Generación de Exámenes**
   ```python
   if export_format in ['docx', 'both']:
       create_exam_docx(
           exam_prefix, i, exam_questions, 
           output_dir, template_path
       )
   ```

---

## 📝 Placeholders Soportados

Los usuarios pueden usar estos placeholders en sus plantillas:

| Placeholder | Descripción | Ejemplo |
|------------|-------------|---------|
| `{{EXAM_NUMBER}}` | Número del examen | 1 |
| `{{EXAM_PREFIX}}` | Prefijo del examen | Parcial |
| `{{EXAM_TITLE}}` | Título completo | Parcial 1 |
| `{{DATE}}` | Fecha de generación | 11 de enero de 2026 |
| `{{COURSE}}` | Nombre del curso | Matemáticas |
| `{{NUM_QUESTIONS}}` | Número de preguntas | 10 |
| `{{EXAM_TIME}}` | Tiempo del examen | 10 minutos |
| `{{CONTENT}}` | Contenido (preguntas) | (preguntas) |

---

## 🔄 Flujo de Usuario

### Escenario 1: Generar exámenes TXT (sin plantilla)
1. Subir archivo de preguntas
2. Configurar parámetros
3. Seleccionar formato: **TXT**
4. Click "Generar Exámenes"
5. ✅ Descarga ZIP con exámenes TXT

### Escenario 2: Generar exámenes DOCX sin plantilla
1. Subir archivo de preguntas
2. Configurar parámetros
3. Seleccionar formato: **DOCX**
4. → Se muestra sección de plantilla
5. **NO marcar** checkbox "Usar plantilla"
6. Click "Generar Exámenes"
7. ✅ Descarga ZIP con exámenes DOCX (formato estándar)

### Escenario 3: Generar exámenes DOCX con plantilla personalizada
1. Subir archivo de preguntas
2. Configurar parámetros
3. Seleccionar formato: **DOCX**
4. → Se muestra sección de plantilla
5. ✅ **Marcar** checkbox "Usar plantilla"
6. → Se muestra campo de subida
7. Subir archivo plantilla.docx
8. Click "Generar Exámenes"
9. ✅ Descarga ZIP con exámenes DOCX (con tu diseño personalizado)

### Escenario 4: Generar ambos formatos con plantilla
1. Subir archivo de preguntas
2. Seleccionar formato: **Ambos**
3. Marcar "Usar plantilla"
4. Subir plantilla.docx
5. Click "Generar Exámenes"
6. ✅ Descarga ZIP con:
   - Exámenes TXT (formato estándar)
   - Exámenes DOCX (con plantilla personalizada)
   - Archivo de respuestas Excel

---

## 🧪 Testing

### Pruebas Realizadas

1. ✅ Interfaz muestra/oculta campos correctamente
2. ✅ JavaScript funciona al cambiar formato
3. ✅ Checkbox toggle funciona correctamente
4. ✅ Backend recibe y procesa plantilla
5. ✅ Validación de archivo DOCX funciona
6. ✅ Generación con plantilla exitosa
7. ✅ Generación sin plantilla exitosa
8. ✅ Formato "Ambos" funciona correctamente

### Para Probar Manualmente

```bash
# 1. Levantar contenedores
docker-compose up -d

# 2. Acceder a interfaz
http://localhost:5000/generate-exams

# 3. Probar diferentes escenarios:
- TXT sin plantilla
- DOCX sin plantilla
- DOCX con plantilla
- Ambos con plantilla
```

---

## 📊 Mejoras Implementadas

### UX/UI
- ✅ Campos condicionales (solo se muestran cuando son relevantes)
- ✅ Ayuda contextual inline
- ✅ Validación de archivos
- ✅ Mensajes de error claros
- ✅ Diseño responsive

### Funcionalidad
- ✅ Soporte completo de plantillas DOCX
- ✅ Validación de formato de archivo
- ✅ Manejo seguro de archivos (secure_filename)
- ✅ Limpieza automática de archivos temporales
- ✅ Generación simultánea de múltiples formatos

### Documentación
- ✅ README.md con guía completa
- ✅ Ejemplos de placeholders
- ✅ Ayuda inline en formulario
- ✅ Tooltips y hints

---

## 🚀 Próximos Pasos (Opcionales)

### Mejoras Futuras Sugeridas

1. **Plantillas Predefinidas**
   - Crear 3-5 plantillas de ejemplo
   - Selector dropdown de plantillas incluidas
   - Galería visual de plantillas

2. **Vista Previa**
   - Preview de plantilla antes de generar
   - Muestra de cómo quedarán los exámenes

3. **Editor de Plantillas**
   - Editor WYSIWYG para crear plantillas online
   - Arrastrar y soltar placeholders

4. **Validación Avanzada**
   - Verificar que plantilla contenga {{CONTENT}}
   - Advertir si faltan placeholders importantes

5. **Historial de Plantillas**
   - Guardar plantillas usadas recientemente
   - Reutilizar plantillas anteriores

---

## 📝 Notas Técnicas

### Compatibilidad
- ✅ Docker: Funciona en contenedor
- ✅ Windows: Probado en PowerShell
- ✅ Linux/Mac: Compatible (sin probar)

### Dependencias
- `python-docx>=1.1.0` - Manejo de archivos DOCX
- `Flask>=3.0.0` - Framework web
- `werkzeug>=3.0.1` - Utilidades (secure_filename)

### Seguridad
- ✅ Validación de extensiones de archivo
- ✅ Nombres de archivo sanitizados (secure_filename)
- ✅ Validación de tamaño de archivo
- ✅ Archivos temporales con prefijos únicos
- ✅ Sin ejecución de código desde plantillas

---

## 🎯 Resultado Final

La interfaz web ahora permite a los usuarios:
- ✅ Seleccionar formato de exportación (TXT, DOCX, Ambos)
- ✅ Opcionalmente usar plantillas DOCX personalizadas
- ✅ Subir archivos de plantilla con diseños personalizados
- ✅ Generar exámenes con encabezados, logos y formatos institucionales
- ✅ Mantener la simplicidad si no necesitan plantillas

**Feature Status:** ✅ COMPLETADO Y PROBADO

---

**Implementado por:** GitHub Copilot  
**Stack:** ExamGenerator v12.20260111 Docker  
**Servicios:** ExGen-App, ExGen-Web
