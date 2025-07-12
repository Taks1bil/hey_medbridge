import random
import os
from openai import OpenAI

class MedBridgeChatbot:
    def __init__(self, use_gpt_fallback=False):
        # Predefined answers for common health questions
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

        # Setup OpenAI GPT client if fallback is enabled
        if self.use_gpt_fallback:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("❌ OPENAI_API_KEY environment variable is not set.")
            self.client = OpenAI(api_key=api_key)

    def get_response(self, user_input):
        user_input_lower = user_input.lower().strip()

        # Check for greetings and common phrases in user input
        if any(word in user_input_lower for word in ["hi", "hello", "hey"]):
            return self.knowledge_base["hi"]
        elif "how are you" in user_input_lower:
            return self.knowledge_base["how are you"]
        elif "help" in user_input_lower:
            return self.knowledge_base["help"]
        elif "what is medbridge" in user_input_lower or "medbridge ai" in user_input_lower:
            return self.knowledge_base["medbridge ai"]

        # If user asks about symptoms or mentions medical keywords
        if "symptoms" in user_input_lower or any(k in user_input_lower for k in self.medical_keywords):
            return self._handle_symptoms(user_input_lower)

        # If no match above and fallback enabled, ask GPT
        if self.use_gpt_fallback:
            return self._ask_gpt(user_input)

        # Default response if nothing matched
        return "🤖 I'm not sure how to help with that. Try asking about symptoms like 'fever', or type 'help'."

    def _handle_symptoms(self, user_input_lower):
        responses = []
        found = False

        # Look for known medical keywords in input
        for keyword in self.medical_keywords:
            if keyword in user_input_lower and keyword != "symptoms":
                responses.append(self.knowledge_base[keyword])
                found = True

        # If no specific keywords found, ask for more details
        if not found:
            responses.append(self.knowledge_base["symptoms"])

        # Warn if serious symptoms are mentioned
        if any(word in user_input_lower for word in ["severe", "emergency", "worsening", "can't breathe", "bleeding"]):
            responses.append("\n\n🚨 This sounds serious. Please visit a clinic or call emergency services.")
        elif found:
            responses.append("\n\n🔎 Note: I'm not a doctor. Always check with a qualified health provider.")

        return " ".join(responses).strip()

    def _ask_gpt(self, prompt):
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
            return f"❌ Sorry, I couldn't reach the AI service. Error: {e}"

# CLI test example (optional)
if __name__ == "__main__":
    bot = MedBridgeChatbot(use_gpt_fallback=True)
    print("🤖 MedBridge AI is online. Ask me anything! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Take care!")
            break
        print("MedBridge:", bot.get_response(user_input))
