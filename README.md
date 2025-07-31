🧠 Meeting Assistant - README
📝 Overview
The Meeting Assistant is a web application designed to help professionals streamline their meeting planning. It uses powerful language models (via Open WebUI or local Ollama) to generate meeting agendas, discussion topics, and action items tailored to your specific context.

🚀 Features
Generate structured meeting agendas based on your meeting type and goals

Select number of agenda items (1, 3, 5, or 10)

Choose tone (formal, informal, team-building, strategic, etc.)

Include or exclude detailed discussion prompts and action items

Choose between Open WebUI and locally installed Ollama models

Copy results to clipboard with a single click

Responsive UI for both desktop and mobile usage

✅ Prerequisites
Python 3.8+

FastAPI and dependencies

Access to Open WebUI (https://chat.ivislabs.in) and/or local Ollama installation

📦 Installation Steps
Set Up Project Structure

Create the project root folder

Create templates/ and static/ directories for HTML and assets

Install Python Dependencies

bash
Copy
Edit
pip install fastapi uvicorn jinja2 httpx
Configure LLM API

Set API key for Open WebUI (if required)

Ensure Ollama is installed and models are pulled (e.g., gemma:2b, llama3, etc.)

Run the Application

bash
Copy
Edit
uvicorn main:app --reload
Visit http://localhost:8000

🧑‍💻 Using the Application
Step 1: Enter Meeting Details
Provide the meeting type (e.g., sprint planning, client update)

Select how many agenda items you want

Choose a tone (e.g., formal, casual, strategic)

Optionally include detailed discussion points and follow-ups

Select the language model you want to use

Step 2: Generate Agenda
Click "Generate Agenda"

Wait for the model to respond with a custom agenda

The results are shown in a user-friendly format

Step 3: Copy and Use
Use the Copy to Clipboard button to save the output

Share it with your team or paste into calendar invites, documents, etc.

⚙️ How It Works
User Inputs Parameters
User fills the meeting configuration form

LLM Request Triggered

App creates a prompt using form data

Sends to Open WebUI API first

Falls back to local Ollama if necessary

Model Responds with Agenda

The model returns structured content

Includes agenda items, optional talking points and actions

App Displays Results

Response is shown on the frontend

Results are cleanly styled and easy to copy

🛠 Troubleshooting
🌐 API Issues
Ensure Open WebUI is reachable

Verify API key (if used)

Run Ollama locally: ollama serve

⚠️ No Model Found
Run ollama list to check local models

Pull one with ollama pull llama3 or similar

❌ Generation Errors
Use simpler input

Try a different model

Check terminal logs for tracebacks

🎨 Customization
Modify prompt templates to suit internal/team/company formats

Update styling in static/ and templates/ directories

Add support for other LLM APIs (e.g., OpenAI, Cohere, Mistral)

Expand to include summaries or follow-up email generation
