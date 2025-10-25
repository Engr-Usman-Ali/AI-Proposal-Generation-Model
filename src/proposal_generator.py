# src/proposal_generator.py

from groq import Groq
import json
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_proposal(client_text: str) -> dict:
    """
    Generate structured AI proposal using Groq's LLaMA-3 model.
    """
    prompt = f"""
    You are an expert proposal writer for DevArion Solution.
    Convert this client brief into a structured professional proposal.

    Client Brief:
    {client_text}

    Return in JSON format with these keys:
    - service_type
    - project_overview
    - objectives
    - timeline
    - estimated_budget
    - tone
    - formatted_text (final professional proposal)
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a professional business proposal writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    raw_output = response.choices[0].message.content.strip()

    try:
        proposal_data = json.loads(raw_output)
    except json.JSONDecodeError:
        proposal_data = {
            "service_type": "N/A",
            "project_overview": "N/A",
            "objectives": [],
            "timeline": "N/A",
            "estimated_budget": "N/A",
            "tone": "Professional",
            "formatted_text": raw_output
        }

    return proposal_data
