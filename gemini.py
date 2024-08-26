import os
import sys
import logging
from langchain.llms import GooglePalm
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("voice_assistant.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("API key not found. Please set it in the .env file.")

llm = GoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=api_key)

user_preferences = {
    "music": "rock",
    "navigation": "shortest route",
    "climate": "cool",
}

prompt_template = """
You are an AI assistant. Focus on understanding and responding to commands and queries.
Current user preferences:
- Music: {music_preference}
- Navigation: {navigation_preference}
- Climate: {climate_preference}

If multiple actions are requested, address them in the order mentioned.

Current conversation:
{history}
Human: {input}
AI:
"""

prompt = PromptTemplate(
    input_variables=["history", "input", "music_preference", "navigation_preference", "climate_preference"],
    template=prompt_template
)

memory = ConversationBufferMemory(input_key="input", memory_key="history")

llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory,
    verbose=False
)

def process_transcription(transcribed_text):
    try:
        response = llm_chain.predict(
            input=transcribed_text,
            music_preference=user_preferences["music"],
            navigation_preference=user_preferences["navigation"],
            climate_preference=user_preferences["climate"]
        )
        logging.info(f"LLM Response: {response}")
        return response
    except Exception as e:
        logging.error(f"Error in LLM processing: {str(e)}")
        return "I encountered an error while processing your request. Could you try again?"

if __name__ == "__main__":
    test_text = "Play some music and set the temperature to cool."
    print(process_transcription(test_text))
