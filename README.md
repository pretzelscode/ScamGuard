# ScamGuard 

ScamGuard is our entry for the Security challenge in Hacktoberfest 2026. It is very common for people to be victimized with scam calls, causing security risks to personal private information. Most victims are unaware that they are part of a scam call and willingly give their private information to a scammer in hopes to resolve technical issues or other problems in which they are told to call to receive "help". There are specific suspicious speech patterns and sensitive information usually shared in these scam calls, therefore the aim of this project is to provide an AI-powered tool that can interpret scammy conversations to protect victims from scam calls by informing them that the conversation is a scam. 

# Open-Source Tools Used
We use two open-source tools for this project: Handy and SpaCY. Handy is a transcription tool that uses the Parakeet V3 speech-to-text model to transcribe recorded audio. Wherever your text cursor is located, it will write the transcription there.  SpaCY, on the other hand, is an open-source natural language processing tool that will take our transcriptions and give context to the conversation. 

# Our Contributions
Since Handy and SpaCY serve completely different purposes for our overall app, we had to implement middleware to process transcriptions and connect the two software tools. Handy currently does not have the feature to stream live data, therefore we pre-record a conversation between two people, and we process the transcription. The transcriptions are concatenated to one giant text, therefore we had to figure out how to break the dialogue between two people. We focused on the punctuations to separate the text to different lines for spaCY to digest because it should be agnostic to who is speaking in the conversation. Once spaCY gets the context of the conversation, it will provide a score of how suspicious the conversation was to determine if it was a safe conversation or if it was scam. 

# Requirements 
You will need to install the following: 
- Handy: `winget install cjpais.Handy`
- Spacy: `pip install spacy` 

# How to Run
Run the following to run the scam guard: 
`python -m ScamGuard.py` 
while scam guard is running, press `ctrl+space` to start recording using Handy. This should transcribe messages for you. When you're done recording press `ctrl+space` again and hit `Enter` twice.

Run the following to get the score of your conversation:
`python scam_detector.py` 