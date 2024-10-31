import asyncio
import edge_tts
import os
import playsound


async def speak(text, voice="en-US-AndrewMultilingualNeural", rate="0%"):
    output_file = "temp_audio.mp3"
    tts = edge_tts.Communicate(text, voice)

    # Save the audio file
    await tts.save(output_file)

    # Play the saved audio
    playsound.playsound(output_file)

    # Clean up the temporary file
    os.remove(output_file)


# Run the speak function
async def main():
    text = "A quantum computer is an advanced computing system that uses quantum mechanics to perform complex calculations, so it slays."
    await speak(text, rate="+50%")
    await speak(text)


# Execute the main coroutine
asyncio.run(main())
