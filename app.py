from flask import Flask, render_template, jsonify, request
from datetime import datetime
import json
import re
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Firebase'i seadistamine
cred = credentials.Certificate('firebase-credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# NLTK ressursside allalaadimine
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

def analyze_text(text):
    """Analüüsib teksti ja leiab teemad, emotsioonid ja seosed"""
    # Tokeniseeri tekst
    tokens = word_tokenize(text.lower())
    
    # Eemalda stopwords
    stop_words = set(stopwords.words('estonian'))
    tokens = [word for word in tokens if word not in stop_words and len(word) > 2]
    
    # Leia sagedamad sõnad (teemad)
    word_freq = Counter(tokens)
    themes = [word for word, freq in word_freq.most_common(5)]
    
    # Analüüsi emotsioonid
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)
    
    emotions = []
    if sentiment['pos'] > 0.5:
        emotions.append('positiivne')
    if sentiment['neg'] > 0.5:
        emotions.append('negatiivne')
    if sentiment['neu'] > 0.5:
        emotions.append('neutraalne')
    
    return {
        'themes': themes,
        'emotions': emotions,
        'sentiment_score': sentiment['compound']
    }

def find_connections(story_id):
    """Leiab seosed teiste lugude vahel"""
    story_ref = db.collection('stories').document(str(story_id))
    story = story_ref.get()
    
    if not story.exists:
        return []
    
    story_data = story.to_dict()
    connections = []
    
    # Kõigi teiste lugude otsimine
    other_stories = db.collection('stories').where('id', '!=', story_id).stream()
    
    for other_story in other_stories:
        other_data = other_story.to_dict()
        # Lihtne seoste leidmine sarnaste sõnade põhjal
        story_words = set(word_tokenize(story_data['content'].lower()))
        other_words = set(word_tokenize(other_data['content'].lower()))
        common_words = story_words.intersection(other_words)
        
        if len(common_words) > 3:  # Kui on rohkem kui 3 ühist sõna
            connection = {
                'id': other_data['id'],
                'title': other_data['title'],
                'description': f"Sarnased teemad: {', '.join(list(common_words)[:3])}",
                'strength': len(common_words) / 10  # Normaliseeri tugevus 0-1 vahemikku
            }
            connections.append(connection)
            
            # Salvesta seos andmebaasi
            db.collection('connections').add({
                'story_id': story_id,
                'connected_story_id': other_data['id'],
                'common_words': list(common_words),
                'strength': connection['strength'],
                'created_at': firestore.SERVER_TIMESTAMP
            })
    
    return connections

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cosmos')
def cosmos():
    return render_template('cosmos.html')

@app.route('/api/stories', methods=['GET'])
def get_stories():
    stories = []
    for story in db.collection('stories').stream():
        stories.append(story.to_dict())
    return jsonify(stories)

@app.route('/api/stories', methods=['POST'])
def add_story():
    story = request.json
    story['id'] = str(len(list(db.collection('stories').stream())) + 1)
    story['timestamp'] = datetime.now().isoformat()
    
    # Analüüsi lugu
    analysis = analyze_text(story['content'])
    story['emotional_intensity'] = abs(analysis['sentiment_score'])
    story['analysis'] = analysis
    
    # Salvesta andmebaasi
    db.collection('stories').document(story['id']).set(story)
    
    # Loo seosed teiste lugudega
    connections = find_connections(story['id'])
    
    return jsonify(story), 201

@app.route('/api/connections/<string:story_id>', methods=['GET'])
def get_connections(story_id):
    connections = []
    for conn in db.collection('connections').where('story_id', '==', story_id).stream():
        connections.append(conn.to_dict())
    return jsonify(connections)

@app.route('/api/insights/<string:story_id>', methods=['GET'])
def get_insights(story_id):
    story_ref = db.collection('stories').document(story_id)
    story = story_ref.get()
    
    if not story.exists:
        return jsonify({'error': 'Lugu ei leitud'}), 404
    
    story_data = story.to_dict()
    connections = find_connections(story_id)
    
    insights = {
        'themes': story_data['analysis']['themes'],
        'emotions': story_data['analysis']['emotions'],
        'connections': [f"Seos luguga '{conn['title']}'" for conn in connections]
    }
    return jsonify(insights)

if __name__ == '__main__':
    app.run(debug=True) 