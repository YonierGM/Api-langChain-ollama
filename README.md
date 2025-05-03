# 🤖 Api Ollama + LangChain

Esta API está construida con FastAPI y permite interactuar con un modelo de lenguaje (LLM), recibiendo preguntas y devolviendo respuestas generadas en tiempo real.

## 🚀 Tecnologías
- 🐍 Python
- ⚡ FastAPI
- 🧠 LLM local (Ollama)

## 📌 Funcionalidades
- Endpoint POST `/chat` para enviar preguntas y recibir respuestas.
- Streaming de respuestas (respuesta en tiempo real).

## ▶️ Ejecutar localmente

1. Clona el repositorio:

```bash
git clone https://github.com/YonierGM/Api-langChain-ollama.git
cd Api-langChain-ollama

2. Instalar paquetes:

```bash
pip install -r requirements.txt

3. Ejecutar:

```bash
uvicorn main:app --reload  
