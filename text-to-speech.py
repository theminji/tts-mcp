from typing import Any
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""
from mcp.server.fastmcp import FastMCP
from supertonic import TTS
from pathlib import Path
mcp = FastMCP("text-to-speech")
tts = TTS(auto_download=True)
STYLE_PATH = Path("Pixie.json")

style = tts.get_voice_style("F1")
@mcp.tool()
async def text_to_speech(input_text: str, output_filename: str = "speech.wav") -> str:
    """Convert input text to a speech audio file and save it to disk
    
    Args:
        input_text: text to synthesize speech from (as a string)
        output_filename: name of the output WAV file (default: speech.wav)
    Output:
        Filepath to generated audio, and the duration of the audio
    """
    try:
        wav, duration = tts.synthesize(input_text, voice_style=style, speed=1.2)
        tts.save_audio(wav, output_path=output_filename)
        output_path = Path(output_filename)
        duration_sec = float(duration) if duration is not None else 0.0
        
        return f"Successfully generated speech audio and saved to: {output_path.absolute()}\nDuration: {duration_sec:.2f} seconds"
        
    except Exception as e:
        return f"Error generating speech: {str(e)}"

def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()