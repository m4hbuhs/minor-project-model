import string
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

def preprocess(text):
    text = text.lower()
    text = "".join([c for c in text if c not in string.punctuation])
    
    stop_words = set(stopwords.words("english"))
    words = text.split()
    words = [w for w in words if w not in stop_words]
    
    return " ".join(words)