# Streamlit Advanced Patterns

## Caching

```python
import streamlit as st

@st.cache_data
def load_data(path):
    return pd.read_parquet(path)

@st.cache_resource
def load_model():
    return pickle.load(open("model.pkl", "rb"))
```

## Multipage Apps

```
app/
├── pages/
│   ├── 1_Data_Explorer.py
│   ├── 2_Model_Demo.py
│   └── 3_Analytics.py
└── Home.py
```

## Secrets Management

```toml
# .streamlit/secrets.toml
openai_api_key = "..."
```

## Custom Components

```bash
pip install streamlit-aggrid streamlit-echarts
```
