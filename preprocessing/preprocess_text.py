import nltk
import spacy # type: ignore
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK resources (if not already downloaded)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Function to preprocess the text
def preprocess_text(text):
    # Lowercase the text
    text = text.lower()

    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    # Lemmatize tokens
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]

    # Join the tokens back into a string
    cleaned_text = ' '.join(lemmatized_tokens)
    
    return cleaned_text

# Load transcript
transcript_path = 'data/transcripts/sample_transcript.txt'
with open(transcript_path, 'r') as file:
    transcript = file.read()

# Preprocess the transcript
preprocessed_text = preprocess_text(transcript)

# Save the preprocessed text
processed_text_path = 'data/transcripts/sample_preprocessed_transcript.txt'
with open(processed_text_path, 'w') as file:
    file.write(preprocessed_text)

print(f"Preprocessed text saved at: {processed_text_path}")
