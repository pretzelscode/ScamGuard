import re
import spacy
from pathlib import Path

BASE = Path(__file__).parent
INPUT_DIR = BASE / "raw_transcript"

nlp = spacy.load("en_core_web_sm")

CATEGORIES = {
    "Untraceable payment": (30, ["gift card", "itunes card", "google play card", "wire transfer",
                                 "western union", "moneygram", "bitcoin", "cryptocurrency",
                                 "cash app", "zelle"]),
    "Secrecy":             (25, ["do not tell anyone", "do not tell", "keep this secret",
                                 "keep it between us", "confidential", "do not hang up"]),
    "Remote access":       (25, ["remote access", "anydesk", "teamviewer", "download the software",
                                 "install the app", "share your screen"]),
    "Urgency":             (15, ["right now", "immediately", "urgent", "within the hour",
                                 "last chance", "today only", "act now"]),
    "Threat / fear":       (20, ["arrest warrant", "arrest", "lawsuit", "legal action", "suspend",
                                 "account be freeze", "compromise", "virus", "hack", "fraud alert"]),
    "Sensitive info":      (40, ["social security number", "give me your password", "I will need your password","verification code",
                                 "pin number", "routing number", "card number", "bank account"]),
}

AUTHORITY = {"microsoft", "apple", "amazon", "irs", "medicare", "social security administration",
             "paypal", "bank", "fbi", "police", "norton", "geek squad"}


def lemma_string(doc) -> str:
    """Lowercase lemmas joined by spaces, padded so whole-word matching is easy."""
    return " " + " ".join(t.lemma_.lower() for t in doc if not t.is_punct) + " "


# Convert each phrase to its lemma form once, the same way transcripts are converted
LEMMA_PHRASES = {
    cat: (weight, [(p, lemma_string(nlp(p)).strip()) for p in phrases])
    for cat, (weight, phrases) in CATEGORIES.items()
}


def analyze(text: str) -> dict:
    doc = nlp(" ".join(text.split()))
    lemmas = lemma_string(doc)

    hits = {}
    for cat, (_, phrases) in LEMMA_PHRASES.items():
        for original, lemma_form in phrases:
            if f" {lemma_form} " in lemmas:
                hits.setdefault(cat, set()).add(original)

    orgs = {e.text.lower() for e in doc.ents if e.text.lower() in AUTHORITY}
    # Fallback in case the NER model misses a name
    orgs |= {a for a in AUTHORITY if re.search(rf"\b{re.escape(a)}\b", text.lower())}
    money = [e.text for e in doc.ents if e.label_ == "MONEY"]

    score = sum(CATEGORIES[c][0] for c in hits)
    reasons = [f"{c}: {', '.join(sorted(v))}" for c, v in hits.items()]

    if orgs:
        score += 10
        reasons.append(f"Claims to be: {', '.join(sorted(orgs))}")
    if money:
        score += 10
        reasons.append(f"Money mentioned: {', '.join(money)}")

    if orgs and ("Urgency" in hits or "Threat / fear" in hits) and \
       ("Untraceable payment" in hits or "Sensitive info" in hits):
        score += 25
        reasons.append("Combo: authority + pressure + payment/info demand")

    score = min(score, 100)
    verdict = "SCAM LIKELY" if score >= 60 else "SUSPICIOUS" if score >= 30 else "LOOKS SAFE"
    return {"score": score, "verdict": verdict, "reasons": reasons}


if __name__ == "__main__":
    print(f"Looking in: {INPUT_DIR}")
    if not INPUT_DIR.is_dir():
        raise SystemExit("Folder not found. Run make_test_transcripts.py first, "
                         "and keep raw_transcript/ next to this script.")
    files = sorted(INPUT_DIR.glob("*.txt"))
    if not files:
        raise SystemExit("raw_transcript/ has no .txt files.")

    for f in files:
        r = analyze(f.read_text(encoding="utf-8"))
        print(f"\n=== {f.name} ===")
        print(f"Risk: {r['score']}%  ->  {r['verdict']}")
        for reason in r["reasons"]:
            print(f"  - {reason}")