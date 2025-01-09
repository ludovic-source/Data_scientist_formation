import numpy as np

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

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