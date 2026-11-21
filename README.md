# 📞 ¿A quién llamar primero? Priorización de clientes en campañas bancarias

> **Machine Learning · Maestría en Ciencia de Datos e Inteligencia Artificial · EPG UNAJ**
> Docente: Dr. Alain Paul Herrera Urtiaga

**Equipo:** [Integrante 1] · [Integrante 2] · [Integrante 3]

🔗 **Demo:** [enlace a la app en Streamlit Community Cloud] · 📄 **Informes:** [Producto 1](informe/Producto1.md) · [Producto 2](informe/Producto2.md)

---

## 1. El problema

En una campaña de telemarketing, solo **11 de cada 100** clientes llamados aceptan abrir un depósito a plazo. Llamar a todos cuesta horas de call center y molesta a clientes que no están interesados.

**Pregunta:** *antes de llamar* a un cliente, ¿aceptará abrir un depósito a plazo?

- **Tipo de problema:** clasificación binaria (suscribe / no suscribe)
- **Métrica principal:** **PR-AUC**, porque el objetivo es **ordenar** la lista de llamadas y las clases están muy desbalanceadas (11 %). Reportamos también ROC-AUC, recall y precisión.

## 2. Los datos

| Campo | Detalle |
|---|---|
| Fuente | [Bank Marketing](https://archive.ics.uci.edu/dataset/222/bank+marketing) (UCI), archivo `bank-additional-full.csv` |
| Tamaño | 41 188 llamadas (mayo 2008 – noviembre 2010) |
| Variables usadas | 19: perfil del cliente, historial de contacto y contexto económico |
| Variable objetivo | `suscribe` (1 = abrió el depósito): **11,3 %** |

Excluimos `duracion_llamada` porque **solo se conoce después de llamar** (fuga de datos): con ella la PR-AUC sube de 0,44 a 0,58, pero el modelo sería inútil.

## 3. Resultados principales

| Modelo | PR-AUC (CV 5 folds) | ROC-AUC (CV 5 folds) |
|---|---|---|
| Baseline (clase mayoritaria) | 0,113 ± 0,000 | 0,500 ± 0,000 |
| k-NN (k = 25) | 0,412 ± 0,008 | 0,766 ± 0,008 |
| Regresión logística (L2) | 0,444 ± 0,009 | 0,790 ± 0,005 |
| LightGBM | 0,463 ± 0,010 | 0,791 ± 0,004 |
| Random Forest · *mejor del Producto 1* | 0,464 ± 0,010 | 0,790 ± 0,004 |
| Red neuronal (MLP 32-16) | 0,444 ± 0,010 | 0,787 ± 0,004 |
| **LightGBM optimizado con Optuna · modelo final** | **0,469 ± 0,016** *(5×5 folds)* | — |

**En el test**, el modelo final logra PR-AUC = **0,497** y ROC-AUC = **0,818**. Llamando solo al **10 %** de clientes con mayor probabilidad, el banco alcanza al **48 %** de los que suscriben, con una tasa de éxito de **54 %** (al azar: 11 %).

**Hallazgos clave:**
- La optimización mejora de forma **significativa pero pequeña**: LightGBM optimizado gana a Random Forest en 22 de 25 folds (Wilcoxon p < 0,001; +0,006 de PR-AUC).
- k-means encontró, sin conocer la respuesta, a los **clientes recontactados** (63 % suscribe) y a los **saturados** de llamadas (4 %).
- ⚠️ El modelo marca al **100 % de los mayores de 60 años**: hay que limitar la presión comercial sobre ese grupo.
- ⚠️ Con una **división temporal**, el modelo es solo 1,6 veces mejor que el azar (4,4 veces con división aleatoria): depende mucho del contexto económico.

## 4. Estructura del repositorio

```
├── README.md                          ← este archivo
├── data/README.md                     ← fuente y diccionario de variables
├── notebooks/
│   ├── 01_eda.ipynb                   ← análisis exploratorio (Producto 1)
│   ├── 02_modelos.ipynb               ← pipeline y comparación de 5 modelos (Producto 1)
│   ├── 03_optimizacion.ipynb          ← Optuna y comparación fold a fold (Producto 2)
│   ├── 04_no_supervisado_y_red.ipynb  ← segmentos, casos raros y red neuronal (Producto 2)
│   └── 05_interpretacion.ipynb        ← umbral, variables, sesgo, prueba temporal, modelo final (Producto 2)
├── app/                               ← demo en Streamlit y modelo guardado
├── informe/                           ← informes de los productos 1 y 2
└── docs/                              ← guías del curso
```

## 5. Cómo reproducir

1. Abrir cada notebook en Google Colab: **Archivo → Abrir cuaderno → GitHub** y pegar el enlace del repositorio.
2. Ejecutar en orden (**Entorno de ejecución → Ejecutar todas**). Los datos se descargan solos.
3. Demo local: `pip install -r app/requirements.txt` y luego `streamlit run app/app.py`.

## 6. Uso de IA generativa

[Declarar aquí cómo usaron asistentes de IA. Todo el código debe poder ser explicado por cualquier integrante.]

---

📘 **Guías del curso:** [Producto 1](docs/Producto1_guia.md) · [Producto 2](docs/Producto2_guia.md) · [GitHub con Colab](docs/Guia_GitHub_Colab.md)
