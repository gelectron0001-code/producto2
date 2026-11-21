# Demo · ¿A quién llamar primero?

`modelo.joblib` guarda el pipeline completo (preprocesamiento + LightGBM optimizado) y el umbral de decisión, generado al final de [`05_interpretacion.ipynb`](../notebooks/05_interpretacion.ipynb).

## Probarla en su computadora
```
pip install -r app/requirements.txt
streamlit run app/app.py
```

## Publicarla gratis en Streamlit Community Cloud
1. Entren a [share.streamlit.io](https://share.streamlit.io) con su cuenta de GitHub.
2. **Create app** → elijan este repositorio → **Main file path:** `app/app.py`.
3. **Deploy** y copien el enlace en el README principal.

**Importante:** la versión de scikit-learn de `requirements.txt` debe ser la misma con la que se guardó `modelo.joblib`. Si regeneran el modelo en Colab, ejecuten `import sklearn; print(sklearn.__version__)` y actualicen el número.
