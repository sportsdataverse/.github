# Sharing and Publishing Notebooks

## nbconvert

```bash
# Convert to HTML
jupyter nbconvert notebook.ipynb --to html

# Convert to PDF
jupyter nbconvert notebook.ipynb --to pdf

# Convert to script
jupyter nbconvert notebook.ipynb --to script
```

## Quarto for Publication

```bash
# Install Quarto
# https://quarto.org/

# Render to HTML/PDF/Word
quarto render notebook.ipynb

# Render with custom theme
quarto render notebook.ipynb --to html --theme cosmo
```

## Voilà for Interactive Dashboards

```bash
pip install voila
voila notebook.ipynb
```

Strips code cells, shows only outputs and widgets.

## Sharing Platforms

- **GitHub** — Native .ipynb rendering
- **Nbviewer** — Public notebook sharing (https://nbviewer.org/)
- **Google Colab** — Share with `File > Share`
- **Hugging Face Spaces** — Gradio/Streamlit from notebooks
