import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import re


POS_TAG = ['PROPN', 'ADJ', 'NOUN', 'VERB']
nlp = spacy.load("en_core_web_sm") # <----- this is the model


def pre_process(text):
    text = text.lower()
    text = re.sub("&lt;/?.*?&gt;"," &lt;&gt; ", text)
    text = re.sub("(\\d|\\W)+"," ",text)
    return text


def summarizeText(text, per):

    document = nlp(text)
    sentence_scores = dict()
    word_freq = dict()
    
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
    return summary


def get_keywords(text):

    keywords = list()
    keywords_count = dict()

    for chunk in range(len(text)//1000000+1):
        for token in nlp(text[chunk*1000000:(chunk+1)*1000000]):
            if token.text in nlp.Defaults.stop_words:
                continue
            if token.text in punctuation:
                continue
            if token.text in ["fig"]:
                continue
            if token.pos_ in POS_TAG:
                keyword = token.text
                if keyword in keywords_count:
                    keywords_count[keyword] += 1
                else:
                    keywords_count[keyword] = 1
                    keywords.append(keyword)

    keywords.sort(key=lambda x: keywords_count[x], reverse=True)
    return keywords
    
     
def classify(text):
    readData = text
    cleanedText = pre_process(readData)
    keywords = get_keywords(cleanedText)
    return keywords


# datafromFile = open("retroreport.txt", "r", encoding="utf8")
# readData = datafromFile.read()

# cleanedText = pre_process(readData)
# print(get_keywords(cleanedText, 10))