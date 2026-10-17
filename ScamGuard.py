from TranscriptReceiver import * 
from scam_detector import *

def main(): 
    print("ScamGuard-Lite-v.0.0.1") 
    transcr_rec = TranscriptReceiver()
    scam_detector = scam_detector()
    transcr_rec.get_recorded_transcript()
    transcr_rec.save_transcript()
    scam_detector.main()

    
if __name__ == "__main__": 
    main(); 
    