# MedBridge AI Chatbot

## Project Overview
This repository contains a basic Python-based chatbot designed as a preliminary frontend for the MedBridge AI healthcare accessibility solution. The chatbot aims to provide immediate, accessible health information and guidance to users, particularly in emerging markets where access to healthcare professionals may be limited. It serves as a proof-of-concept for an AI-powered health assistant capable of handling basic queries and directing users towards appropriate care.

## Features
- **Interactive Conversation:** Engages users in a text-based dialogue.
- **Symptom Inquiry:** Asks users about their symptoms and provides general information based on keywords.
- **General Health Information:** Offers details on common illnesses, preventive measures, and basic health advice.
- **Medical Guidance:** Advises users to seek professional medical attention for severe or persistent symptoms.
- **About MedBridge AI:** Provides information about the platform's mission and capabilities.
- **Multi-language Support (Conceptual):** Designed with future expansion to local languages in mind.

## Setup and Installation

### Prerequisites
To run this chatbot, you will need:
- Python 3.x installed on your system.

### Installation
No specific installation steps are required beyond having Python 3.x. The chatbot is a single Python script.

1.  **Download the script:** Obtain the `medbridge_chatbot.py` file.
    (If you received this README as part of a package, the file should be in the same directory.)

## Usage

### Running the Chatbot Locally
To start an interactive session with the chatbot in your terminal:

1.  **Open your terminal or command prompt.**
2.  **Navigate to the directory** where you saved `medbridge_chatbot.py`.
    ```bash
    cd /path/to/your/chatbot/directory
    ```
3.  **Execute the Python script:**
    ```bash
    python3 medbridge_chatbot.py
    ```
    (If `python3` does not work, try `python medbridge_chatbot.py`)

4.  **Interact with the chatbot:** Follow the prompts and type your questions or symptoms. To end the conversation, type `exit`.

### Example Interaction
```
MedBridge AI Chatbot: Hello! I am MedBridge AI, your personal health assistant. How can I help you today? Type 'exit' to end the conversation.
You: Hi
MedBridge AI Chatbot: Hello! I am MedBridge AI, your personal health assistant. How can I help you today? You can tell me about your symptoms, ask for general health information, or learn more about MedBridge AI.
You: I have a fever and a headache.
MedBridge AI Chatbot: Headaches can be caused by stress, dehydration, or lack of sleep. If your headache is severe, persistent, or accompanied by other symptoms like fever or vision changes, please consult a doctor immediately. Fever is often a sign that your body is fighting an infection. Rest, drink plenty of fluids, and consider fever-reducing medication if needed. If your fever is very high, lasts for more than a few days, or is accompanied by severe symptoms, seek medical attention. 
Remember, I am an AI and cannot provide a diagnosis. Always consult a healthcare professional for accurate medical advice.
You: What is MedBridge AI?
MedBridge AI Chatbot: MedBridge AI is an artificial intelligence-powered platform designed to improve healthcare accessibility in emerging markets. We provide preliminary health information and guidance through a simple chat interface, helping connect people to the care they need.
You: exit
MedBridge AI Chatbot: Goodbye! Stay healthy.
```

## Deployment Instructions (Conceptual)

This basic chatbot is designed for command-line interaction. For real-world deployment as part of the MedBridge AI solution, it would need to be integrated with a messaging platform (like WhatsApp, SMS, or a custom mobile app) and hosted on a server.

### Key Considerations for Deployment:

1.  **Messaging Platform Integration:**
    *   **WhatsApp/SMS API:** Use a service like Twilio, MessageBird, or a similar provider that offers APIs for sending and receiving messages. The chatbot logic would need to be adapted to process incoming messages from these APIs and send responses back.
    *   **Webhook:** The messaging platform would typically send incoming messages to a webhook endpoint hosted on your server. Your chatbot application would listen for these webhooks.

2.  **Server Hosting:**
    *   **Cloud Platforms:** Deploy the Python script on cloud platforms such as AWS (EC2, Lambda), Google Cloud Platform (Cloud Run, App Engine), Azure (App Service), or Heroku. These platforms provide the necessary infrastructure to run your application 24/7.
    *   **Containerization (Docker):** For easier deployment and scalability, consider containerizing the application using Docker. This ensures the environment is consistent across development and production.

3.  **Scalability:**
    *   As user numbers grow, the chatbot needs to handle concurrent requests. Cloud services offer auto-scaling capabilities to manage increased load.

4.  **Security:**
    *   Ensure secure handling of user data, especially if sensitive health information is processed. This includes encryption in transit and at rest, and adherence to data protection regulations (e.g., HIPAA, GDPR).

5.  **Database Integration:**
    *   For a more advanced chatbot, you would integrate with a database to store user conversation history, user profiles, and a more extensive, dynamic knowledge base. This would allow for personalized interactions and continuous learning.

6.  **Advanced NLP/ML Integration:**
    *   To move beyond keyword matching, integrate with more sophisticated Natural Language Processing (NLP) libraries or cloud-based AI services (e.g., Google Dialogflow, AWS Lex, OpenAI APIs) for better understanding of user intent, entity recognition, and more nuanced responses.

### Example Deployment Flow (Simplified):

```mermaid
graph TD
    User[User via WhatsApp/SMS] --> MessagingPlatform[Messaging Platform (e.g., Twilio)]
    MessagingPlatform --> Webhook[Webhook Endpoint (Your Server)]
    Webhook --> ChatbotApp[MedBridge AI Chatbot Application]
    ChatbotApp --> KnowledgeBase[Knowledge Base/Database]
    ChatbotApp --> MessagingPlatform
    MessagingPlatform --> User
```

## Future Enhancements
- Integration with external APIs for clinic locations, emergency services, or telemedicine.
- Expansion of the knowledge base with more detailed medical information.
- Implementation of advanced NLP techniques for better conversational understanding.
- Personalization features based on user history.
- Voice input/output capabilities.
- Integration with electronic health records (with strict privacy controls).

## Contributing
Contributions to enhance the MedBridge AI Chatbot are welcome. Please refer to the project guidelines for more information.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details (if applicable).

---
*Authored by Manus AI for Team 3, MedBridge AI Project.*



## Deploying the Chatbot as a Web Application (Flask)

To make your MedBridge AI Chatbot accessible via a web interface, you can deploy it as a Flask web application. This allows users to interact with the chatbot through a browser or any application that can make HTTP requests.

### Prerequisites for Web Deployment
- A hosting platform that supports Python web applications (e.g., PythonAnywhere, Heroku, Render, DigitalOcean, AWS EC2).
- Basic understanding of Flask and web deployment concepts.

### Files for Web Deployment
- `medbridge_chatbot.py`: The core chatbot logic.
- `app.py`: The Flask application that exposes the chatbot via a web API.
- `requirements.txt`: Lists the Python dependencies (`Flask`).

### `app.py` Overview
The `app.py` file sets up a simple Flask application with one main endpoint (`/chat`) that accepts POST requests. When a message is sent to this endpoint, it uses the `MedBridgeChatbot` to generate a response and returns it as JSON.

```python
from flask import Flask, request, jsonify
from medbridge_chatbot import MedBridgeChatbot

app = Flask(__name__)
chatbot = MedBridgeChatbot()

@app.route("/")
def index():
    return "MedBridge AI Chatbot API. Use /chat to interact."

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"response": "No message provided."}), 400

    bot_response = chatbot.get_response(user_message)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
```

### `requirements.txt`
This file lists the Python packages required by your Flask application:

```
Flask
```

### General Deployment Steps (Example: PythonAnywhere/Heroku)

While specific steps vary by platform, the general process involves:

1.  **Sign up for a hosting account:** Create an account on your chosen platform (e.g., [PythonAnywhere](https://www.pythonanywhere.com/), [Heroku](https://www.heroku.com/)).
2.  **Upload your files:** Upload `medbridge_chatbot.py`, `app.py`, and `requirements.txt` to your project directory on the hosting platform.
3.  **Install dependencies:** The platform will typically read `requirements.txt` and install Flask and any other necessary libraries automatically.
4.  **Configure the web application:**
    *   **PythonAnywhere:** You would create a new web app, select Flask, and point it to your `app.py` file (specifically, the `app` object within it).
    *   **Heroku:** You would use Git to push your code to Heroku, and you might need a `Procfile` to tell Heroku how to run your Flask app (e.g., `web: gunicorn app:app`).
5.  **Start the web application:** Once configured, the platform will start your Flask application, making it accessible via a public URL.

### Testing the Deployed API
Once deployed, you can test your chatbot API using tools like `curl` or Postman, or by building a simple HTML form.

**Example `curl` command:**

```bash
curl -X POST -H "Content-Type: application/json" -d "{\"message\": \"hello\"}" YOUR_DEPLOYED_URL/chat
```

Replace `YOUR_DEPLOYED_URL` with the actual URL provided by your hosting platform.

### Building a Simple Web Frontend (Optional)

For a user-friendly interface, you can create a simple HTML page with JavaScript that sends messages to your deployed Flask API. This HTML page can then be hosted on a static hosting service like Netlify.

**`index.html` (Example Snippet):**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MedBridge AI Chatbot</title>
    <style>
        body { font-family: sans-serif; margin: 20px; background-color: #f4f4f4; }
        #chat-box { border: 1px solid #ccc; padding: 10px; height: 300px; overflow-y: scroll; background-color: #fff; }
        #user-input { width: calc(100% - 80px); padding: 8px; margin-top: 10px; }
        #send-button { padding: 8px 15px; margin-left: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>MedBridge AI Chatbot</h1>
    <div id="chat-box"></div>
    <input type="text" id="user-input" placeholder="Type your message...">
    <button id="send-button">Send</button>

    <script>
        const chatBox = document.getElementById("chat-box");
        const userInput = document.getElementById("user-input");
        const sendButton = document.getElementById("send-button");
        const API_URL = "YOUR_DEPLOYED_URL/chat"; // *** IMPORTANT: Replace with your actual deployed API URL ***

        function appendMessage(sender, message) {
            const msgDiv = document.createElement("div");
            msgDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
            chatBox.appendChild(msgDiv);
            chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
        }

        sendButton.addEventListener("click", async () => {
            const message = userInput.value.trim();
            if (message === "") return;

            appendMessage("You", message);
            userInput.value = "";

            try {
                const response = await fetch(API_URL, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ message: message })
                });
                const data = await response.json();
                appendMessage("MedBridge AI", data.response);
            } catch (error) {
                console.error("Error communicating with chatbot API:", error);
                appendMessage("MedBridge AI", "Sorry, I'm having trouble connecting right now. Please try again later.");
            }
        });

        userInput.addEventListener("keypress", (event) => {
            if (event.key === "Enter") {
                sendButton.click();
            }
        });

        appendMessage("MedBridge AI", "Hello! I am MedBridge AI, your personal health assistant. How can I help you today?");
    </script>
</body>
</html>
```

Remember to replace `YOUR_DEPLOYED_URL` in the JavaScript code with the actual URL of your deployed Flask application. This `index.html` can then be hosted on Netlify as a static site.



## Deploying the Chatbot as a Streamlit Web Application

Streamlit provides a straightforward way to turn Python scripts into interactive web applications. This is an excellent option for showcasing your MedBridge AI Chatbot with a user-friendly interface.

### Files for Streamlit Deployment
- `medbridge_chatbot.py`: The core chatbot logic.
- `streamlit_app.py`: The Streamlit application that creates the web interface.
- `requirements.txt`: Lists the Python dependencies (`streamlit`).

### `streamlit_app.py` Overview
The `streamlit_app.py` file uses Streamlit components to build a chat interface. It initializes the `MedBridgeChatbot` and maintains the conversation history in `st.session_state`.

```python
import streamlit as st
from medbridge_chatbot import MedBridgeChatbot

# Initialize the chatbot
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = MedBridgeChatbot()

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

st.set_page_config(page_title="MedBridge AI Chatbot", page_icon=":robot_face:")
st.title("MedBridge AI Chatbot")
st.markdown("Your personal health assistant. Ask me about symptoms, general health, or MedBridge AI.")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What can I help you with?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot response
    with st.chat_message("assistant"):
        response = st.session_state.chatbot.get_response(prompt)
        st.markdown(response)
    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
```

### `requirements.txt` (for Streamlit)
This file lists the Python packages required by your Streamlit application:

```
Flask
streamlit
```

### Running the Streamlit App Locally

1.  **Ensure Python and pip are installed.**
2.  **Navigate to your project directory** in the terminal where `medbridge_chatbot.py`, `streamlit_app.py`, and `requirements.txt` are located.
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Streamlit application:**
    ```bash
    streamlit run streamlit_app.py
    ```
    This command will open a new tab in your web browser with the Streamlit application.

### Deploying to Streamlit Community Cloud

Streamlit Community Cloud offers a free and easy way to deploy your Streamlit applications. You will need a GitHub repository for your project.

1.  **Create a GitHub Repository:**
    *   Initialize a new Git repository in your project folder.
    *   Add `medbridge_chatbot.py`, `streamlit_app.py`, and `requirements.txt` to this repository.
    *   Commit your changes and push them to GitHub.

2.  **Sign up/Log in to Streamlit Community Cloud:**
    *   Go to [https://share.streamlit.io/](https://share.streamlit.io/) and sign in with your GitHub account.

3.  **Deploy your app:**
    *   Click on the "New app" button.
    *   Select your GitHub repository and the branch where your app code resides.
    *   Specify the main file path as `streamlit_app.py`.
    *   Click "Deploy!"

Streamlit will build and deploy your application, providing you with a public URL that you can share with others. Any changes you push to your GitHub repository will automatically trigger a redeployment on Streamlit Community Cloud.

### Important Notes for Deployment:

*   **`medbridge_chatbot.py` must be in the same directory** as `streamlit_app.py` or accessible via Python path, as `streamlit_app.py` imports it.
*   **Streamlit Community Cloud automatically installs dependencies** listed in `requirements.txt`.
*   **For more complex applications or persistent data**, consider integrating with external databases or APIs, as Streamlit Community Cloud is stateless.


