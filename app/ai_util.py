import base64
import os
from google import genai
from google.genai import types

#from key import API_KEY
from models import User

'''def test_ai():
    client = genai.Client(api_key=API_KEY)
    chat = client.chats.create(model="gemini-2.0-flash")
    response = chat.send_message_stream("I have 2 dogs in my house.")
    for chunk in response:
        print(chunk.text, end="")
    response = chat.send_message_stream("How many paws are in my house?")
    for chunk in response:
        print(chunk.text, end="")
    for message in chat._curated_history:
        print(f'role - ', message.role, end=": ")
        print(message.parts[0].text)'''
import random
def genrate_rating_chemo(user:User):
    return random.random() * 100
    '''def get_urgency_score(patient: PatientData) -> float:
    """Send patient data to Gemini AI and get urgency score."""
    model = genai.GenerativeModel("gemini-pro")  # Use Gemini Pro model
    prompt = f"""
    You are a medical AI assistant. Based on the given patient data, assign an urgency score from 0 to 100.
    The higher the number, the more urgent the case.

    Patient Data:
    - Age: {patient.age}
    - Cancer Stage: {patient.cancer_stage}
    - Needs Chemotherapy: {patient.chemo_needed}
    - Needs Radiotherapy: {patient.radio_needed}
    - Symptoms: {', '.join(patient.symptoms)}
    - Doctor Priority: {patient.doctor_priority}

    Return only a single float number.
    """
    response = model.generate_content(prompt)
    
    try:
        return float(response.text.strip())  # Extract float urgency score
    except ValueError:
        return 0.0  # Default if AI fails

def genrate_rating_radio(user:User):
    r = random.Random() * 100
    client = genai.Client(
            api_key=os.environ.get(API_KEY),
    )

    model = "gemini-2.0-flash"
    contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text="""INSERT_INPUT_HERE"""
                    ),
                ],
            ),
        ]
    generate_content_config = types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192,
            response_mime_type="text/plain",
            system_instruction=[
        types.Part.from_text(
        text="""You are an AI medical assistant.  
        You will analyze patient medical data and return a **single urgency score (0-100)**.  
        Input is a JSON object with patient info.  
        Output is a JSON object containing only `urgency_score`.  
        DO NOT provide explanations—just return the score."""
                ),
            ],
        )

    for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
        print(chunk.text, end="")'''
    
def genrate_rating_radio(user:User):
    return random.random() * 100.0