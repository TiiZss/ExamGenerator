#!/usr/bin/env python3
"""Test script para verificar integración Ollama"""
import sys
sys.path.insert(0, '/app')

import qg

print("🧪 Probando Ollama en red Docker interna...\n")

texto = "Python es un lenguaje de programación interpretado de alto nivel."

try:
    preguntas = qg.generate_questions_with_ollama(
        text_content=texto,
        num_questions=2,
        model_name='phi3:mini',
        ollama_url='http://ollama:11434',
        language='español',
        interactive=False
    )
    
    if preguntas:
        print("✅ ÉXITO: Ollama funcionando correctamente")
        print(f"\nPreguntas generadas:\n{preguntas[:300]}...")
    else:
        print("❌ ERROR: No se generaron preguntas")
except Exception as e:
    print(f"❌ ERROR: {e}")
