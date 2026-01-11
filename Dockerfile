# ExamGenerator v12 - Dockerfile
# Multi-stage build para optimizar tamaño

# ============================================
# Stage 1: Builder - Instalar dependencias
# ============================================
FROM python:3.11-slim as builder

LABEL maintainer="TiiZss <tiizss@github.com>"
LABEL description="ExamGenerator - Generador avanzado de exámenes aleatorios con IA"
LABEL version="12.20260111"

# Variables de entorno para Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Crear directorio de trabajo
WORKDIR /build

# Copiar archivos de configuración
COPY pyproject.toml .python-version ./
COPY requirements.txt ./

# Instalar dependencias del sistema necesarias para python-docx, reportlab, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Crear venv e instalar dependencias con pip
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# ============================================
# Stage 2: Runtime - Imagen final optimizada
# ============================================
FROM python:3.11-slim AS runtime

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    EXAMGEN_HOME="/app" \
    EXAMGEN_DATA="/data" \
    EXAMGEN_OUTPUT="/output"

# Instalar dependencias del sistema solo para runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libxml2 \
    libxslt1.1 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copiar venv desde builder
COPY --from=builder /opt/venv /opt/venv

# Crear usuario no-root para seguridad
RUN useradd -m -u 1000 -s /bin/bash examgen && \
    mkdir -p /app /data /output && \
    chown -R examgen:examgen /app /data /output

# Cambiar a usuario no-root
USER examgen

# Establecer directorio de trabajo
WORKDIR /app

# Copiar código de la aplicación
COPY --chown=examgen:examgen examgenerator/ ./examgenerator/
COPY --chown=examgen:examgen eg.py cli.py qg.py run_web.py ./
COPY --chown=examgen:examgen config.yaml ./
COPY --chown=examgen:examgen examples/ ./examples/
COPY --chown=examgen:examgen templates/ ./templates/

# Crear directorios para volúmenes
RUN mkdir -p /data/questions /output/exams /app/logs

# Exponer puerto para interfaz web
EXPOSE 5000

# Healthcheck para el contenedor
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Punto de entrada por defecto
ENTRYPOINT ["python"]

# Comando por defecto: mostrar ayuda del CLI
CMD ["cli.py", "--help"]
