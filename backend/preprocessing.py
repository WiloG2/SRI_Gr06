import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Descargas necesarias
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Inicialización
tokenizer = RegexpTokenizer(r'[a-zA-Z]+')  # Solo palabras alfabéticas, sin números ni puntuación
stop_words = set(stopwords.words('english'))  # Convertimos el listado de stopwords en un set para mejorar la búsqueda
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    # 1. Convertir a minúsculas
    text = text.lower()

    # 2. Tokenización usando la nueva expresión regular para solo palabras alfabéticas
    tokens = tokenizer.tokenize(text)

    # 3. Eliminar stopwords de forma eficiente
    filtered_tokens = [token for token in tokens if token not in stop_words]

    # 4. Lematización
    tokens = [lemmatizer.lemmatize(t) for t in filtered_tokens]

    # 5. Reconstrucción del texto
    clean_text = ' '.join(tokens)
    return clean_text