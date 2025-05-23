# Sentimentalapp

Interaktiivne rakendus lugude ja emotsioonide visualiseerimiseks.

## Seadistamine

1. Klooni repositoorium:
```bash
git clone [repository-url]
cd Sentimentalapp
```

2. Loo virtuaalne keskkond ja aktiveeri see:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# või
venv\Scripts\activate  # Windows
```

3. Paigalda sõltuvused:
```bash
pip install -r requirements.txt
```

4. Firebase'i seadistamine:
   - Mine [Firebase Console](https://console.firebase.google.com/)
   - Loo uus projekt
   - Loo Firestore andmebaas
   - Lae alla teenuse konto võtmed (Service Account Key)
   - Salvesta fail kui `firebase-credentials.json` projekti juurkausta

5. Käivita rakendus:
```bash
python app.py
```

## Funktsioonid

- Lugude salvestamine ja analüüs
- Emotsionaalse intensiivsuse mõõtmine
- Lugude vaheliste seoste visualiseerimine
- Interaktiivne kosmose visualiseerimine
- Teemade ja emotsioonide tuvastamine

## Tehnoloogiad

- Python/Flask
- Firebase/Firestore
- D3.js
- NLTK
- HTML/CSS/JavaScript 