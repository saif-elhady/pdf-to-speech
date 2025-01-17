from flask import Flask, request, jsonify, send_file, render_template
import os
import asyncio
import edge_tts
import pdfplumber
from flasgger import Swagger, swag_from


app = Flask(__name__)
swagger = Swagger(app)

# Define available voices and languages
VOICES = {
    'en': ['en-US-GuyNeural', 'en-US-JennyNeural'],
    'af': ['af-ZA-AdriNeural'],
    'bn': ['bn-IN-BashkarNeural', 'bn-IN-TanishaaNeural'],
    'bs': ['bs-BA-GoranNeural', 'bs-BA-VesnaNeural'],
    'bg': ['bg-BG-BorislavNeural', 'bg-BG-KalinaNeural'],
    'my': ['my-MM-NilarNeural', 'my-MM-ThihaNeural'],
    'ca': ['ca-ES-EnricNeural', 'ca-ES-JoanaNeural'],
    'zh': ['zh-HK-HiuGaaiNeural', 'zh-HK-HiuMaanNeural', 'zh-HK-WanLungNeural'],
    'hr': ['hr-HR-GabrijelaNeural', 'hr-HR-SreckoNeural'],
    'cs': ['cs-CZ-AntoninNeural', 'cs-CZ-VlastaNeural'],
    'da': ['da-DK-ChristelNeural', 'da-DK-JeppeNeural'],
}

def pdf_to_text_plumber(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

async def generate_audio(text, voice, output_file):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

@app.route('/')
def index():
    return render_template('index.html')  # Make sure your HTML is named 'index.html'

@app.route('/convert/', methods=['POST'])

@swag_from({
    'parameters': [
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'The PDF file to be converted'
        }
    ],
    'responses': {
        200: {
            'description': 'The audio file',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'string',
                        'example': 'Audio file generated successfully'
                    }
                }
            }
        }
    }
})

def convert_to_audio():
    # Get the uploaded PDF file
    
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(error="No selected file"), 400
    async def generate_audio(text, voice, output_file):
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
    

    # Set default language, voice, and speed
    lang = 'en'
    voice = 'en-US-GuyNeural'  # Default voice
    
    # Save the uploaded file temporarily
    pdf_path = f"temp_{file.filename}"
    file.save(pdf_path)
    
    # Extract text from the PDF
    text = pdf_to_text_plumber(pdf_path)
    
    # Define the output MP3 file path
    output_file = f"output_{file.filename.split('.')[0]}.mp3"
    
    # Generate audio from the extracted text
    asyncio.run(generate_audio(text, voice, output_file))
    
    # Remove the temporary PDF file
    os.remove(pdf_path)
    
    # Return the MP3 file to the client
    return send_file(output_file, as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)
