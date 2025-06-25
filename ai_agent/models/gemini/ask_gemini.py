import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# os.environ['HTTP_PROXY'] = 'http://127.0.0.1:8086'
# os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:8086'
load_dotenv()
sys.stdout.reconfigure(encoding='utf-8')
model = ("gemini-2.0-flash-001")

def ask_gemin(contents: types.Content) -> str:
    """
    Ask Gemini model with the given prompt and return the response text.
    
    :param prompt: The input prompt to send to the Gemini model.
    :return: The response text from the Gemini model.
    """
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY"),
        # project="your-project-id",  # Replace with your actual project ID
        # location="global"  # Replace with your actual location if needed
    )
    generate_content_config = types.GenerateContentConfig(
        temperature = 1,
        top_p = 1,
        seed = 0,
        max_output_tokens = 8192
    )
    for chunk in client.models.generate_content_stream(
        model = model,
        contents = contents,
        config = generate_content_config,
    ):
        print(chunk.text, end='', flush=True)
        print()  # Ensure a newline after the response
    return chunk.text

def ask_gemini_with_image(image_path: str, prompt: str) -> str:
    """ 
    Ask Gemini model with an image and a prompt, and return the response text.
    :param image_path: The path to the image file to send to the Gemini model.  
    :param prompt: The input prompt to send to the Gemini model.
    :return: The response text from the Gemini model.
    """
    if prompt.__len__() < 10:
        return "Error: Prompt must be at least 10 characters long."
    try:
        if image_path is None or not image_path.strip():
            contents = [types.Content(role="user",parts=[types.Part(text=prompt)])]
            return ask_gemin(contents)
        if not os.path.exists(image_path):
            return f"Error: Image file '{image_path}' does not exist."
            # image = types.Image(
            #     uri="gs://your-bucket-name/your-image.jpg"  # Replace with your actual image URI
            # )
        image = types.Part.from_bytes(
            data=open(image_path, "rb").read(),
            mime_type="image/png"
        )
        contents = [
            types.Content(
                role="user",
                parts=[
                    image, 
                    types.Part(text=prompt)
                ]
            )
        ]
        return ask_gemin(contents)
    except Exception as e:
        print(f"Error: {e}")
        return str(e)

# from ai_agent.tools import rename_file, read_file, list_files
def persistent_session():
    """
    Main function to interact with the Gemini model.
    """
    while True:
        user_input = input("Input: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        response_text = ask_gemini_with_image("", user_input)
        print("Response:", response_text)

if __name__ == "__main__":
    persistent_session()
