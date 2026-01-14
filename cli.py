#!/usr/bin/env python3
"""
Modern CLI for ExamGenerator using Click.
CLI moderno para ExamGenerator usando Click.
"""

import click
from pathlib import Path

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    class DummyConsole:
        def print(self, *args, **kwargs):
            print(*args)
    console = DummyConsole()


@click.group()
@click.version_option(version="13.20260114", prog_name="ExamGenerator")
def cli():
    """ExamGenerator - Generador avanzado de exámenes aleatorios con IA.
    
    📚 Genera exámenes únicos y personalizados con múltiples formatos de salida.
    """
    pass


@cli.command(name="generate")
@click.argument('questions_file', type=click.Path(exists=True))
@click.argument('exam_prefix', type=str)
@click.argument('num_exams', type=int)
@click.argument('questions_per_exam', type=int)
@click.option('--format', '-f', 'export_format',
              type=click.Choice(['txt', 'docx', 'both'], case_sensitive=False),
              default='txt',
              help='Formato de exportación de exámenes')
@click.option('--template', '-t', type=click.Path(exists=True),
              help='Plantilla DOCX para los exámenes')
@click.option('--answers', '-a',
              type=click.Choice(['txt', 'excel', 'xlsx', 'csv', 'html'], case_sensitive=False),
              default='txt',
              help='Formato para archivo de respuestas')
@click.option('--config', '-c', type=click.Path(exists=True),
              help='Archivo de configuración YAML personalizado')
@click.option('--time-per-question', type=int, default=1,
              help='Minutos por pregunta (por defecto: 1)')
def generate_exams(questions_file, exam_prefix, num_exams, questions_per_exam,
                   export_format, template, answers, config, time_per_question):
    """Generar exámenes desde archivo de preguntas.
    
    QUESTIONS_FILE: Archivo con las preguntas (formato .txt)
    
    EXAM_PREFIX: Prefijo para los exámenes (ej: "Parcial", "Final")
    
    NUM_EXAMS: Cantidad de exámenes a generar
    
    QUESTIONS_PER_EXAM: Número de preguntas por examen
    
    \b
    Ejemplos:
      examgen generate preguntas.txt Parcial 3 10
      examgen generate preguntas.txt Final 5 20 --format both --answers excel
      examgen generate preguntas.txt Parcial 2 15 --template plantilla.docx
    """
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Generando exámenes...", total=None)
            
            # Import here to avoid slow startup
            from examgenerator.core import load_questions_from_file, validate_questions
            from examgenerator.config import config as app_config
            
            # Load custom config if provided
            if config:
                app_config.load_config(config)
            
            # Load questions
            progress.update(task, description="Cargando preguntas...")
            questions = load_questions_from_file(questions_file)
            validate_questions(questions)
            
            console.print(f"✓ Cargadas {len(questions)} preguntas desde [cyan]{questions_file}[/cyan]")
            
            # Generate exams using the original eg.py logic
            progress.update(task, description=f"Generando {num_exams} exámenes...")
            
            # Import and call main generation
            from examgenerator import legacy as eg
            eg.main_generate(
                questions_file=questions_file,
                exam_prefix=exam_prefix,
                num_exams=num_exams,
                num_questions=questions_per_exam,
                export_format=export_format,
                template_path=template,
                answers_format=answers,
                minutes_per_question=time_per_question
            )
        
        # Success message
        console.print()
        console.print(Panel.fit(
            f"[green]✓ ¡Exámenes generados exitosamente![/green]\n\n"
            f"📁 Directorio: [cyan]Examenes_{exam_prefix}[/cyan]\n"
            f"📝 Exámenes: [yellow]{num_exams}[/yellow]\n"
            f"❓ Preguntas por examen: [yellow]{questions_per_exam}[/yellow]\n"
            f"📤 Formato: [yellow]{export_format}[/yellow]\n"
            f"📊 Respuestas: [yellow]{answers}[/yellow]",
            title="Generación Completa",
            border_style="green"
        ))
        
    except Exception as e:
        console.print(f"[red]✗ Error: {str(e)}[/red]")
        raise click.Abort()


@cli.command(name="ai-generate")
@click.argument('document_file', type=click.Path(exists=True))
@click.option('--num-questions', '-n', type=int, default=10,
              help='Número de preguntas a generar')
@click.option('--language', '-l', type=str, default='español',
              help='Idioma para las preguntas')
@click.option('--engine', '-e',
              type=click.Choice(['gemini', 'ollama'], case_sensitive=False),
              default='gemini',
              help='Motor de IA a utilizar')
@click.option('--model', '-m', type=str,
              help='Modelo específico (ej: gemini-1.5-pro, llama2)')
@click.option('--output', '-o', type=click.Path(), default='preguntas_ia.txt',
              help='Archivo de salida para las preguntas')
@click.option('--config', '-c', type=click.Path(exists=True),
              help='Archivo de configuración YAML personalizado')
def ai_generate(document_file, num_questions, language, engine, model, output, config):
    """Generar preguntas con IA desde documentos PDF/DOCX/PPTX.
    
    DOCUMENT_FILE: Archivo fuente (PDF, DOCX o PPTX)
    
    \b
    Ejemplos:
      examgen ai-generate documento.pdf -n 15
      examgen ai-generate presentacion.pptx -n 10 --engine ollama
      examgen ai-generate apuntes.docx -n 20 --model gemini-1.5-pro
    """
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Generando preguntas con IA...", total=None)
            
            # Import here
            from examgenerator.config import config as app_config
            
            # Load custom config if provided
            if config:
                app_config.load_config(config)
            
            # Check engine availability
            if engine == 'gemini':
                import os
                if not os.getenv('GOOGLE_API_KEY'):
                    console.print("[red]✗ Error: GOOGLE_API_KEY no configurada[/red]")
                    console.print("Configura tu API key: export GOOGLE_API_KEY='tu-api-key'")
                    raise click.Abort()
            
            progress.update(task, description=f"Extrayendo texto de {document_file}...")
            
            # Import qg functions
            from examgenerator.ai import (extract_text_from_pdf, extract_text_from_docx, 
                           extract_text_from_pptx, generate_questions_with_gemini, 
                           generate_questions_with_ollama)
            
            # Extract text from document
            file_ext = Path(document_file).suffix.lower()
            text_content = None
            
            if file_ext == '.pdf':
                text_content = extract_text_from_pdf(document_file)
            elif file_ext == '.docx':
                text_content = extract_text_from_docx(document_file)
            elif file_ext == '.pptx':
                text_content = extract_text_from_pptx(document_file)
            else:
                console.print(f"[red]✗ Formato no soportado: {file_ext}[/red]")
                raise click.Abort()
            
            if not text_content:
                console.print("[red]✗ No se pudo extraer texto del documento[/red]")
                raise click.Abort()
            
            # Determine model
            if model is None:
                model = "gemini-1.5-flash" if engine == "gemini" else "llama2"
            
            # Generate questions
            progress.update(task, description=f"Generando preguntas con {engine}...")
            
            questions = None
            if engine == 'gemini':
                questions = generate_questions_with_gemini(
                    text_content, num_questions, language, model)
            else:  # ollama
                questions = generate_questions_with_ollama(
                    text_content, num_questions, language, model, 
                    "http://localhost:11434")
            
            if not questions:
                console.print("[red]✗ No se pudieron generar preguntas[/red]")
                raise click.Abort()
            
            # Save to file
            with open(output, 'w', encoding='utf-8') as f:
                f.write(questions)
        
        # Success message
        console.print()
        console.print(Panel.fit(
            f"[green]✓ ¡Preguntas generadas con IA![/green]\n\n"
            f"📄 Documento: [cyan]{document_file}[/cyan]\n"
            f"🤖 Motor: [yellow]{engine}[/yellow]\n"
            f"❓ Preguntas: [yellow]{num_questions}[/yellow]\n"
            f"🌐 Idioma: [yellow]{language}[/yellow]\n"
            f"💾 Guardadas en: [cyan]{output}[/cyan]",
            title="Generación IA Completa",
            border_style="green"
        ))
        
    except Exception as e:
        console.print(f"[red]✗ Error: {str(e)}[/red]")
        raise click.Abort()


@cli.command(name="config")
@click.option('--show', is_flag=True, help='Mostrar configuración actual')
@click.option('--create', is_flag=True, help='Crear archivo de configuración por defecto')
@click.option('--path', type=click.Path(), default='config.yaml',
              help='Ruta del archivo de configuración')
def manage_config(show, create, path):
    """Gestionar configuración de ExamGenerator.
    
    \b
    Ejemplos:
      examgen config --show
      examgen config --create
      examgen config --create --path mi_config.yaml
    """
    from examgenerator.config import config as app_config
    
    if create:
        app_config.save(path)
        console.print(f"[green]✓ Configuración creada en: {path}[/green]")
        return
    
    if show:
        config_data = app_config.all
        
        table = Table(title="Configuración de ExamGenerator", show_header=True, header_style="bold magenta")
        table.add_column("Sección", style="cyan")
        table.add_column("Configuración", style="yellow")
        table.add_column("Valor", style="green")
        
        for section, settings in config_data.items():
            if isinstance(settings, dict):
                for key, value in settings.items():
                    if isinstance(value, dict):
                        for subkey, subvalue in value.items():
                            table.add_row(f"{section}.{key}", subkey, str(subvalue))
                    else:
                        table.add_row(section, key, str(value))
            else:
                table.add_row(section, "", str(settings))
        
        console.print(table)
        return
    
    console.print("[yellow]Uso: examgen config --show o --create[/yellow]")


@cli.command(name="validate")
@click.argument('questions_file', type=click.Path(exists=True))
def validate(questions_file):
    """Validar formato de archivo de preguntas.
    
    QUESTIONS_FILE: Archivo de preguntas a validar
    
    \b
    Ejemplo:
      examgen validate preguntas.txt
    """
    try:
        from examgenerator.core import load_questions_from_file, validate_questions
        
        console.print(f"Validando [cyan]{questions_file}[/cyan]...")
        
        questions = load_questions_from_file(questions_file)
        validate_questions(questions)
        
        # Show summary
        table = Table(title="Resumen de Preguntas", show_header=True)
        table.add_column("Pregunta #", justify="right", style="cyan")
        table.add_column("Opciones", justify="center", style="yellow")
        table.add_column("Respuesta", justify="center", style="green")
        
        for i, q in enumerate(questions[:10], 1):  # Show first 10
            table.add_row(
                str(i),
                str(len(q.get('options', []))),
                str(q.get('answer', 'N/A'))
            )
        
        if len(questions) > 10:
            table.add_row("...", "...", "...")
        
        console.print(table)
        console.print(f"\n[green]✓ Archivo válido: {len(questions)} preguntas cargadas[/green]")
        
    except Exception as e:
        console.print(f"[red]✗ Error de validación: {str(e)}[/red]")
        raise click.Abort()


@cli.command(name="web")
@click.option('--host', default='127.0.0.1', help='Host para el servidor web')
@click.option('--port', type=int, default=5000, help='Puerto para el servidor web')
@click.option('--debug', is_flag=True, help='Activar modo debug')
def run_web(host, port, debug):
    """Iniciar interfaz web de ExamGenerator.
    
    \b
    Ejemplo:
      examgen web
      examgen web --port 8080 --debug
    """
    console.print(Panel.fit(
        f"[cyan]🌐 Iniciando ExamGenerator Web Interface[/cyan]\n\n"
        f"Host: [yellow]{host}[/yellow]\n"
        f"Puerto: [yellow]{port}[/yellow]\n"
        f"URL: [green]http://{host}:{port}[/green]",
        title="ExamGenerator Web",
        border_style="cyan"
    ))
    
    try:
        from examgenerator import web_runner as run_web
        run_web.run_app(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        console.print("\n[yellow]Servidor detenido[/yellow]")
    except Exception as e:
        console.print(f"[red]✗ Error al iniciar servidor: {str(e)}[/red]")
        raise click.Abort()


@cli.command(name="info")
def show_info():
    """Mostrar información del sistema y configuración."""
    import sys
    from examgenerator.config import config
    
    panel_content = f"""[bold cyan]ExamGenerator v12.20260111[/bold cyan]
    
[yellow]Python:[/yellow] {sys.version.split()[0]}
[yellow]Plataforma:[/yellow] {sys.platform}

[bold]Módulos Disponibles:[/bold]"""
    
    # Check available modules
    modules = {
        'docx': 'Exportación DOCX',
        'openpyxl': 'Exportación Excel',
        'google.generativeai': 'IA Google Gemini',
        'flask': 'Interfaz Web',
        'reportlab': 'Exportación PDF',
        'yaml': 'Configuración YAML',
        'click': 'CLI Moderno',
        'rich': 'Interfaz Enriquecida'
    }
    
    for module, description in modules.items():
        try:
            __import__(module)
            panel_content += f"\n[green]✓[/green] {description}"
        except ImportError:
            panel_content += f"\n[red]✗[/red] {description}"
    
    console.print(Panel(panel_content, title="Información del Sistema", border_style="blue"))


if __name__ == '__main__':
    cli()
