# ExamGenerator v12 - Dockerfile (UV Optimized)
# Multi-stage build para optimizar tamaño y velocidad

# ============================================
# Stage 1: Builder - Instalar dependencias con UV
# ============================================
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 
ENV UV_LINK_MODE=copy

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar (si las hay)
# python-docx y reportlab pueden necesitarlas
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de definición de dependencias
COPY pyproject.toml uv.lock ./

# Sincronizar dependencias (crea .venv)
# --frozen: usa lockfile sin actualizarlo
# --no-install-project: solo dependencias, no el proyecto en sí todavía
# --no-dev: solo prod
RUN uv sync --frozen --no-install-project --no-dev

# ============================================
# Stage 2: Runtime - Imagen final optimizada
# ============================================
FROM python:3.11-slim-bookworm AS runtime

# Información del mantenedor
LABEL maintainer="TiiZss <tiizss@github.com>"
LABEL version="13.20260114"

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    EXAMGEN_HOME="/app" \
    EXAMGEN_DATA="/data" \
    EXAMGEN_OUTPUT="/output"

# Instalar dependencias del sistema requeridas en runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libxml2 \
    libxslt1.1 \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root
RUN useradd -m -u 1000 -s /bin/bash examgen

# Crear estructura de directorios
WORKDIR /app
RUN mkdir -p /data/questions /output/exams /app/logs && \
    chown -R examgen:examgen /app /data /output

# Copiar entorno virtual desde builder
COPY --from=builder --chown=examgen:examgen /app/.venv /app/.venv

# Copiar código de la aplicación
# (Ordenado por frecuencia de cambio para aprovechar caché)
COPY --chown=examgen:examgen config.yaml ./
COPY --chown=examgen:examgen templates/ ./templates/
COPY --chown=examgen:examgen examples/ ./examples/
COPY --chown=examgen:examgen examgenerator/ ./examgenerator/
COPY --chown=examgen:examgen cli.py ./

# Cambiar a usuario no-root
USER examgen

# Exponer puerto
EXPOSE 5000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Comando por defecto
ENTRYPOINT ["python"]
CMD ["cli.py", "--help"]
