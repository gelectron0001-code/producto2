# ¿A quién llamar primero? Priorización de clientes en campañas bancarias
## Producto 1 · Informe técnico de modelado supervisado

**Equipo:** [Integrante 1] · [Integrante 2] · [Integrante 3]
**Repositorio:** [enlace de GitHub]

---

## 1. Problema y contexto

Los bancos promocionan productos de ahorro, como los depósitos a plazo, mediante campañas de telemarketing. Solo una pequeña parte de los clientes llamados acepta, así que la mayoría de las llamadas consume tiempo del call center sin resultado y puede molestar al cliente.

**Pregunta:** *antes de llamar* a un cliente, ¿aceptará abrir un depósito a plazo?

Con esta predicción, el banco puede **ordenar la lista de llamadas** y empezar por los clientes con mayor probabilidad. Es un problema de **clasificación binaria**.

## 2. Datos

**Fuente:** *Bank Marketing*, UCI Machine Learning Repository (Moro et al., 2014), archivo `bank-additional-full.csv`.
**Tamaño:** 41 188 llamadas de un banco portugués (mayo 2008 – noviembre 2010). **Variable objetivo:** `suscribe` (1 = abrió el depósito), presente en el **11,3 %** de los casos.

Usamos 19 variables conocidas **antes de la llamada**: perfil del cliente (edad, ocupación, estado civil, educación, créditos), historial de contacto (llamadas en esta campaña, contactos previos, resultado anterior, días desde el último contacto, canal, mes y día) y cinco indicadores económicos del mes.

**Hallazgos del análisis exploratorio** (`notebooks/01_eda.ipynb`):

1. **Clases muy desbalanceadas:** solo el 11 % suscribe. Un modelo que diga siempre "no" tendría 89 % de accuracy sin detectar a nadie; por eso no usamos la accuracy.
2. **El historial manda:** quienes aceptaron en la campaña anterior suscriben en un **65 %**; quienes nunca fueron contactados, en un **9 %**.
3. **El contexto económico pesa:** con euribor menor a 1 % suscribe el **46 %**; con euribor mayor a 4 %, solo el **5 %**.
4. **Insistir no funciona:** la tasa cae de **13 %** con una llamada a **3 %** con más de diez llamadas en la misma campaña.
5. **Datos incompletos codificados:** `pdays = 999` (nunca contactado) aparece en el 96 % de las filas, y `unknown` en el 21 % de `en_mora`.

## 3. Métrica de éxito

**Métrica principal: PR-AUC (average precision).**

**Justificación:** el banco no necesita un "sí/no" perfecto, sino una **lista ordenada** para llamar primero a los mejores candidatos. Con solo 11 % de positivos, el ROC-AUC se ve optimista porque premia ordenar bien la enorme masa de negativos; la PR-AUC, en cambio, mide qué tan "limpia" queda la parte alta de la lista. Un modelo al azar tiene PR-AUC ≈ 0,11. Reportamos además **ROC-AUC**, **recall** y **precisión**.

## 4. Preprocesamiento

| Tipo | Columnas | Tratamiento |
|---|---|---|
| Numéricas (9) | edad, llamadas, contactos previos, días desde el último contacto, indicadores económicos | 999 → faltante; imputar con la mediana **+ indicador de faltante**; escalar |
| Categóricas (10) | ocupación, estado civil, educación, créditos, canal, mes, día, resultado previo | One-hot con `handle_unknown="ignore"`; `unknown` se mantiene como categoría |

El indicador de faltante convierte el código 999 en una variable útil: "nunca fue contactado".

**Cómo evitamos la fuga de datos:**
- Todo el preprocesamiento va **dentro de un `Pipeline`** con `ColumnTransformer`, así que se aprende solo con el train de cada fold.
- **Excluimos `duracion_llamada`**, que solo existe después de la llamada. Lo comprobamos: con ella la PR-AUC de la logística sube de 0,444 a 0,581, una mejora falsa.
- Separamos un **20 % de test** estratificado al inicio y lo usamos **una sola vez**.

## 5. Modelos comparados

| Modelo | Por qué lo incluimos |
|---|---|
| Baseline (clase mayoritaria) | Punto de referencia mínimo |
| Regresión logística (L2) | Modelo lineal regularizado, simple e interpretable |
| k-NN (k = 25) | Modelo basado en distancias |
| Random Forest (300 árboles) | Ensamble de bagging |
| LightGBM | Ensamble de boosting |

Los modelos usan `class_weight="balanced"` cuando lo permiten. **Validación:** validación cruzada estratificada de 5 folds sobre el 80 % de entrenamiento.

## 6. Resultados

| Modelo | PR-AUC | ROC-AUC | Recall | Precisión |
|---|---|---|---|---|
| Baseline | 0,113 ± 0,000 | 0,500 ± 0,000 | 0,000 ± 0,000 | 0,000 ± 0,000 |
| k-NN (k = 25) | 0,412 ± 0,008 | 0,766 ± 0,008 | 0,242 ± 0,014 | 0,632 ± 0,014 |
| Regresión logística (L2) | 0,444 ± 0,009 | 0,790 ± 0,005 | 0,623 ± 0,006 | 0,350 ± 0,006 |
| LightGBM | 0,463 ± 0,010 | 0,791 ± 0,004 | 0,617 ± 0,007 | 0,379 ± 0,004 |
| **Random Forest** | **0,464 ± 0,010** | **0,790 ± 0,004** | **0,607 ± 0,013** | **0,394 ± 0,006** |

**Mejor modelo: Random Forest**, empatado en la práctica con LightGBM. k-NN tiene buena precisión pero recall muy bajo, porque no usa ponderación de clases.

**Resultado en el test:** PR-AUC = **0,490**, ROC-AUC = **0,808**, recall = 0,638 y precisión = 0,420, en línea con la validación cruzada.

En lenguaje sencillo: **si el banco llama solo al 10 % de clientes que el modelo pone primero, alcanza al 48 % de todos los que suscribirían, y uno de cada dos llamados acepta** (contra uno de cada nueve llamando al azar).

## 7. Conclusiones y próximos pasos

- Un modelo de árboles ordena a los clientes cuatro veces mejor que el azar, usando solo información disponible antes de llamar.
- La variable más tentadora, la duración de la llamada, era una fuga de datos: identificarla fue tan importante como elegir el modelo.
- **Para el Producto 2:** optimizar LightGBM con Optuna y comprobar fold a fold si supera a Random Forest; elegir un umbral de decisión; segmentar a los clientes con k-means; comparar con una red neuronal y revisar si el modelo trata distinto a algún grupo de edad.

---

**Referencia:** Moro, S., Rita, P. y Cortez, P. (2014). *Bank Marketing* [Conjunto de datos]. UCI Machine Learning Repository. https://doi.org/10.24432/C5K306

**Uso de IA generativa:** [declarar aquí]
