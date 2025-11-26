<<<<<<< HEAD
import os
import argparse
import google.generativeai as genai
import pypdf
import docx
from pptx import Presentation

def get_api_key():
    """
    Obtiene la clave de API desde una variable de entorno para mayor seguridad.
    """
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("Error: La variable de entorno GOOGLE_API_KEY no está configurada. "
                         "Por favor, configúrala con tu clave de API de Google AI.")
    return api_key

def extract_text_from_pdf(file_path):
    """Extrae texto de un fichero PDF."""
    print(f"📄 Extrayendo texto del PDF: {os.path.basename(file_path)}...")
    try:
        reader = pypdf.PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error al leer el PDF: {e}")
        return None

def extract_text_from_docx(file_path):
    """Extrae texto de un fichero DOCX."""
    print(f"📄 Extrayendo texto del DOCX: {os.path.basename(file_path)}...")
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error al leer el DOCX: {e}")
        return None

def extract_text_from_pptx(file_path):
    """Extrae texto de un fichero PPTX."""
    print(f"📄 Extrayendo texto del PPTX: {os.path.basename(file_path)}...")
    try:
        prs = Presentation(file_path)
        text = ""
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text += shape.text + "\n"
        return text
    except Exception as e:
        print(f"Error al leer el PPTX: {e}")
        return None

def generate_questions(text_content, num_questions=10, language="español"):
    """
    Envía el texto a la IA de Gemini y genera preguntas.
    """
    if not text_content or text_content.strip() == "":
        print("El texto extraído está vacío. No se pueden generar preguntas.")
        return None

    print("\n🧠 Enviando texto a la IA para generar preguntas...")
    
    try:
        genai.configure(api_key=get_api_key())
        
        # Usamos un modelo rápido y eficiente como gemini-1.5-flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Basándote en el siguiente texto, genera exactamente {num_questions} preguntas clave que evalúen la comprensión del contenido.
        Las preguntas deben ser claras, concisas y directamente relacionadas con los temas más importantes del documento.
        Genera las preguntas en {language}.

        Aquí está el texto:
        ---
        {text_content}
        ---
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"\n❌ Error al contactar con la API de Gemini: {e}")
        return None

def main():
    """Función principal para orquestar el proceso."""
    parser = argparse.ArgumentParser(
        description="Genera preguntas sobre un fichero PDF, DOCX o PPTX usando IA."
    )
    parser.add_argument("fichero", help="Ruta al fichero PDF, DOCX o PPTX.")
    parser.add_argument("--num_preguntas", type=int, default=10, help="Número de preguntas a generar.")
    parser.add_argument("--idioma", type=str, default="español", help="Idioma para las preguntas.")
    
    args = parser.parse_args()
    
    file_path = args.fichero
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if not os.path.exists(file_path):
        print(f"❌ Error: El fichero '{file_path}' no existe.")
        return

    extracted_text = ""
    if file_ext == '.pdf':
        extracted_text = extract_text_from_pdf(file_path)
    elif file_ext == '.docx':
        extracted_text = extract_text_from_docx(file_path)
    elif file_ext == '.pptx':
        extracted_text = extract_text_from_pptx(file_path)
    else:
        print(f"❌ Error: Tipo de fichero '{file_ext}' no soportado. Usa PDF, DOCX o PPTX.")
        return

    if extracted_text:
        questions = generate_questions(extracted_text, args.num_preguntas, args.idioma)
        if questions:
            print("\n✅ ¡Aquí tienes las preguntas generadas! ✅")
            print("-" * 40)
            print(questions)
            print("-" * 40)

if __name__ == "__main__":
=======
import os
import argparse
import google.generativeai as genai
import pypdf
import docx
from pptx import Presentation

def get_api_key():
    """
    Obtiene la clave de API desde una variable de entorno para mayor seguridad.
    """
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("Error: La variable de entorno GOOGLE_API_KEY no está configurada. "
                         "Por favor, configúrala con tu clave de API de Google AI.")
    return api_key

def extract_text_from_pdf(file_path):
    """Extrae texto de un fichero PDF."""
    print(f"📄 Extrayendo texto del PDF: {os.path.basename(file_path)}...")
    try:
        reader = pypdf.PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error al leer el PDF: {e}")
        return None

def extract_text_from_docx(file_path):
    """Extrae texto de un fichero DOCX."""
    print(f"📄 Extrayendo texto del DOCX: {os.path.basename(file_path)}...")
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error al leer el DOCX: {e}")
        return None

def extract_text_from_pptx(file_path):
    """Extrae texto de un fichero PPTX."""
    print(f"📄 Extrayendo texto del PPTX: {os.path.basename(file_path)}...")
    try:
        prs = Presentation(file_path)
        text = ""
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text += shape.text + "\n"
        return text
    except Exception as e:
        print(f"Error al leer el PPTX: {e}")
        return None

def generate_questions(text_content, num_questions=10, language="español"):
    """
    Envía el texto a la IA de Gemini y genera preguntas.
    """
    if not text_content or text_content.strip() == "":
        print("El texto extraído está vacío. No se pueden generar preguntas.")
        return None

    print("\n🧠 Enviando texto a la IA para generar preguntas...")
    
    try:
        genai.configure(api_key=get_api_key())
        
        # Usamos un modelo rápido y eficiente como gemini-1.5-flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Basándote en el siguiente texto, genera exactamente {num_questions} preguntas clave que evalúen la comprensión del contenido.
        Las preguntas deben ser claras, concisas y directamente relacionadas con los temas más importantes del documento.
        Genera las preguntas en {language}.

        Aquí está el texto:
        ---
        {text_content}
        ---
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"\n❌ Error al contactar con la API de Gemini: {e}")
        return None

def main():
    """Función principal para orquestar el proceso."""
    parser = argparse.ArgumentParser(
        description="Genera preguntas sobre un fichero PDF, DOCX o PPTX usando IA."
    )
    parser.add_argument("fichero", help="Ruta al fichero PDF, DOCX o PPTX.")
    parser.add_argument("--num_preguntas", type=int, default=10, help="Número de preguntas a generar.")
    parser.add_argument("--idioma", type=str, default="español", help="Idioma para las preguntas.")
    
    args = parser.parse_args()
    
    file_path = args.fichero
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if not os.path.exists(file_path):
        print(f"❌ Error: El fichero '{file_path}' no existe.")
        return

    extracted_text = ""
    if file_ext == '.pdf':
        extracted_text = extract_text_from_pdf(file_path)
    elif file_ext == '.docx':
        extracted_text = extract_text_from_docx(file_path)
    elif file_ext == '.pptx':
        extracted_text = extract_text_from_pptx(file_path)
    else:
        print(f"❌ Error: Tipo de fichero '{file_ext}' no soportado. Usa PDF, DOCX o PPTX.")
        return

    if extracted_text:
        questions = generate_questions(extracted_text, args.num_preguntas, args.idioma)
        if questions:
            print("\n✅ ¡Aquí tienes las preguntas generadas! ✅")
            print("-" * 40)
            print(questions)
            print("-" * 40)

if __name__ == "__main__":
>>>>>>> da6a17fb926a5a85bd4d383ef80408fcec706452
    main()