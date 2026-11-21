# Priorización de clientes en campañas de telemarketing bancario con aprendizaje automático
## Producto 2 · Proyecto integrador final

**Autores:** [Integrante 1] · [Integrante 2] · [Integrante 3]
**Repositorio:** [enlace de GitHub] · **Demo:** [enlace]

---

## Resumen

Las campañas de telemarketing bancario tienen tasas de éxito bajas: en nuestros datos, solo 11 % de los clientes llamados abre un depósito a plazo. Este trabajo construye un modelo que, antes de llamar, estima la probabilidad de que un cliente acepte, para ordenar la lista de llamadas. Usamos 41 188 llamadas del repositorio UCI y 19 variables de perfil, historial de contacto y contexto económico, y excluimos la duración de la llamada por ser fuga de datos. Comparamos cinco modelos supervisados con validación cruzada estratificada y la métrica PR-AUC. Optimizamos LightGBM con Optuna, que superó a Random Forest en 22 de 25 folds (Wilcoxon p < 0,001), con una mejora pequeña (+0,006). En el test, el modelo final logró PR-AUC = 0,497 y ROC-AUC = 0,818: llamando al 10 % de clientes mejor ubicados se alcanza al 48 % de los suscriptores. k-means identificó, sin usar la respuesta, un segmento de clientes recontactados con 63 % de éxito y otro de clientes saturados con 4 %. La revisión ética muestra que el modelo prioriza a todos los mayores de 60 años, y una prueba temporal revela una fuerte dependencia del contexto económico.

**Palabras clave:** marketing bancario, priorización de clientes, datos desbalanceados, aprendizaje automático, validación temporal.

## 1. Introducción

Las campañas de marketing directo son una forma común de vender productos financieros, pero su eficiencia es baja: la mayoría de las llamadas no termina en una venta, consume horas del call center y puede deteriorar la relación con el cliente. Moro, Cortez y Rita (2014) mostraron que modelos de aprendizaje automático entrenados con datos de campañas anteriores pueden mejorar la selección de clientes.

Este trabajo amplía el Producto 1 con optimización de hiperparámetros, tratamiento del desbalance mediante el umbral de decisión, análisis no supervisado, una red neuronal, interpretación del modelo, revisión de sesgo, una prueba de robustez temporal y una demo funcional.

## 2. Datos

Usamos *Bank Marketing* (UCI), versión `bank-additional-full.csv`: 41 188 llamadas de un banco portugués entre mayo de 2008 y noviembre de 2010, de las cuales el **11,3 %** terminó en suscripción. Empleamos 19 variables conocidas antes de la llamada y **excluimos la duración de la llamada**, que el propio repositorio advierte que debe descartarse en un modelo predictivo realista. El código 999 de `pdays` (nunca contactado) se trató como faltante con indicador.

## 3. Método

### 3.1 Preprocesamiento
Pipeline con `ColumnTransformer`: para las numéricas, imputación con la mediana más indicador de faltante y escalado; para las categóricas, one-hot con `handle_unknown="ignore"`, manteniendo `unknown` como categoría.

### 3.2 Validación y métrica
División 80/20 estratificada; el test se usó una sola vez. Validación cruzada estratificada de 5 folds para comparar modelos y de **5 folds × 5 repeticiones** para la comparación estadística (prueba de Wilcoxon). Métrica principal: **PR-AUC**, adecuada para ordenar con clases desbalanceadas.

### 3.3 Optimización y desbalance
Optimizamos LightGBM con Optuna (30 intentos, muestreador TPE) sobre ocho hiperparámetros: número de árboles, tasa de aprendizaje, número de hojas, mínimo de casos por hoja, submuestreo de filas y columnas, regularización L2 y **`class_weight`** (ninguno o balanceado). Así, el tratamiento del desbalance se eligió con datos, no a priori. El umbral de decisión se eligió maximizando **F2** sobre probabilidades de validación cruzada en train.

## 4. Experimentos y resultados

### 4.1 Comparación de modelos

| Modelo | PR-AUC | ROC-AUC |
|---|---|---|
| Baseline | 0,113 ± 0,000 | 0,500 ± 0,000 |
| k-NN (k = 25) | 0,412 ± 0,008 | 0,766 ± 0,008 |
| Regresión logística (L2) | 0,444 ± 0,009 | 0,790 ± 0,005 |
| Red neuronal (MLP 32-16) | 0,444 ± 0,010 | 0,787 ± 0,004 |
| LightGBM original | 0,463 ± 0,010 | 0,791 ± 0,004 |
| Random Forest (modelo del Producto 1) | 0,464 ± 0,010 | 0,790 ± 0,004 |
| **LightGBM optimizado** | **0,472** *(CV 5 folds de Optuna)* | — |

### 4.2 ¿La mejora es real?

| Comparación (5 folds × 5 repeticiones) | PR-AUC media | Folds ganados | Diferencia | Wilcoxon |
|---|---|---|---|---|
| LightGBM optimizado vs. LightGBM original | 0,469 vs. 0,462 | 22 de 25 | +0,007 | p < 0,001 |
| LightGBM optimizado vs. Random Forest | 0,469 vs. 0,463 | 22 de 25 | +0,006 | p < 0,001 |

La mejora es **estadísticamente real pero pequeña**. Adoptamos LightGBM optimizado porque no agrega complejidad frente a Random Forest. Optuna eligió `class_weight=None`: para una métrica de ordenamiento no hace falta reponderar, y el desbalance se resolvió con el umbral.

La red neuronal no supera a los ensambles de árboles, algo esperable en datos de tabla.

### 4.3 Umbral y resultado en el test

Con el umbral **0,10** (máximo F2 en validación cruzada), el modelo final obtuvo en el test:

| PR-AUC | ROC-AUC | Recall | Precisión | Clientes a llamar |
|---|---|---|---|---|
| 0,497 | 0,818 | 0,673 | 0,369 | 21 % |

**Lectura de negocio:** llamando al 21 % de la base se alcanza a dos de cada tres suscriptores, con una tasa de éxito tres veces mayor que al azar. Si la capacidad es aún menor, llamar al 10 % mejor ubicado alcanza al 48 % de los suscriptores con 54 % de éxito.

### 4.4 Análisis no supervisado: segmentos de clientes

Con k-means sobre siete variables escaladas (edad, llamadas, contactos previos, contacto previo, euribor, empleo y su variación) y k = 4 (silueta 0,525, casi igual a k = 3 pero más útil), encontramos **sin usar la respuesta**:

| Segmento | Clientes | Rasgos | % suscribe |
|---|---|---|---|
| Saturados | 2 084 | ~11 llamadas en esta campaña | 3,9 % |
| Fríos en tasas altas | 25 609 | Nunca contactados, euribor ~4,8 % | 4,9 % |
| Fríos en tasas bajas | 11 965 | Nunca contactados, euribor ~1,2 % | 19,5 % |
| **Recontactados** | **1 530** | Contactados en campañas anteriores | **63,4 %** |

Isolation Forest (3 % de contaminación) señaló 1 236 casos "raros" que suscriben en un **59 %**: casi todos son clientes recontactados en épocas de tasas bajas. Aquí lo raro no es un error de datos, sino una oportunidad comercial.

## 5. Interpretación

Según la importancia por permutación en el test (caída de la PR-AUC), las variables que más pesan son:

1. **Número de empleados** (0,093) y **euribor a 3 meses** (0,039): el contexto económico del mes.
2. **Días desde el último contacto** (0,033) y **resultado previo** (0,014): el historial con el cliente.
3. **Tipo de contacto** (0,022): el celular funciona mejor que el teléfono fijo.

El modelo aprende **cuándo** conviene llamar tanto como **a quién**, lo que coincide con el análisis exploratorio.

## 6. Ética y limitaciones

**Equidad y protección del consumidor.** En el test, el modelo prioriza al **100 %** de los mayores de 60 años (su tasa real de suscripción es 46 %) y detecta el 91 % de los interesados menores de 25, frente al 62 % del grupo de 26 a 60 años. Que el modelo sea "preciso" con los mayores no lo hace inocuo: insistir con productos financieros a personas mayores puede convertirse en venta presionada. Recomendamos un tope de llamadas, un guion específico y revisión humana para este grupo. Por estado civil, el recall va de 58 % (divorciados) a 73 % (solteros), una brecha a monitorear.

**Uso responsable.** El modelo sirve para **ordenar llamadas** de una campaña de ahorro; no debe usarse para decidir créditos, tasas ni condiciones de ningún cliente.

**Limitaciones.**
- **Dependencia del contexto económico:** con una división temporal (entrenar con el primer 80 % de las llamadas y probar con el último 20 %), la tasa de suscripción cambia de 6 % a 31 % y el modelo pasa de ser 4,4 a solo 1,6 veces mejor que el azar. Antes de usarlo habría que reentrenarlo con frecuencia y validarlo en el tiempo.
- Los datos son de un banco portugués durante la crisis de 2008–2010; habría que validarlo con datos locales antes de usarlo en Perú.
- No hay variables de ingresos, saldo ni canal digital, que probablemente explicarían mejor el interés del cliente.

## 7. Conclusiones

Un modelo LightGBM optimizado ordena a los clientes 4,4 veces mejor que el azar usando solo información disponible antes de llamar, y permite alcanzar a la mitad de los suscriptores llamando a uno de cada diez clientes. La optimización mejora de forma significativa pero modesta, y ni la red neuronal ni la reponderación de clases aportan más. El análisis no supervisado entrega reglas simples y accionables: priorizar a los recontactados y dejar de llamar a los saturados. Antes de usarlo en producción se debe controlar la presión comercial sobre los mayores de 60 años y validar el modelo en el tiempo.

**Trabajo futuro:** validación temporal con ventana deslizante, calibración de probabilidades, variables de comportamiento digital del cliente y prueba con datos de una entidad financiera peruana.

## Referencias

- Akiba, T., Sano, S., Yanase, T., Ohta, T. y Koyama, M. (2019). Optuna: A next-generation hyperparameter optimization framework. En *Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining* (pp. 2623–2631). https://doi.org/10.1145/3292500.3330701
- Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3.ª ed.). O'Reilly.
- James, G., Witten, D., Hastie, T., Tibshirani, R. y Taylor, J. (2023). *An introduction to statistical learning with applications in Python*. Springer.
- Moro, S., Cortez, P. y Rita, P. (2014). A data-driven approach to predict the success of bank telemarketing. *Decision Support Systems, 62*, 22–31. https://doi.org/10.1016/j.dss.2014.03.001
- Moro, S., Rita, P. y Cortez, P. (2014). *Bank Marketing* [Conjunto de datos]. UCI Machine Learning Repository. https://doi.org/10.24432/C5K306

---

**Uso de IA generativa:** [declarar aquí]
