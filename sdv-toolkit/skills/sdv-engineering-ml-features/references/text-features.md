# Text Feature Engineering

Complete guide to extracting features from text data.

## Bag-of-Words: Count Vectorizer

```python
from sklearn.feature_extraction.text import CountVectorizer

# Basic count vectorization
vectorizer = CountVectorizer()
X_counts = vectorizer.fit_transform(texts)

# With parameters
vectorizer = CountVectorizer(
    max_features=1000,        # Limit vocabulary size
    ngram_range=(1, 2),       # Unigrams and bigrams
    min_df=2,                 # Ignore terms appearing in <2 documents
    max_df=0.95,              # Ignore terms in >95% of documents
    stop_words='english'      # Remove common English stop words
)
X_counts = vectorizer.fit_transform(texts)
```

## TF-IDF Vectorization

Preferred over raw counts for most applications:

```python
from sklearn.feature_extraction.text import TfidfVectorizer

# Basic TF-IDF
vectorizer = TfidfVectorizer()
X_tfidf = vectorizer.fit_transform(texts)

# With parameters
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),       # Unigrams + bigrams
    min_df=5,
    max_df=0.9,
    stop_words='english',
    sublinear_tf=True         # Apply sublinear tf scaling (1 + log(tf))
)
X_tfidf = vectorizer.fit_transform(texts)
```

**TF-IDF formula:** TF × IDF = (term frequency) × log(N / document frequency)

## Text Preprocessing Pipeline

```python
import re
from sklearn.feature_extraction.text import TfidfVectorizer

def preprocess_text(text):
    """Custom text preprocessing."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\d+', '', text)       # Remove numbers
    return text

# With custom preprocessor
vectorizer = TfidfVectorizer(
    preprocessor=preprocess_text,
    max_features=1000
)
```

## Word Embeddings

### Sentence Transformers (Recommended)

```python
from sentence_transformers import SentenceTransformer

# Load pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dimensions, fast
# OR
model = SentenceTransformer('all-mpnet-base-v2') # 768 dimensions, more accurate

# Encode texts
embeddings = model.encode(
    texts,
    show_progress_bar=True,
    batch_size=32,
    convert_to_numpy=True
)
```

**Common models:**
| Model | Dimensions | Speed | Quality |
|---|---|---|---|
| all-MiniLM-L6-v2 | 384 | Fast | Good |
| all-mpnet-base-v2 | 768 | Medium | Best |
| paraphrase-MiniLM-L3-v2 | 384 | Very fast | Good |

### Hugging Face Transformers

```python
from transformers import AutoTokenizer, AutoModel
import torch

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
model = AutoModel.from_pretrained('distilbert-base-uncased')

# Tokenize and encode
tokens = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')
with torch.no_grad():
    outputs = model(**tokens)
    # Use [CLS] token embedding or mean pooling
    embeddings = outputs.last_hidden_state[:, 0, :].numpy()
```

## Character-Level Features

```python
# Character-level TF-IDF (good for catching typos, patterns)
char_vectorizer = TfidfVectorizer(
    analyzer='char',
    ngram_range=(3, 5),       # Character n-grams
    max_features=5000
)
X_char = char_vectorizer.fit_transform(texts)
```

## Basic Text Statistics

```python
import numpy as np

def extract_text_stats(df, text_col):
    """Extract basic text statistics."""
    df = df.copy()
    
    # Length features
    df['text_length'] = df[text_col].str.len()
    df['word_count'] = df[text_col].str.split().str.len()
    
    # Average word length
    df['avg_word_length'] = df[text_col].apply(
        lambda x: np.mean([len(w) for w in x.split()]) if x.split() else 0
    )
    
    # Character type counts
    df['uppercase_count'] = df[text_col].apply(lambda x: sum(1 for c in x if c.isupper()))
    df['digit_count'] = df[text_col].apply(lambda x: sum(1 for c in x if c.isdigit()))
    df['punctuation_count'] = df[text_col].apply(lambda x: sum(1 for c in x if c in '.,!?;:'))
    
    # Ratios (guard against division by zero)
    df['uppercase_ratio'] = np.where(
        df['text_length'] > 0,
        df['uppercase_count'] / df['text_length'],
        0.0
    )
    
    return df
```

## Domain-Specific Features

```python
import re

def extract_domain_features(df, text_col):
    """Extract domain-specific text features."""
    df = df.copy()
    
    # Email indicators
    df['has_email'] = df[text_col].str.contains(r'\S+@\S+', regex=True, na=False)
    
    # URL indicators
    df['has_url'] = df[text_col].str.contains(r'http[s]?://', regex=True, na=False)
    df['url_count'] = df[text_col].str.count(r'http[s]?://')
    
    # Mention/hashtag counts (social media)
    df['mention_count'] = df[text_col].str.count(r'@\w+')
    df['hashtag_count'] = df[text_col].str.count(r'#\w+')
    
    # Question/exclamation indicators
    df['is_question'] = df[text_col].str.contains(r'\?', na=False)
    df['exclamation_count'] = df[text_col].str.count('!')
    
    return df
```

## Feature Selection for Text

```python
from sklearn.feature_selection import SelectKBest, chi2, mutual_info_classif

# Chi-square for classification (selects features most correlated with target)
selector = SelectKBest(chi2, k=1000)
X_selected = selector.fit_transform(X_tfidf, y)

# Mutual information (works for any supervised task)
selector = SelectKBest(mutual_info_classif, k=1000)
X_selected = selector.fit_transform(X_tfidf, y)
```

## Combining Text and Structured Features

```python
from scipy.sparse import hstack
from sklearn.compose import ColumnTransformer

# Method 1: Combine sparse matrices
X_combined = hstack([X_tfidf, X_structured])

# Method 2: ColumnTransformer in pipeline
preprocessor = ColumnTransformer([
    ('text', TfidfVectorizer(max_features=1000), 'text_column'),
    ('num', StandardScaler(), numeric_columns),
    ('cat', OneHotEncoder(), categorical_columns)
])
```

## Embeddings vs TF-IDF Selection

| Approach | Best For | Pros | Cons |
|---|---|---|---|
| **TF-IDF** | Classification, interpretability | Fast, sparse, interpretable | Loses semantics, word order |
| **Embeddings** | Semantic similarity, clustering | Captures meaning, transferable | Dense, less interpretable |

## Complete Pipeline Example

```python
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# Simple text classification pipeline
text_clf = Pipeline([
    ('tfidf', TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        min_df=2
    )),
    ('clf', RandomForestClassifier(n_estimators=100))
])

text_clf.fit(train_texts, train_labels)
predictions = text_clf.predict(test_texts)
```
