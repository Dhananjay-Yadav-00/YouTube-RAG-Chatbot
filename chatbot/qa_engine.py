from groq import Groq
from config import GROQ_API_KEY
from chatbot.prompts import PROMPTS, SYSTEM_INSTRUCTIONS

client = Groq(api_key=GROQ_API_KEY)

def answer(question, docs, intent):
    context = "\n".join([d.page_content for d in docs])
    prompt = f"""
{SYSTEM_INSTRUCTIONS}

Current Context/Data:
{context}

Specific Task for this query:
{PROMPTS[intent]}

User Question:
{question}

Provide your analysis follow the MANDATORY RESPONSE STRUCTURE:
"""
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.1-8b-instant",
    )
    return chat_completion.choices[0].message.content
