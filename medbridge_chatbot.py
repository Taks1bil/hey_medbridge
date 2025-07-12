
class MedBridgeChatbot:
    def __init__(self):
        self.knowledge_base = {
            "headache": "Headaches can be caused by stress, dehydration, or lack of sleep. If your headache is severe, persistent, or accompanied by other symptoms like fever or vision changes, please consult a doctor immediately.",
            "fever": "Fever is often a sign that your body is fighting an infection. Rest, drink plenty of fluids, and consider fever-reducing medication if needed. If your fever is very high, lasts for more than a few days, or is accompanied by severe symptoms, seek medical attention.",
            "malaria": "Malaria is a serious disease caused by a parasite spread by mosquitoes. Symptoms include fever, chills, and flu-like illness. It is preventable and curable. If you suspect you have malaria, please seek medical attention for proper diagnosis and treatment.",
            "cold": "The common cold is a viral infection of your nose and throat. Symptoms usually include a runny nose, sore throat, cough, and congestion. Rest, fluids, and over-the-counter remedies can help. It usually resolves within a week or two.",
            "medbridge ai": "MedBridge AI is an artificial intelligence-powered platform designed to improve healthcare accessibility in emerging markets. We provide preliminary health information and guidance through a simple chat interface, helping connect people to the care they need.",
            "symptoms": "Please describe your symptoms in more detail. For example, 'I have a cough and a sore throat.'",
            "help": "I can help you with basic health information, answer questions about common symptoms, or tell you more about MedBridge AI. What would you like to know?",
            "hi": "Hello! I am MedBridge AI, your personal health assistant. How can I help you today? You can tell me about your symptoms, ask for general health information, or learn more about MedBridge AI.",
            "hello": "Hello! I am MedBridge AI, your personal health assistant. How can I help you today? You can tell me about your symptoms, ask for general health information, or learn more about MedBridge AI.",
            "how are you": "I am an AI, so I don't have feelings, but I'm ready to assist you! How can I help you with your health today?"
        }
        self.medical_keywords = ["headache", "fever", "malaria", "cold", "symptoms"]

    def get_response(self, user_input):
        user_input = user_input.lower()

        if "symptoms" in user_input or any(keyword in user_input for keyword in self.medical_keywords):
            return self._handle_symptoms(user_input)
        elif "medbridge ai" in user_input or "what is medbridge ai" in user_input:
            return self.knowledge_base["medbridge ai"]
        elif "hello" in user_input or "hi" in user_input:
            return self.knowledge_base["hello"]
        elif "how are you" in user_input:
            return self.knowledge_base["how are you"]
        elif "help" in user_input:
            return self.knowledge_base["help"]
        else:
            return "I'm not sure how to respond to that. Can you rephrase your question or ask about a specific symptom or health topic?"

    def _handle_symptoms(self, user_input):
        response = []
        found_symptom = False
        for keyword in self.medical_keywords:
            if keyword in user_input and keyword != "symptoms":
                response.append(self.knowledge_base.get(keyword, ""))
                found_symptom = True
        
        if not found_symptom:
            response.append(self.knowledge_base["symptoms"])

        if "severe" in user_input or "persistent" in user_input or "worse" in user_input or "emergency" in user_input:
            response.append("\n\nImportant: Your symptoms sound concerning. Please seek immediate medical attention from a qualified healthcare professional or visit the nearest clinic.")
        elif found_symptom:
            response.append("\n\nRemember, I am an AI and cannot provide a diagnosis. Always consult a healthcare professional for accurate medical advice.")

        return " ".join(response).strip()


if __name__ == "__main__":
    chatbot = MedBridgeChatbot()
    print("MedBridge AI Chatbot: Hello! I am MedBridge AI, your personal health assistant. How can I help you today? Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("MedBridge AI Chatbot: Goodbye! Stay healthy.")
            break
        response = chatbot.get_response(user_input)
        print(f"MedBridge AI Chatbot: {response}")


