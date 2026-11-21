# Producto 1 · Informe técnico de modelado supervisado

**Peso:** 35 % de la nota final · **Modalidad:** grupal

## Qué demuestra

Que el equipo sabe **plantear un problema** de machine learning, **preparar los datos sin errores** y **comparar modelos de forma honesta**.

## Qué se entrega

- [ ] **Informe en PDF** de 5 a 8 páginas → guardarlo en `informe/Producto1.pdf`
- [ ] **Notebook o repositorio** que se ejecute de principio a fin sin errores

---

## Estructura del informe

Tomen como referencia el ejemplo [`informe/Producto1_ejemplo.md`](../informe/Producto1_ejemplo.md). Cada sección indica en qué sesión se vio el tema.

| Sección | Qué debe tener | Sesión |
|---|---|---|
| 1. Problema y contexto | La pregunta, por qué importa y si es regresión o clasificación | 1 |
| 2. Datos | Fuente, tamaño, variables y **3 a 5 hallazgos** del análisis exploratorio | 1 |
| 3. Métrica de éxito | Cuál se usa y **por qué** | 3 |
| 4. Preprocesamiento | El pipeline construido y **cómo se evitó la fuga de datos** | 4 |
| 5. Modelos comparados | Los 5 modelos obligatorios (ver abajo) | 2, 3 y 5 |
| 6. Resultados | Tabla con validación cruzada (**promedio ± desviación**) y el mejor modelo | 5 |
| 7. Conclusiones | Qué aprendieron y qué mejorarán en la Unidad II | — |

### Los 5 modelos obligatorios

1. Un **baseline** simple (`DummyClassifier` o `DummyRegressor`)
2. Al menos un **modelo lineal regularizado** (logística con L2, Ridge o Lasso)
3. Un modelo de **kernels o k-NN**
4. Un **Random Forest**
5. Un modelo de **boosting** (LightGBM, XGBoost o CatBoost)

---

## Rúbrica (20 puntos)

| Criterio | Puntos |
|---|---|
| Formulación del problema y justificación de la métrica | 4 |
| Datos y análisis exploratorio | 3 |
| Pipeline correcto, sin fuga de datos | 4 |
| Comparación de modelos con validación adecuada | 5 |
| Reproducibilidad del código | 2 |
| Redacción y conclusiones | 2 |
| **Total** | **20** |

---

## Lista de control antes de entregar

- [ ] El notebook corre completo con **Entorno de ejecución → Reiniciar y ejecutar todas**
- [ ] Todo el preprocesamiento está **dentro de un `Pipeline`**
- [ ] Ninguna variable usa información **del futuro** (que no existiría al momento de predecir)
- [ ] El test se usó **una sola vez**, al final
- [ ] La tabla de resultados tiene **promedio ± desviación** de la validación cruzada
- [ ] La métrica está justificada con el **costo del error** del problema
- [ ] Declararon el uso de IA generativa, si la usaron

## Errores frecuentes

- ❌ Reportar la **accuracy** con clases desbalanceadas → usen recall, precisión o PR-AUC.
- ❌ **Escalar o imputar antes de dividir** los datos → fuga de datos.
- ❌ Reportar **un solo número** sin validación cruzada.
- ❌ Elegir el modelo mirando el **test** varias veces.
