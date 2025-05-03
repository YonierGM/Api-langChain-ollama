# FastAPI
from fastapi import FastAPI, HTTPException
# Pydantic (para validación de datos)
from pydantic import BaseModel
# Respuestas personalizadas (streaming)
from fastapi.responses import StreamingResponse

# Langchain
from langchain_core.messages import SystemMessage, HumanMessage
# Langchain + Ollama (conector/puente)
from langchain_ollama import ChatOllama

from dotenv import load_dotenv
import os

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()  # Cargar .env

# Configurar el modelo desde el .env
llm = ChatOllama(
    model=os.getenv("MODEL_NAME", "llama3.2:3b"),
    temperature=float(os.getenv("TEMPERATURE", 0.7)),
)

# Request body
class ChatRequest(BaseModel):
    question: str

prompt = """
🍳✨ ¡Conviértete en un chef en casa! 

Genera una lista de recomendaciones sobre recetas ideales para preparar en diferentes ocasiones. Asegúrate de proporcionar descripciones detalladas y relevantes sobre cada receta, incluyendo los ingredientes y el paso a paso. Usa un tono amigable y ameno. **Incluye emojis relacionados con la comida y el contexto** para hacer la experiencia más divertida y visual.

### 🗂️ Contextual Guidance:
- **Tipo de Comida:** Desayunos 🥐, Almuerzos 🍝 y Cenas 🍲.
- **Características:** Recetas fáciles para el día a día y platos especiales para ocasiones importantes 🎉.

### 💡 Few-Shot Prompting:
1. **Desayuno:**  
   - Instrucción: "Recomienda una receta rápida y saludable para el desayuno."
   - Respuesta Esperada: "🍓 Te sugiero preparar un tazón de avena con frutas. Solo necesitas avena, leche (o leche vegetal) 🥛 y tus frutas favoritas 🍌🍎. Cocina la avena hasta que esté suave y agrega las frutas al gusto. ¡Es una receta rápida, nutritiva y deliciosa! 💪"

2. **Cena Especial:**  
   - Instrucción: "Sugiéreme una receta especial para una cena con amigos."
   - Respuesta Esperada: "🍽️ Te recomiendo preparar un filete de salmón a la parrilla con quinoa y espárragos. Sazona el salmón con aceite de oliva, ajo y limón 🐟🍋. Cocina a la parrilla unos minutos y acompaña con quinoa cocida y espárragos al vapor. ¡Es elegante, saludable y delicioso! 🌿"

### ✅ Specific Instructions:
- Asegúrate de que las recetas sean fáciles de seguir para cocineros de todos los niveles 🧑‍🍳.
- Cada receta debe incluir una breve descripción (máx. 100 palabras) sobre:
  - Ingredientes principales 🍅🧄🧀.
  - Pasos clave de preparación 📝.

### 📋 Framing Limitations:
- Proporciona al menos **dos recetas** en tu respuesta.
- Mantén un equilibrio entre recetas rápidas 🍽️ y recetas más elaboradas 🎂.
"""

# Generar respuesta en streaming
def generate_response(question: str):
    messages = [
        SystemMessage(content=prompt),
        HumanMessage(content=question)
    ]
    try:
        #Se llama al modelo en modo stream
        for chunk in llm.stream(messages):
            #porción del texto generado que se va enviando
            yield chunk.content
    except Exception as e:
        yield f"\n Error: {str(e)}"

# Endpoint con streaming
@app.post("/chat")
async def chat_stream(req: ChatRequest):
    return StreamingResponse(generate_response(req.question), media_type="text/plain")