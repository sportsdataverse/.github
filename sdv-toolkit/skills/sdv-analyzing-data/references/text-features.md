# Text Feature Engineering

## Bag-of-Words

```python
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

# Count
count = CountVectorizer(max_features=1000, ngram_range=(1, 2))
X_count = count.fit_transform(texts)

# TF-IDF
tfidf = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
X_tfidf = tfidf.fit_transform(texts)
```

## Word Embeddings

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(texts, show_progress_bar=True)
```

## Basic Text Stats

```python
df['text_length'] = df['text'].str.len()
df['word_count'] = df['text'].str.split().str.len()
df['avg_word_length'] = df['text'].apply(lambda x: np.mean([len(w) for w in x.split()]))
```
