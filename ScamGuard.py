from TranscriptReceiver import * 

def main(): 
    print("ScamGuard-Lite-v.0.0.1") 
    transcr_rec = TranscriptReceiver()
    transcr_rec.get_recorded_transcript()
    transcr_rec.save_transcript()
    
if __name__ == "__main__": 
    main(); 
    