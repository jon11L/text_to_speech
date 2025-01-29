import asyncio
import edge_tts
import json
import os


BASE_AUDIO_DIR = "audio_result/"
AUDIO_FORMAT = ".mp3"


with open("edge_tts_voices.json", "r") as json_file:
    voices_data = json.load(json_file)

with open("test_read.md", "r") as file:
    text_2 = file.read()
    # voices_data = json.load(file)


# include an imput for user to type in their text. or invite to put the path to a pdf or text file.
text_input = input("Type or paste your text here:  ")

# here change the number to select another voice from 0 to 322 (find in edge_tts_voices.json file)
voice_number =  int(input(f"Type the number of the voice desired between 0 and {len(voices_data)}:  "))

TEXT = text_input
VOICE = voices_data[voice_number]["Name"] 
print(f"Voice selected: \n{VOICE}\n")


print("Would you like to enter the name of the audio file. If none given it will remain unchanged.")
file_name = input("type name here or simply press enter:  ")
if file_name == "": # no name given else the name is given by user
    file_name = f"test_{voice_number}" # name the output file.

# Where the audio file will be saved
output_audio_file = os.path.join(BASE_AUDIO_DIR, file_name + AUDIO_FORMAT)


async def amain():
    '''Convert the given text into speech.
    Saves the audio file using the edge-tts module
    '''
    communicate = edge_tts.Communicate(text_2, VOICE, rate="+0%", pitch="-5Hz", volume="+0%")
    await communicate.save(output_audio_file)

loop = asyncio.get_event_loop_policy().get_event_loop()
try:
    loop.run_until_complete(amain())
finally:
    loop.close()