# Matplotlib Advanced Patterns

## Subplots and Layouts

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

for idx, ax in enumerate(axes):
    ax.plot(x, y)
    ax.set_title(f"Subplot {idx}")

plt.tight_layout()
```

## Annotations

```python
ax.annotate('Peak', xy=(x_peak, y_peak), 
            xytext=(x_peak+1, y_peak+1),
            arrowprops=dict(arrowstyle='->', color='red'))
```

## Custom Styles

```python
plt.style.use('seaborn-v0_8-whitegrid')
# Or create your own style file
plt.style.use('./my_style.mplstyle')
```
