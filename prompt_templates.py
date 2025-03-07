# prompt_templates.py

MEETING_PROMPT = """
You are an experienced meeting facilitator. Please generate a detailed meeting agenda and structure.

Context:
- Meeting Type: {meeting_type}
- Description: {description}
- Duration: {duration}
- Format: {include_actions}

Create a professional meeting plan that includes:
1. Meeting objectives and goals
2. Time-boxed agenda items
3. Key discussion points
4. Required preparation
5. Action items and next steps {include_actions}

Guidelines:
- Keep timing realistic for {duration} duration
- Include clear section breaks
- Prioritize important topics
- Add buffer time for discussions

Format your response with clear sections:
---
MEETING AGENDA
Meeting Type: {meeting_type}
Duration: {duration}

Objectives:
[List key meeting objectives]

Agenda:
[Time-boxed agenda items]

Discussion Points:
[Key points to cover]

Preparation Required:
[List any pre-meeting tasks]

Action Items:
[Suggested action items and owners]
---

RESPOND IN THIS FORMAT WITHOUT ANY ADDITIONAL TEXT.
"""