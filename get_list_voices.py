import subprocess
import json
import re

def get_edge_tts_voices():
    '''Returns a list of the voices available from the edge-tts module
    takes this list normally presented in the console and iterate over it
    to return in a readable json format.
    From then it facilitates the task to choice between the voices available"
    '''
    try:
        # Run the `edge-tts --list-voices` command
        result = subprocess.run(["edge-tts", "--list-voices"], capture_output=True, text=True, check=True)
        
        lines = result.stdout.strip().split("\n")
        voices = []
        
        # Regex to extract fields from each line
        pattern = r"^(\S+)\s+(Male|Female)\s+(.+?)\s{2,}(.+)$"
        
        id_number = 0
        for line in lines:
            # Skip headers or invalid lines
            if not line or "Name" in line or "--------" in line:
                continue

            id_number += 1

            match = re.match(pattern, line)
            if match:
                name, gender, categories, personalities = match.groups()
                voices.append({
                    "id": id_number,
                    "Name": name,
                    "Gender": gender,
                    "ContentCategories": categories,
                    "VoicePersonalities": personalities,
                })
        
        return voices
    except subprocess.CalledProcessError as e:
        print("Error running edge-tts:", e)
        return []
    except Exception as e:
        print("An unexpected error occurred:", e)
        return []

# Get the list of voices
voices = get_edge_tts_voices()

# store the list of voices in a separate file
with open("edge_tts_voices.json", "w") as file:
    json.dump(voices, file, indent=4)