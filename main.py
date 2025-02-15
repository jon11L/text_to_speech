import asyncio
import edge_tts
import json
import os
import datetime

import PyPDF2
# from PyPDF2 import PdfReader


#   -------- This script will require extra external libraries if the PDF file has encryptions. ----------------------------

BASE_AUDIO_DIR = "audio_result/"
AUDIO_FORMAT = ".mp3"


with open("edge_tts_voices.json", "r") as json_file:
    voices_data = json.load(json_file)


def get_pdf_pages(total_pages: int):
    '''Prompt the user to input the page range to extract text from.'''
    # selected_page = False
    while True:
        try:
            print(f"There are {total_pages} pages in the pdf file.")
            page_range = input("Enter the page range (e.g., 1-3 (for page 1 to 3) // 5, 7-9 (for page 5 and 7 to 9)) or press enter for all pages: ").strip()
            if page_range == "":
                return list(range(total_pages))  # default to all pages if no range provided

            pages = page_range.split(",")
            print(f"pages: {pages}") # debug print
            extracted_pages = []
            
            for page in pages:
                page = page.strip()
                if "-" in page:
                    start, end = map(int, page.split("-"))
                    if start < 1 or end > total_pages or start > total_pages or start > end:
                        print(f"Invalid range: {start}-{end}. Enter pages between 1 and {total_pages}.")
                        raise ValueError
                    print(f"\nstart: {start}, end: {end}.\n") #debug print
                    extracted_pages.extend(range(start -1 , end))

                else:
                    page_num = int(page)
                    if page_num < 1 or page_num > total_pages:
                        print(f"Invalid page number: {page_num}. Enter pages between 1 and {total_pages}.")
                        raise ValueError
                    extracted_pages.append(page_num -1)

            else: #  if all inputs are valid
                return extracted_pages
        except ValueError:
            print("Error: Invalid page range. Please enter a valid range (e.g., 1-3, 5, 7-9) or leave blank for all pages.")


def get_text_input():
    '''Prompt the user for direct text input or to provide a pdf file.'''
    choice = input("Enter text manually (T) or provide a PDF file path (P)? [T/P]: ").strip().lower()

    if choice == "p":
        print("If you are on Windows, provide the path like: C:\\Users\\YourName\\Documents\\file.pdf")
        print("If you are on macOS/Linux, provide the path like: /Users/YourName/Documents/file.pdf")
        file_path = input("Enter PDF file path: ").strip()
        if not os.path.isfile(file_path): # or file_path.endswith("pdf"):
            print("Error: File not found or not a PDF file")
            return get_text_input()
        print("file found --> sending pdf to select pages and extract text")
        # page_range = get_pdf_page_range() # give the option to User to select pages in the pdf
        return extract_text_from_pdf(file_path)

    elif choice == "t":
        return input("Type/paste your text here: ").strip()
    else:
        print("Error: Invalid choice. Please enter 'T' for text input or 'P' for PDF file path.")
        return get_text_input()


def get_voice():
    '''Prompt the user to select a voice from the available options.'''
    while True:
        try:
            voice_number = int(input(f"\nSelect a voice number between 1 and {len(voices_data)}: "))
            voice_number -= 1
            if 0 <= voice_number < len(voices_data):
                voice = voices_data[voice_number]["Name"]
                return voice, voice_number
            else:
                print("Error: Invalid voice number.")
        except ValueError:
            print("Error: Invalid voice number. Please enter a number.")


def extract_text_from_pdf(pdf_path):
    '''Extract text from a PDF file using a third-party library.'''

    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        print("**pdf extracted**\n")
        text = ""
        page_count = len(reader.pages)
        # print(f"\nNumber of pages: {page_count}\n") # debug print
        selected_pages = get_pdf_pages(page_count)
        if selected_pages is not None:
            for page_num in selected_pages:
                page = reader.pages[page_num]
                text += page.extract_text()
                print(f"\n**page {page_num+1} extracted**")
                print(f"Text extracted: {text[:100]}...\n")
                # asyncio.sleep(0.1) # Uncomment this line to slow down the conversion speed

        return text.strip()

def generate_file_name(voice_number):
    '''Create a unique audio file name based on current date and time.'''

    print("\nWould you like to enter the name of the audio file? Default name will be the voice selected and time the file was created\n")
    file_name = input("type the file name here or simply press enter:  ")
    if file_name == "": # no name given else the name is given by user
        file_name = f"test_{voice_number +1}" # name the output file.
        if os.path.exists(BASE_AUDIO_DIR + "_" + file_name + AUDIO_FORMAT):
            now = datetime.datetime.now()
            date =  now.strftime("%H%M-%d%m")
            file_name += date

    # Where the audio file will be saved
    output_audio_file = os.path.join(BASE_AUDIO_DIR, file_name + AUDIO_FORMAT)
    return output_audio_file



async def text_to_speech(text, voice, output_file):
    '''Convert the given text into speech.
    Saves the audio file using the edge-tts module
    '''
    communicate = edge_tts.Communicate(text, voice, rate="+0%", pitch="+0Hz", volume="+0%")
    await communicate.save(output_file)



def main():
    '''Main function to orchestrate the text-to-speech conversion.'''
    print("\nText-to-Speech Conversion")
    print("=========================\n")
    
    text = get_text_input()
    voice, voice_number = get_voice()
    
    # print(f"\nSelected Text: {text[:100]}") # debug print
    print(f"Selected Voice: {voice}\n")
    output_file = generate_file_name(voice_number)
    
    print("Converting text to speech...")
    print(f"\nAudio file saved as: {output_file}")

    loop = asyncio.get_event_loop_policy().get_event_loop()
    try:
        loop.run_until_complete(text_to_speech(text, voice, output_file))
    finally:
        loop.close()


if __name__ == "__main__":
    main()


# path for PDF trial
# D:\german learning\A1.1_Loesungen_Arbeitsbuch.pdf
# D:\games\Cartes-Contre-l-Humanite.pdf
# D:\music software_learning\DJing-For-Dummies.pdf


# get text from user V
# select voice
# if text is from pdf edit it
# give filename
# pass text and voice to the edge-tts
# start the script