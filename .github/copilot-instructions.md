# ExamGenerator AI Coding Assistant Instructions

## Project Overview
ExamGenerator is a dual-purpose Python CLI tool for generating randomized exams: **eg.py** (main generator with template system) and **qg.py** (AI-powered question generator using Google Gemini).

## Architecture & Core Components

### Main Generator (eg.py)
- **Deterministic Randomization**: Uses `random.seed(f"{exam_prefix}_{exam_number}")` before each exam generation to ensure identical shuffling across TXT and DOCX formats for the same exam
- **Template System**: Supports 15+ placeholders in DOCX templates: `{{EXAM_NUMBER}}`, `{{EXAM_TITLE}}`, `{{DATE}}`, `{{COURSE}}`, `{{NUM_QUESTIONS}}`, `{{EXAM_TIME}}`, `{{CONTENT}}`, etc.
- **Answer Tracking**: Calculates new correct letter after shuffling options by finding the original correct answer text in the shuffled list: `new_correct_letter = option_letters[shuffled_options.index(correct_answer_text)]`
- **Multi-Format Export**: TXT, DOCX, or both simultaneously with transposed answer files (exams as rows, questions as columns)

### AI Generator (qg.py)
- **Multi-Engine Support**: Supports both Google Gemini (cloud) and Ollama (local) AI engines
- **Simple Pipeline**: Extract text (PDF/DOCX/PPTX) → Send to AI → Return questions
- **Security Pattern**: API key via environment variable `GOOGLE_API_KEY` for Gemini, HTTP requests for Ollama
- **Model Selection**: 
  - Gemini: `gemini-1.5-flash` (default), `gemini-1.5-pro`
  - Ollama: `llama2` (default), `mistral`, `codellama`, etc.
- **Local AI**: Ollama runs on `http://localhost:11434` by default, customizable via `--ollama_url`

## Question File Format (preguntas.txt)
Critical parsing rules in `load_questions_from_file()`:
- Questions start with optional number `^\d+\.\s*` (stripped during parsing)
- Options MUST match `^[A-D][).]\s` exactly
- Answer line: `ANSWER: X)` where X is A-D
- **Empty lines delimit questions** - parser adds question when hitting blank line
- No validation for 4 options - parser accepts any number matching the pattern

## Key Development Patterns

### Command Line Arguments
```python
# eg.py: <questions_file> <exam_prefix> <num_exams> <questions_per_exam> [format] [template] [answers_format]
python eg.py preguntas.txt Parcial 3 10 both plantilla.docx xlsx

# qg.py: <file> --num_preguntas N --idioma LANG --motor ENGINE --modelo MODEL
# Google Gemini (cloud)
python qg.py documento.pdf --num_preguntas 15 --idioma español --motor gemini

# Ollama (local AI)
python qg.py documento.pdf --num_preguntas 10 --motor ollama --modelo llama2
```

### Output Organization
- Creates `Examenes_{exam_prefix}/` directory automatically
- Sanitizes folder names: `re.sub(r'[<>:"/\\|?*]', '_', exam_prefix)`
- Generates individual exam files + single consolidated answer file

### DOCX Template Handling
1. Replace placeholders in ALL paragraphs AND table cells using `replace_placeholders()`
2. Find insertion point with markers: `{{CONTENT}}`, `{{QUESTIONS}}`, or `{{EXAM_CONTENT}}`
3. Apply custom styles if they exist (`'Custom Title'`, `'Question'`), fallback to manual formatting
4. Questions and answers always use separate documents

### Time Calculation
Default: 1 minute per question, formatted as "X minutos" or "X hora(s) y Y minutos"

## Critical Git Context
Files show merge conflict markers (`<<<<<<< HEAD`, `=======`, `>>>>>>> da6a17f`) - **always clean these when editing**. Project is active with version 9.20251125.

## Installation & Environment

### Multi-Platform Scripts
- **Windows**: `install.ps1` (handles ExecutionPolicy), PowerShell commands in MAKEFILE won't work
- **Linux/macOS**: `install.sh`, `quick_install.sh`, `setup.sh`, or `make install`
- **Virtual Environment**: Always `.venv` directory, activated before pip installs, `requests>=2.31.0`
- Conditional imports: Check for `openpyxl` before Excel export, `docx` before DOCX generation, `requests` for Ollama
### Dependencies
- **Core**: `python-docx>=1.1.0`, `openpyxl>=3.1.0`
- **AI Features**: `google-generativeai>=0.3.0`, `pypdf>=3.17.0`, `python-pptx>=0.6.23`
- Conditional imports: Check for `openpyxl` before Excel export, `docx` before DOCX generation

## Common Development Tasks

### Adding New Export Formats
1. Add format to `validate_args()` allowed list
2. Implement `create_answers_{format}()` following transposed layout pattern (exams as rows)
3. Update main() conditional logic for format selection

### Adding Template Placeholders
1. Add to `replacements` dict in `replace_placeholders()` with Spanish month names for dates
2. Document in README.md placeholder section
3. Update both paragraph and table cell replacement loops

### Modifying Question Parsing
- Edit regex patterns compiled once at start of `load_questions_from_file()`
- Maintain state machine: `current_question` dict, `options` list, empty line triggers save
- Always raise `ValueError` with line numbers for format errors

### AI Integration Changes
- **Dual Engine Architecture**: Separate functions `generate_questions_with_gemini()` and `generate_questions_with_ollama()`
- **Auto-start Ollama**: `ensure_ollama_running()` checks if Ollama is running and offers to start it automatically
- **Model selection**: Via `--motor` (gemini/ollama) and `--modelo` arguments
- **Ollama specifics**: 
  - Uses REST API (`/api/generate` endpoint) with 5-minute timeout
  - Auto-detection with `check_ollama_running()` before use
  - Auto-start capability via `start_ollama_server()` - prompts user before starting
  - Connection error handling with helpful messages about `ollama serve`
  - Customizable URL via `--ollama_url`
- **Gemini specifics**: Uses `google-generativeai` library with API key validation
- Prompt engineering: Questions must be "claras, concisas y directamente relacionadas"
- Error handling: Print Spanish error messages, gracefully handle API failures

## Testing & Quality

### Manual Testing Commands
```bash
# Basic exam generationwith Gemini (requires API key)
python qg.py documento.pdf --num_preguntas 10

# AI question generation with Ollama (requires Ollama running)
python qg.py documento.pdf --motor ollama --modelo llama2 Test 2 5

# With template and DOCX
python eg.py preguntas.txt Parcial 3 10 docx plantilla.docx

# AI question generation (requires API key)
python qg.py documento.pdf --num_preguntas 10
```

### Make Targets
- `make test`: Verify modules import, check file existence
- `make example`: Runs basic 2-exam, 5-question generation
- `make clean`: Removes `.venv`, `Examenes_*`, `__pycache__`

## Spanish-First Project
All user-facing text, comments, variable names, and error messages are in Spanish. Maintain this convention when adding features. Month names use Spanish: "enero", "febrero", etc.

## Anti-Patterns to Avoid
- ❌ Don't modify randomization seed logic - breaks format consistency
- ❌ Don't add question validation in parser - parser is permissive by design
- ❌ Don't hardcode API keys - always use environment variables
- ❌ Don't break empty-line question delimiter in parser
- ❌ Don't change transposed layout (exams as rows) in answer files without updating all formats
