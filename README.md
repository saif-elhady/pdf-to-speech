# PDF to Speech Conversion

This project converts PDF documents to speech using Python. It extracts text from PDF files and generates audio files (e.g., MP3) that read out the content, allowing users to listen to the contents of their PDF files.

## Features

- **PDF Text Extraction**: Extract text from PDF files using `pdfplumber`.
- **Text-to-Speech Conversion**: Convert the extracted text into speech using `edge_tts` or similar tools.
- **Multiple Language Support**: Support for different languages and voices (e.g., English, French, etc.).
- **Custom Voice Speed**: Ability to control the speed of the speech.
- **Chunking Large Text**: Handles large text files by breaking them into manageable chunks for smoother speech synthesis.

## Requirements

To run this project, you will need the following dependencies:

- Python 3.x
- `pdfplumber` (for extracting text from PDF)
- `edge_tts` (for converting text to speech)
- `asyncio` (for asynchronous processing)
- `fpdf` (optional, for exporting text to PDF after summarization or conversion)

You can install the required libraries using pip:

```bash
pip install pdfplumber edge-tts fpdf asyncio
```

## How to Run

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/pdf-to-speech.git
   cd pdf-to-speech
   ```

2. **Prepare your PDF file**: Place the PDF file you want to convert in the project folder.

3. **Run the notebook**:
   Open and run the notebook `PDF_to_Speech_Conversion.ipynb` using Jupyter or your preferred notebook environment.

4. **Process the PDF**:
   The notebook will:
   - Extract text from the PDF.
   - Optionally clean the text.
   - Convert the text into speech.

5. **Adjust Settings**:
   - Customize the voice and speed of the generated speech by editing the corresponding variables in the notebook (e.g., `voice_speed`, `selected_voice`).

6. **Generate Output**:
   - Once the notebook is executed, an audio file (e.g., MP3) will be generated in the project directory with the speech from the PDF.

## Customization

You can customize the project in the following ways:
- **Change the language or voice**: By selecting different voices available in `edge_tts`.
- **Adjust the speech rate**: Modify the speech rate in the notebook by changing the `rate` parameter.
- **Extract text from specific PDF sections**: Modify the text extraction logic in the notebook to focus on specific pages or sections of the PDF.

## Example

Here is an example of using the project to convert a PDF document into an MP3 file:

```python
import asyncio
import edge_tts
import pdfplumber

# Example: Extract text from PDF and convert to speech
pdf_path = 'example.pdf'

# Extract text from PDF
with pdfplumber.open(pdf_path) as pdf:
    text = ''
    for page in pdf.pages:
        text += page.extract_text()

# Convert text to speech and save as MP3
voice = 'en-US-GuyNeural'
rate = '0%'
output_file = 'output.mp3'

async def convert_to_speech(text, voice, rate, output_file):
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(output_file)

# Run the conversion
asyncio.run(convert_to_speech(text, voice, rate, output_file))
```
