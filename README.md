# Therapy Chatbot

A conversational AI-powered therapy chatbot built with LangChain, Google Generative AI, and Streamlit. This application provides emotional and logical support by classifying user inputs and responding appropriately with either empathetic, therapist-like responses or factual, logical answers.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Project Overview
The Therapy Chatbot is designed to assist users by providing tailored responses based on the nature of their input. It leverages natural language processing to classify messages as either "emotional" (requiring empathetic support) or "logical" (requiring factual information). The chatbot uses a state-based workflow to process inputs and is accessible via both a command-line interface and a Streamlit web interface.

## Features
- **Message Classification**: Automatically identifies whether a user's message requires emotional or logical support.
- **Empathetic Responses**: Acts as a compassionate therapist for emotional queries, validating feelings and asking thoughtful follow-up questions.
- **Logical Responses**: Provides clear, concise, and evidence-based answers for informational or analytical queries.
- **Dual Interfaces**:
  - Command-line interface for quick interaction.
  - Streamlit-based web UI for a user-friendly experience.
- **Persistent Chat History**: Maintains conversation context using session state in the Streamlit interface.

## Directory Structure
```
ahmedelkassrawy-therapy-chatbot/
├── chatbot.py                     # Core chatbot logic and workflow
├── requirements.txt               # Dependencies for the core chatbot
├── streamlit.py                   # Streamlit web interface for the chatbot
└── therapy-chatbot-ui/            # Streamlit-based UI subproject
    ├── README.md                  # Documentation for the UI subproject
    ├── requirements.txt           # Dependencies for the UI subproject
    └── src/
        ├── app.py                 # Main entry point for the Streamlit UI
        ├── chatbot.py             # Streamlit-specific chatbot integration
        └── components/
            └── __init__.py        # Placeholder for reusable UI components
```

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ahmedelkassrawy/therapy-chatbot.git
   cd ahmedelkassrawy-therapy-chatbot
   ```

2. **Set Up a Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   - For the core chatbot:
     ```bash
     pip install -r requirements.txt
     ```
   - For the Streamlit UI:
     ```bash
     cd therapy-chatbot-ui
     pip install -r requirements.txt
     ```

4. **Set Environment Variables**:
   - Replace the Google API key in `chatbot.py` and `streamlit.py` with your own key:
     ```python
     os.environ["GOOGLE_API_KEY"] = "your-google-api-key"
     ```

5. **Run the Application**:
   - **Command-Line Interface**:
     ```bash
     python chatbot.py
     ```
     Type messages in the terminal and press Enter. Type `exit` to quit.
   - **Streamlit Web Interface** (from the root directory):
     ```bash
     streamlit run streamlit.py
     ```
     Or, for the alternative UI:
     ```bash
     cd therapy-chatbot-ui
     streamlit run src/app.py
     ```

## Usage
- **Command-Line Interface**:
  - Run `python chatbot.py` and interact with the chatbot via the terminal.
  - Example:
    ```
    Message: I'm feeling really overwhelmed today.
    Assistant: I'm so sorry to hear you're feeling overwhelmed. It sounds really tough. Can you share a bit more about what's been going on?
    ```
  - Type `exit` to end the session.

- **Streamlit Web Interface**:
  - Access the web UI via the browser after running the Streamlit command.
  - Enter messages in the input field and view responses in the chat history.
  - Type `exit` to reset the conversation.

## Technologies Used
- **Python**: Core programming language.
- **LangChain**: For building the chatbot workflow and integrating with Google Generative AI.
- **Google Generative AI (Gemini)**: Powers the language model for message classification and responses.
- **Streamlit**: Provides the web-based user interface.
- **Pydantic**: For structured data validation (e.g., message classification).
- **Qdrant**: Vector store integration (not fully utilized in the current version).

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please ensure your code follows the existing style and includes appropriate tests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
