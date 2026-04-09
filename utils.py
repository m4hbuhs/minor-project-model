import string
from nltk.corpus import stopwords

# Load stopwords only ONCE at module import
stop_words = set(stopwords.words("english"))

def preprocess(text):
    text = text.lower()
    # Remove punctuation
    text = "".join([c for c in text if c not in string.punctuation])
    # Split into words
    words = text.split()
    # Remove stopwords (using the pre-loaded set - much faster)
    words = [w for w in words if w not in stop_words]
    
    return " ".join(words)