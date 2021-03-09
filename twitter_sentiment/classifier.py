import re
import pickle
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

with open('twitter_sentiment/models/Tokenizer.pickle', 'rb') as file:
    tokenizer = pickle.load(file)
model = load_model('twitter_sentiment/models/Twitter-Sentiment-BiLSTM.h5')

# Reading contractions.csv and storing it as a dict.
contractions = pd.read_csv('twitter_sentiment/models/contractions.csv', index_col='Contraction')
contractions.index = contractions.index.str.lower()
contractions.Meaning = contractions.Meaning.str.lower()
contractions_dict = contractions.to_dict()['Meaning']

# Defining regex patterns.
urlPattern = r"((http://)[^ ]*|(https://)[^ ]*|(www\.)[^ ]*)"
userPattern = r'@[^\s]+'
hashtagPattern = r'#[^\s]+'
alphaPattern = r"[^a-z0-9<>]"
sequencePattern = r"(.)\1\1+"
seqReplacePattern = r"\1\1"

# Defining regex for emojis
smileemoji = r"[8:=;]['`\-]?[)d]+"
sademoji = r"[8:=;]['`\-]?\(+"
neutralemoji = r"[8:=;]['`\-]?[\/|l*]"
lolemoji = r"[8:=;]['`\-]?p+"


def preprocess_apply(tweet):
    tweet = tweet.lower()
    # Replace all URls with '<url>'
    tweet = re.sub(urlPattern, '<url>', tweet)
    # Replace @USERNAME to '<user>'.
    tweet = re.sub(userPattern, '<user>', tweet)
    # Replace #Hashtags to '<hashtags>'.
    tweet = re.sub(userPattern, '<hashtag>', tweet)
    # Replace 3 or more consecutive letters by 2 letter.
    tweet = re.sub(sequencePattern, seqReplacePattern, tweet)
    # Replace all emojis.
    tweet = re.sub(r'<3', '<heart>', tweet)
    tweet = re.sub(smileemoji, '<smile>', tweet)
    tweet = re.sub(sademoji, '<sadface>', tweet)
    tweet = re.sub(neutralemoji, '<neutralface>', tweet)
    tweet = re.sub(lolemoji, '<lolface>', tweet)
    for contraction, replacement in contractions_dict.items():
        tweet = tweet.replace(contraction, replacement)
    # Remove non-alphanumeric and symbols
    tweet = re.sub(alphaPattern, ' ', tweet)
    # Adding space on either side of '/' to seperate words (After replacing URLS).
    tweet = re.sub(r'/', ' / ', tweet)
    return tweet


def predict(text):
    if isinstance(text, str):
        text = list(text, )
    processed_text = [preprocess_apply(t) for t in text]
    text = pad_sequences(tokenizer.texts_to_sequences(processed_text), maxlen=60)
    sentiment = model.predict(text)
    sentiment = np.where(sentiment > 0.5, 1, -1)
    return processed_text, sentiment