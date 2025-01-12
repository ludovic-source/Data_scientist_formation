import numpy as np

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import words
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

import wordcloud
from wordcloud import WordCloud

from collections import defaultdict
from collections import Counter

# ----------------------------------------------------------------------------------------------------------------------------

def freq_stats_from_dataframe(df):
    """
    Calcule les fréquences des mots à partir d'un DataFrame contenant les articles et descriptions.
    
    Args:
    - df (pd.DataFrame): DataFrame avec deux colonnes ['product_name', 'description'].
    
    Returns:
    - freq (dict): Fréquences des mots pour chaque article.
    - stats (pd.DataFrame): DataFrame des statistiques par article.
    """
    corpora = defaultdict(list)

    # tokenizer pour conserver uniquement les caractères alphanumériques
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    
    # Construction du corpus par image
    for _, row in df.iterrows():
        product = row['product_name']
        description = row['description']
        
        # Tokenisation de la description
        tokens = tokenizer.tokenize(description.lower())
        corpora[product] += tokens
    
    # Calcul des fréquences et des statistiques
    freq = {product: nltk.FreqDist(words) for product, words in corpora.items()}
    stats = {product: {'total': len(words), 'unique': len(nltk.FreqDist(words).keys())} for product, words in corpora.items()}
    
    # Conversion des statistiques en DataFrame
    stats_df = pd.DataFrame.from_dict(stats, orient='index')
    
    return freq, stats_df, corpora

# ----------------------------------------------------------------------------------------------------------------------------

def freq_stats_from_dataframe_without_stopwords(df, sw):
    """
    Calcule les fréquences des mots à partir d'un DataFrame contenant les articles et descriptions, sans les stopwords.
    
    Args:
    - df (pd.DataFrame): DataFrame avec deux colonnes ['product_name', 'description'].
    
    Returns:
    - freq (dict): Fréquences des mots pour chaque article.
    - stats (pd.DataFrame): DataFrame des statistiques par article.
    """
    corpora = defaultdict(list)

    # tokenizer pour conserver uniquement les caractères alphanumériques
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    
    # Construction du corpus par image
    for _, row in df.iterrows():
        product = row['product_name']
        description = row['description']
        
        # Tokenisation de la description
        tokens = tokenizer.tokenize(description.lower())
        corpora[product] += [w for w in tokens if not w in sw]
    
    # Calcul des fréquences et des statistiques
    freq = {product: nltk.FreqDist(words) for product, words in corpora.items()}
    stats = {product: {'total': len(words), 'unique': len(nltk.FreqDist(words).keys())} for product, words in corpora.items()}
    
    # Conversion des statistiques en DataFrame
    stats_df = pd.DataFrame.from_dict(stats, orient='index')
    
    return freq, stats_df, corpora

# ----------------------------------------------------------------------------------------------------------------------------

def freq_stats_from_dataframe_without_stopwords_and_with_lemmatizer(df, sw):
    """
    Calcule les fréquences des mots à partir d'un DataFrame contenant les articles et descriptions, sans les stopwords, et en lemmatisant les mots.
    
    Args:
    - df (pd.DataFrame): DataFrame avec deux colonnes ['product_name', 'description'].
    
    Returns:
    - freq (dict): Fréquences des mots pour chaque article.
    - stats (pd.DataFrame): DataFrame des statistiques par article.
    """
    # Initialiser le lemmatizer
    lemmatizer = WordNetLemmatizer()

    # tokenizer pour conserver uniquement les caractères alphanumériques
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    
    corpora = defaultdict(list)
    
    # Construction du corpus par image
    for _, row in df.iterrows():
        product = row['product_name']
        description = row['description']
        
        # Tokenisation de la description
        tokens = tokenizer.tokenize(description.lower())
        # Lemmatisation des mots (tokens)
        lemmatized_tokens = [lemmatizer.lemmatize(w) for w in tokens]
        # Suppression des stopwords (sw)
        corpora[product] += [w for w in lemmatized_tokens if w not in sw]
    
    # Calcul des fréquences et des statistiques
    freq = {product: nltk.FreqDist(words) for product, words in corpora.items()}
    stats = {product: {'total': len(words), 'unique': len(nltk.FreqDist(words).keys())} for product, words in corpora.items()}
    
    # Conversion des statistiques en DataFrame
    stats_df = pd.DataFrame.from_dict(stats, orient='index')
    
    return freq, stats_df, corpora

# ----------------------------------------------------------------------------------------------------------------------------

def process_text(df, sw):
    """
    Processes text data from a DataFrame, calculates word frequencies, and removes stopwords 
    while lemmatizing the words. It also filters out non-English words using a provided 
    dictionary of English words.

    This function takes a DataFrame with two columns, 'product_name' and 'description', 
    and applies the following steps:
    - Tokenizes the text from the 'description' column.
    - Lemmatizes each word in the description.
    - Removes stopwords (from the 'sw' set) and non-English words (not in 'english_words').
    - Calculates the word frequencies for each 'product_name' in the DataFrame.

    Args:
        df (pd.DataFrame): A DataFrame with two columns:
            - 'product_name': The name of the product.
            - 'description': The description of the product.
        sw (set): A set of stopwords to exclude from the word list.

    Returns:
        freq (dict): A dictionary where the keys are product names and the values are 
            frequency distributions of the words in the descriptions.
        stats (pd.DataFrame): A DataFrame with statistics for each product, 
            including total word count and unique word count.
        corpora (defaultdict): A dictionary where the keys are product names and the values 
            are lists of words from the descriptions after lemmatization, stopword removal, 
            and English word filtering.
    """

    # Initialiser le lemmatizer
    lemmatizer = WordNetLemmatizer()

    # tokenizer pour conserver uniquement les caractères alphanumériques
    tokenizer = nltk.RegexpTokenizer(r'\w+')

    # Télécharger le dictionnaire de mots si vous ne l'avez pas encore fait
    nltk.download('words')

    # Liste des mots valides en anglais (dictionnaire de NLTK)
    valid_words = set(words.words())
    
    corpora = defaultdict(list)
    
    # Construction du corpus par image
    for _, row in df.iterrows():
        product = row['product_name']
        description = row['description']
        
        # Tokenisation de la description
        tokens = tokenizer.tokenize(description.lower())
        # Lemmatisation des mots (tokens)
        lemmatized_tokens = [lemmatizer.lemmatize(w) for w in tokens]
        # Suppression des stopwords (sw) et des mots qui ne sont pas dans le dictionnaire anglais
        corpora[product] += [w for w in lemmatized_tokens if w not in sw and w in valid_words]
    
    # Calcul des fréquences et des statistiques
    freq = {product: nltk.FreqDist(words) for product, words in corpora.items()}
    stats = {product: {'total': len(words), 'unique': len(nltk.FreqDist(words).keys())} for product, words in corpora.items()}
    
    # Conversion des statistiques en DataFrame
    stats_df = pd.DataFrame.from_dict(stats, orient='index')
    
    return freq, stats_df, corpora

# ----------------------------------------------------------------------------------------------------------------------------

def process_text_2(df, sw):
    """
    Processes text data from a DataFrame, calculates word frequencies, and removes stopwords 
    while lemmatizing the words. It also filters out non-English words using a provided 
    dictionary of English words.

    This function takes a DataFrame with two columns, 'product_name' and 'description', 
    and applies the following steps:
    - Tokenizes the text from the 'description' column.
    - Lemmatizes each word in the description.
    - Removes stopwords (from the 'sw' set) and non-English words (not in 'english_words').
    - Removes words with only one character.
    - Calculates the word frequencies for each 'product_name' in the DataFrame.

    Args:
        df (pd.DataFrame): A DataFrame with two columns:
            - 'product_name': The name of the product.
            - 'description': The description of the product.
        sw (set): A set of stopwords to exclude from the word list.

    Returns:
        freq (dict): A dictionary where the keys are product names and the values are 
            frequency distributions of the words in the descriptions.
        stats (pd.DataFrame): A DataFrame with statistics for each product, 
            including total word count and unique word count.
        corpora (defaultdict): A dictionary where the keys are product names and the values 
            are lists of words from the descriptions after lemmatization, stopword removal, 
            and English word filtering.
    """

    # Initialiser le lemmatizer
    lemmatizer = WordNetLemmatizer()

    # tokenizer pour conserver uniquement les caractères alphanumériques
    tokenizer = nltk.RegexpTokenizer(r'\w+')

    # Télécharger le dictionnaire de mots si vous ne l'avez pas encore fait
    nltk.download('words')

    # Liste des mots valides en anglais (dictionnaire de NLTK)
    valid_words = set(words.words())
    
    corpora = defaultdict(list)
    
    # Construction du corpus par image
    for _, row in df.iterrows():
        product = row['product_name']
        description = row['description']
        
        # Tokenisation de la description
        tokens = tokenizer.tokenize(description.lower())
        # Lemmatisation des mots (tokens)
        lemmatized_tokens = [lemmatizer.lemmatize(w) for w in tokens]
        # Suppression des stopwords (sw) et des mots qui ne sont pas dans le dictionnaire anglais,
        # et des mots d'un seul caractère
        corpora[product] += [w for w in lemmatized_tokens if w not in sw and w in valid_words and len(w) > 1]
    
    # Calcul des fréquences et des statistiques
    freq = {product: nltk.FreqDist(words) for product, words in corpora.items()}
    stats = {product: {'total': len(words), 'unique': len(nltk.FreqDist(words).keys())} for product, words in corpora.items()}
    
    # Conversion des statistiques en DataFrame
    stats_df = pd.DataFrame.from_dict(stats, orient='index')
    
    return freq, stats_df, corpora

# ----------------------------------------------------------------------------------------------------------------------------

# Obtenir le classement des mots les plus présents
def get_most_common_words(freq):
    """
    Récupère les mots les plus fréquents sur tout le corpus.
    
    Args:
    - freq (dict): Dictionnaire des fréquences pour chaque article.
    
    Returns:
    - sorted_words (list): Liste des mots triés par fréquence (mot, fréquence).
    """
    # Combiner toutes les fréquences dans un Counter global
    total_freq = Counter()
    for product, product_freq in freq.items():
        total_freq.update(product_freq)
    
    # Trier par fréquence et retourner
    return total_freq.most_common()

# ----------------------------------------------------------------------------------------------------------------------------

def print_wordcloud(words):

    """
    Generates and displays a word cloud from a Counter of word frequencies.

    This function accepts a `Counter` object where each key is a word and the 
    associated value is the frequency of that word. It then generates a word 
    cloud image, which is displayed using Matplotlib.

    Parameters:
        words (Counter): A `Counter` object containing words as keys and their
                          frequencies as values. The `Counter` is typically generated
                          by counting word occurrences in a text or dataset.

    Returns:
        None: This function does not return any value. It generates and displays 
              the word cloud image.
    
    Example:
        freq = Counter({'python': 10, 'data': 5, 'science': 3})
        print_wordcloud(freq)

    Raises:
        ValueError: If the `words` parameter is not a `Counter` object.
    """

    # Créer un Counter pour combiner toutes les fréquences
    combined_frequencies = Counter()
    
    # Ajouter chaque mot avec sa fréquence au Counter
    for word, nb in words.items():  # Utilisez .items() pour décomposer le Counter
        combined_frequencies[word] += nb
    
    # Générer le nuage de mots
    wordcloud = WordCloud(
        background_color='white',
        width=800,
        height=400,
        colormap='viridis'
    ).generate_from_frequencies(combined_frequencies)

    # Afficher le nuage de mots
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    