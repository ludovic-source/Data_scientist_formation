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

import re

# ----------------------------------------------------------------------------------------------------------------------------

def freq_stats_for_description(df):
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

def freq_stats_for_product_name(df):
    """
    Calcule les fréquences des mots du product_name à partir d'un DataFrame contenant les articles et le product_name.
    
    Args:
    - df (pd.DataFrame): DataFrame avec deux colonnes ['product_name', 'product_name'].
    
    Returns:
    - freq (dict): Fréquences des mots du product_name pour chaque article.
    - stats (pd.DataFrame): DataFrame des statistiques par article.
    """
    corpora = defaultdict(list)

    # tokenizer pour conserver uniquement les caractères alphanumériques
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    
    # Construction du corpus par image
    for _, row in df.iterrows():
        product = row['product_name']
        product_tokens = row['product_name']
        
        # Tokenisation de la description
        tokens = tokenizer.tokenize(product_tokens.lower())
        corpora[product] += tokens
    
    # Calcul des fréquences et des statistiques
    freq = {product: nltk.FreqDist(words) for product, words in corpora.items()}
    stats = {product: {'total': len(words), 'unique': len(nltk.FreqDist(words).keys())} for product, words in corpora.items()}
    
    # Conversion des statistiques en DataFrame
    stats_df = pd.DataFrame.from_dict(stats, orient='index')
    
    return freq, stats_df, corpora

# ----------------------------------------------------------------------------------------------------------------------------

def freq_stats_for_description_without_stopwords(df, sw):
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

def freq_stats_for_description_without_stopwords_and_with_lemmatizer(df, sw):
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

def process_text(df, sw, column):
    """
    Processes text data from a DataFrame, calculates word frequencies, and removes stopwords 
    while lemmatizing the words. It also filters out non-English words using a provided 
    dictionary of English words.

    This function takes a DataFrame with two columns, 'product_name' and column, 
    and applies the following steps:
    - Tokenizes the text from the column.
    - Lemmatizes each word in the column.
    - Removes stopwords (from the 'sw' set) and non-English words (not in 'english_words').
    - Calculates the word frequencies for each 'product_name' in the DataFrame.

    Args:
        df (pd.DataFrame): A DataFrame with two columns:
            - 'product_name': The name of the product.
            - 'description': The description of the product.
        sw (set): A set of stopwords to exclude from the word list.
        column (string) : name of column for the process.

    Returns:
        freq (dict): A dictionary where the keys are product names and the values are 
            frequency distributions of the words in the descriptions.
        stats (pd.DataFrame): A DataFrame with statistics for each product, 
            including total word count and unique word count.
        corpora (defaultdict): A dictionary where the keys are product names and the values 
            are lists of words from the column after lemmatization, stopword removal, 
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
        column_to_tokenize = row[column]
        
        # Tokenisation de la colonne demandée
        tokens = tokenizer.tokenize(column_to_tokenize.lower())
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

def process_final_text(df, sw, column):
    """
    Processes text data from a DataFrame, calculates word frequencies, and removes stopwords 
    while lemmatizing the words. It also filters out non-English words using a provided 
    dictionary of English words.

    This function takes a DataFrame with two columns, 'product_name' and column, 
    and applies the following steps:
    - Tokenizes the text from the column.
    - Lemmatizes each word in the column.
    - Removes stopwords (from the 'sw' set) and non-English words (not in 'english_words').
    - Remove words with one character
    - Calculates the word frequencies for each 'product_name' in the DataFrame.

    Args:
        df (pd.DataFrame): A DataFrame with two columns:
            - 'product_name': The name of the product.
            - 'description': The description of the product.
        sw (set): A set of stopwords to exclude from the word list.
        column (string) : name of column for the process.

    Returns:
        freq (dict): A dictionary where the keys are product names and the values are 
            frequency distributions of the words in the descriptions.
        stats (pd.DataFrame): A DataFrame with statistics for each product, 
            including total word count and unique word count.
        corpora (defaultdict): A dictionary where the keys are product names and the values 
            are lists of words from the column after lemmatization, stopword removal, 
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
        column_to_tokenize = row[column]
        
        # Tokenisation de la colonne demandée
        tokens = tokenizer.tokenize(column_to_tokenize.lower())
        # Lemmatisation des mots (tokens)
        lemmatized_tokens = [lemmatizer.lemmatize(w) for w in tokens]
        # Suppression des stopwords (sw) et des mots qui ne sont pas dans le dictionnaire anglais, 
        # et des mots de moins d'une lettre
        corpora[product] += [w for w in lemmatized_tokens if w not in sw and w in valid_words and len(w) > 1]
    
    # Calcul des fréquences et des statistiques
    freq = {product: nltk.FreqDist(words) for product, words in corpora.items()}
    stats = {product: {'total': len(words), 'unique': len(nltk.FreqDist(words).keys())} for product, words in corpora.items()}
    
    # Conversion des statistiques en DataFrame
    stats_df = pd.DataFrame.from_dict(stats, orient='index')
    
    return freq, stats_df, corpora


# ----------------------------------------------------------------------------------------------------------------------------

def create_set_personal_stopwords(most_common_words, unique, numerical):

    """
    Create a custom set of stopwords based on specific criteria.

    Args:
        most_common_words (list of tuples): List of tuples (word, frequency) for the corpus.
        unique (bool): Whether to add words with a frequency of 1 to the stopwords set.
        numerical (bool): Whether to add words containing only digits to the stopwords set.

    Returns:
        set: A custom set of stopwords.
    """    

    # On créé notre set de stopwords avec l'ensemble de stopwords par défaut présent dans la librairie NLTK
    sw = set()
    sw.update(tuple(nltk.corpus.stopwords.words('english')))

    if unique:
        # Suppression des mots présents une seule fois
        unique_tokens = []
        for word, count in most_common_words:
            if count == 1:
                unique_tokens.append(word)
        sw.update(unique_tokens)

    if numerical:
        # suppression des tokens avec des chiffres
        numerical_tokens = []
        for word, count in most_common_words:
            if word.isdigit():
                numerical_tokens.append(word)
        sw.update(numerical_tokens)

    return sw

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

# ----------------------------------------------------------------------------------------------------------------------------

def clean_category_first_level(category):

    """
    Extract the first-level category from a category string and clean it.

    This function takes a category string, extracts the portion before the
    first occurrence of '>>', and retains only alphanumeric characters and spaces.

    Args:
        category (str): The category string containing hierarchical levels.

    Returns:
        str: The cleaned first-level category as a string.
    """

    # Sélectionner la catégorie de premier niveau
    cat_first_level = category.split(">>")[0].strip()

    # Conserver uniquement les caractères alphanumériques et les espaces
    result = re.sub(r'[^a-zA-Z0-9 ]', '', cat_first_level)

    return result
