import os
from typing import List, Optional
from fastapi import FastAPI, Request, Form, HTTPException # type: ignore
from fastapi.templating import Jinja2Templates # type: ignore
from fastapi.staticfiles import StaticFiles # type: ignore
from fastapi.responses import HTMLResponse # type: ignore
import httpx # type: ignore
from pydantic import BaseModel # type: ignore
import json
from prompt_templates import MEETING_PROMPT

app = FastAPI(title="Meeting Assistant")

# Set up templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuration for open-webui API
WEBUI_ENABLED = True  # Set to use open-webui API
WEBUI_BASE_URL = "https://chat.ivislabs.in/api"
API_KEY = "sk-ce706b683e9d4e4e9032ccad4b3b214e"  # Replace with your actual API key if needed
DEFAULT_MODEL = "gemma2:2b"  # Update to one of the available models

# Fallback to local Ollama API if needed
OLLAMA_ENABLED = True  # Set to False to use only the web UI API
OLLAMA_HOST = "localhost"
OLLAMA_PORT = "11434"
OLLAMA_API_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api"

class MeetingRequest(BaseModel):
    meeting_type: str
    description: str
    duration: str = "30min"
    generate_actions: bool = True

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate_meeting_content(
    meeting_type: str = Form(...),
    description: str = Form(...),
    duration: str = Form("30min"),
    generate_actions: bool = Form(True),
    model: str = Form(DEFAULT_MODEL)
):
    try:
        # Build the prompt using the template
        prompt = MEETING_PROMPT.format(
            meeting_type=meeting_type,
            description=description,
            duration=duration,
            include_actions="with action items" if generate_actions else "without action items"
        )
        
        # Try using the open-webui API first if enabled
        if WEBUI_ENABLED:
            try:
                messages = [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
                
                request_payload = {
                    "model": model,
                    "messages": messages
                }
                print(f"Attempting open-webui API with payload: {json.dumps(request_payload)}")
                
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{WEBUI_BASE_URL}/chat/completions",
                        headers={
                            "Authorization": f"Bearer {API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json=request_payload,
                        timeout=60.0
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        generated_text = ""
                        
                        if "choices" in result and len(result["choices"]) > 0:
                            choice = result["choices"][0]
                            if "message" in choice and "content" in choice["message"]:
                                generated_text = choice["message"]["content"]
                            elif "text" in choice:
                                generated_text = choice["text"]
                        elif "response" in result:
                            generated_text = result["response"]
                        
                        if generated_text:
                            return {"response": generated_text}
            except Exception as e:
                print(f"Open-webui API attempt failed: {str(e)}")
        
        # Fallback to Ollama if needed
        if OLLAMA_ENABLED:
            print("Falling back to direct Ollama API")
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{OLLAMA_API_URL}/generate",
                    json={
                        "model": model,
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=60.0
                )
                
                if response.status_code != 200:
                    raise HTTPException(status_code=500, detail="Failed to generate content from Ollama API")
                
                result = response.json()
                generated_text = result.get("response", "")
                
                return {"response": generated_text}
                
        raise HTTPException(status_code=500, detail="Failed to generate content from any available LLM API")
            
    except Exception as e:
        import traceback
        print(f"Error in meeting content generation: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error in meeting content generation: {str(e)}")

@app.post("/summarize")
async def summarize_transcript(
    transcript: str = Form(...),
    model: str = Form(DEFAULT_MODEL)
):
    try:
        # Create a prompt for transcript summarization
        prompt = f"""
        Please analyze this meeting transcript and:
        1. Extract key discussion points
        2. List all action items with assignees if mentioned
        3. Highlight any important decisions made
        4. Note any follow-up meetings or deadlines

        Transcript:
        {transcript}

        Format the response with clear sections:
        ---
        Key Points:
        [List key points discussed]

        Action Items:
        [List actions with assignees]

        Decisions:
        [List key decisions]

        Follow-ups:
        [List follow-up items and deadlines]
        ---
        """

        if WEBUI_ENABLED:
            # ...existing API call code structure...
            messages = [{"role": "user", "content": prompt}]
            # ...rest of the API calling logic remains same as generate_meeting_content...
            pass

        if OLLAMA_ENABLED:
            # ...existing Ollama fallback code structure...
            pass

    except Exception as e:
        print(f"Error in transcript summarization: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in transcript summarization: {str(e)}")

@app.get("/models")
async def get_models():
    try:
        if WEBUI_ENABLED:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        f"{WEBUI_BASE_URL}/models",
                        headers={
                            "Authorization": f"Bearer {API_KEY}"
                        }
                    )
                    
                    if response.status_code == 200:
                        models_data = response.json()
                        
                        if "data" in models_data and isinstance(models_data["data"], list):
                            model_names = []
                            for model in models_data["data"]:
                                if "id" in model:
                                    model_names.append(model["id"])
                            
                            if model_names:
                                return {"models": model_names}
            except Exception as e:
                print(f"Error fetching models from open-webui API: {str(e)}")
        
        if OLLAMA_ENABLED:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{OLLAMA_API_URL}/tags")
                    if response.status_code == 200:
                        models = response.json().get("models", [])
                        model_names = [model.get("name") for model in models]
                        return {"models": model_names}
            except Exception as e:
                print(f"Error fetching models from Ollama: {str(e)}")
        
        fallback_models = [DEFAULT_MODEL, "gemma2:2b", "qwen2.5:0.5b", "deepseek-r1:1.5b", "deepseek-coder:latest"]
        return {"models": fallback_models}
    except Exception as e:
        print(f"Unexpected error in get_models: {str(e)}")
        return {"models": [DEFAULT_MODEL]}

if __name__ == "__main__":
    import uvicorn # type: ignore
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)