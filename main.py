from openai import OpenAI # imports the OpenAI client library
from dotenv import load_dotenv
import os # imports a build way to interact with the underlying operating system
import json

load_dotenv()
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY")) # client initialization with your API key

#3 things every API call needs = key, model, prompt

#system promt = AI's job description
SYSTEM_PROMPT = """
You are a clinical triage assistant. Your job is to receive user-reported symptoms and recommend next steps. You do not provide a diagnosis like a doctor.
Based on the user's input, classify the situation into one of the following categories:
- Home Care
- Primary Care
- Urgent Care
- Emergency Care

Return your response in strict JSON format with the following fields:
- severity: one of ["Home Care", "Primary Care", "Urgent Care", "Emergency Care"]
- recommendation: a clear next step for the user
- explanation: a brief reasoning for the recommendation (1–2 sentences)
""" # When something is writtenn in ALL_CAPS, it means it is not to be changed ever, it is constant.

symptoms = input("describe your symptoms: ") #user input for symptoms


if len(symptoms) < 7: # input must be 7 characters long
    print("Invalid input. Please describe a real symptom you are feeling.")
    exit()

response = client.chat.completions.create(
    model = "gpt-4o-mini", # calls to model type from OpenAI we are calling
    messages = [ # dictionary to seperate content for a user roles
        {"role" : "system", "content": SYSTEM_PROMPT}, # Role is the agent if SYSTEM_PROMPT is accessible which also means no access to user role content
        {"role" : "user", "content": symptoms} # if user input for symptom is touched we know that role will be user role no access to system role content
    ]
)

result = response.choices[0].message.content # When answer is created multiple messages are made, here is where we choose first prompt to ensure efficiency




try:
    
    if result == None:
        print(["no response received"]) #handles empty cases
    else:
        data = json.loads(result or "")   # Only parse when result actually exists 
        print("* " + data["severity"]) # prints the needed fields
        print("* " + data["recommendation"])
        print("* " + data["explanation"])
except json.JSONDecodeError:  # catches broken JSON
    print("the AI returned something that wasn't a valid JSON") 


