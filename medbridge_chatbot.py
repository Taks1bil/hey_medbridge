import random
import os
from openai import OpenAI

class MedBridgeChatbot:
    def __init__(self, use_gpt_fallback=False):
        self.knowledge_base = {
            "headache": "Headaches can be caused by stress, dehydration, or lack of sleep. If your headache is severe or comes with other symptoms, please see a doctor.",
            "fever": "Fever is your body's way of fighting infection. Rest, stay hydrated, and monitor your temperature. If it persists, consult a healthcare professional.",
            "malaria": "Malaria is a serious disease transmitted by mosquitoes. Symptoms include fever, chills, and body aches. Please get tested and treated immediately.",
            "cold": "The common cold often brings sneezing, coughing, and a sore throat. Rest, hydrate, and it should clear within a week or so.",
            "medbridge ai": "MedBridge AI is your virtual health assistant, offering early guidance on health concerns and helping you know when to seek care.",
            "symptoms": "Tell me more about how you're feeling. What symptoms do you have?",
            "help": "I can answer basic health questions or provide guidance on symptoms. Just type what you're experiencing!",
            "hi": random.choice([
                "Hi there! 😊 How can I help you today?",
                "Hello! I'm here to support your health questions.",
                "Hey! 👋 What can I assist you with today?"
            ]),
            "how are you": "I'm just lines of code, but I'm fully charged and ready to help you stay healthy!"
        }
        self.medical_keywords = ["headache", "fever", "malaria", "cold", "symptoms"]

        self.use_gpt_fallback = use_gpt_fallback
        if self.use_gpt_fallback:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set")
            self.client = OpenAI(api_key=api_key)

    def get_response(self, user_input):
        user_input_lower = user_input.lower().strip()

        # Try local knowledge base first
        # Greetings and small talk
        if any(greet in user_input_lower for greet in ["hi", "hello", "hey"]):
            return self.knowledge_base["hi"]
        elif "how are you" in user_input_lower:
            return self.knowledge_base["how are you"]
        elif "help" in user_input_lower:
            return self.knowledge_base["help"]
        elif "what is medbridge" in user_input_lower or "medbridge ai" in user_input_lower:
            return self.knowledge_base["medbridge ai"]

        # Symptom check
        if "symptoms" in user_input_lower or any(k in user_input_lower for k in self.medical_keywords):
            return self._handle_symptoms(user_input_lower)

        # Fallback to GPT if enabled
        if self.use_gpt_fallback:
            return self._get_gpt_response(user_input)

        # Default fallback response
        return "🤖 Hmm... I’m not sure how to help with that. Try asking about symptoms like 'fever' or type 'help' to see what I can do."

    def _handle_symptoms(self, user_input):
        response_parts = []
        matched = False

        for keyword in self.medical_keywords:
            if keyword in user_input and keyword != "symptoms":
                response_parts.append(self.knowledge_base.get(keyword))
                matched = True

        if not matched:
            response_parts.append(self.knowledge_base["symptoms"])

        if any(word in user_input for word in ["severe", "emergency", "worsening", "can't breathe", "bleeding"]):
            response_parts.append("\n\n🚨 This sounds serious. Please visit a clinic or call emergency services right away.")
        elif matched:
            response_parts.append("\n\n🔎 Please note, I’m not a doctor. Always consult a qualified healthcare provider for a diagnosis.")

        return " ".join(response_parts).strip()

    def _get_gpt_response(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful medical assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            # fallback error message
            return f"🤖 Sorry, I couldn't get a response from the AI service. Error: {e}"

# Local test (CLI use only)
if __name__ == "__main__":
    bot = MedBridgeChatbot(use_gpt_fallback=True)
    print("🤖 MedBridge AI is online. Ask me about your symptoms. Type 'exit' to leave.")
    while True:
        msg = input("You: ")
        if msg.lower() in ["exit", "quit"]:
            print("MedBridge: Take care! 👋")
            break
        print("MedBridge:", bot.get_response(msg))
