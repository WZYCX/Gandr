import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import re

datafromFile = open("C:/Users/tiech/Downloads/retroreport.txt", "r", encoding="utf8")

readData = datafromFile.read()

def pre_process(text):
    text = text.lower()
    text = re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)
    text = re.sub("(\\d|\\W)+"," ",text)
    
    return text

cleanedText = pre_process(readData)

nlp = spacy.load("en_core_web_sm") # <----- this is the model


def summarizeText(text, per):
    
    #constants
    document = nlp(text)
    sentence_scores = {}
    word_freq = {}
    tokens = [token.text for token in document]
    
    #algorithm
    
    for word in document:
        if word.text not in STOP_WORDS:
                if word.text not in word_freq.keys():
                    word_freq[word.text] = 1
                else:
                    word_freq[word.text] += 1
    max_freq = max(word_freq.values())
    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / max_freq
    sentence_tokens = [sent for sent in document.sents]
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_freq.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_freq[word.text.lower()]
                else:
                    sentence_scores[sent] += word_freq[word.text.lower()]
    select_length = int(len(sentence_tokens) * per)
    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    final_summary = [word.text for word in summary]
    summary = "".join(final_summary)
    
    
    
    #return
    return summary


def get_keywords(text):
    #constants
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB'] 
    document = nlp(text)
    
    #algorithm
    for token in document:
        if token.text in nlp.Defaults.stop_words or token.text in punctuation:
            continue
        if token.pos_ in pos_tag:
            result.append(token.text)
    return result
    
    
print(set(get_keywords(cleanedText)))
