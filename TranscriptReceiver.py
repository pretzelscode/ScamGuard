import msvcrt


class TranscriptReceiver: 
    def __init__(self): 
        self.text_input = ""

    def get_recorded_transcript(self):
        print(">", end="", flush=True)
        
        while True:
            if msvcrt.kbhit():
                char = msvcrt.getch()
                
                # Detect Ctrl + Space (Registers as a null byte b'\x00' on Windows)
                if char in (b'\r', b'\n'):
                    print("!! Enter pressed. App is no longer receiving input.")
                    break
                
                # Echo typed text to the screen
                else:
                    self.input_chars = input()
                
                    
    def save_transcript(self):
        with open("rawTranscript.txt", "w", encoding="utf-8") as file:
            file.write(self.input_chars)
