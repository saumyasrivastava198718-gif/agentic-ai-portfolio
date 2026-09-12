from dotenv import load_dotenv
from google import genai

# Load variables from .env
load_dotenv()

# Create Gemini client
client = genai.Client()

# Send a simple test request
interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="Explain RAG in three simple sentences."
)

print("\nGEMINI RESPONSE:\n")
print(interaction.output_text)