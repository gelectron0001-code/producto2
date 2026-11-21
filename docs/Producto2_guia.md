# Producto 2 · Proyecto integrador final

**Peso:** 35 % de la nota final · **Modalidad:** grupal, con preguntas individuales

## Qué demuestra

Que el equipo puede llevar su modelo **del prototipo a una solución optimizada, explicable y funcionando**, y defenderla con rigor.

## Qué se entrega

**Documentos en UPG Learning hasta las 08:00 del domingo 15 de noviembre.** La exposición es ese mismo día.

- [ ] **Informe tipo artículo** de 6 a 10 páginas → `informe/Producto2.pdf`
- [ ] **Repositorio en GitHub** con el README completo
- [ ] **Demo funcionando** en Streamlit o Gradio, con el enlace en el README
- [ ] **Exposición** de 15 minutos + 5 de preguntas

---

## Qué se agrega al Producto 1

El Producto 2 **no empieza de cero**: es el Producto 1 más estas cinco partes.

| Qué agregar | Cómo | Sesión |
|---|---|---|
| **1. Optimización** | Su mejor modelo optimizado con Optuna, y tratamiento del desbalance si lo hay | 6 |
| **2. Comparación honesta** | El modelo optimizado contra el del Producto 1, **fold a fold** (Wilcoxon) | 6 |
| **3. Análisis no supervisado** | Segmentación (k-means) o casos raros (Isolation Forest) que **aporte al problema** | 7 |
| **4. Red neuronal** | Un MLP comparado con su mejor modelo | 8 |
| **5. Interpretación y ética** | SHAP o importancia por permutación; revisión de sesgo si hay variables sensibles (sexo, edad, zona) | 9 |

Y la **demo funcionando** durante la exposición (sesión 9).

---

## Estructura del informe tipo artículo

Tomen como referencia el ejemplo [`informe/Producto2_ejemplo.md`](../informe/Producto2_ejemplo.md).

1. **Resumen** (150–200 palabras)
2. **Introducción:** el problema, por qué importa y trabajos relacionados
3. **Datos**
4. **Método:** pipeline, modelos, validación y optimización
5. **Experimentos y resultados:** tablas y gráficos
6. **Interpretación:** qué variables pesan y qué perfiles se encontraron
7. **Ética y limitaciones:** sesgos, riesgos de uso y qué no puede hacer el modelo
8. **Conclusiones**
9. **Referencias** en APA 7

---

## La exposición (15 + 5 minutos)

| Minutos | Contenido sugerido |
|---|---|
| 2 | El problema y por qué importa |
| 2 | Los datos y la métrica |
| 4 | Los modelos y la mejora frente al Producto 1 |
| 3 | Qué variables pesan y qué perfiles encontraron |
| 2 | **La demo en vivo** |
| 2 | Limitaciones y conclusiones |
| **+5** | Preguntas del docente a **cada integrante** |

**Defensa individual:** cada integrante responde al menos una pregunta sobre **cualquier parte** del trabajo. La nota puede ajustarse para quien no demuestre dominio de lo entregado.

---

## Rúbrica (20 puntos)

| Criterio | Puntos |
|---|---|
| Mejora y optimización del modelo respecto al Producto 1 | 4 |
| Comparación con red neuronal y análisis no supervisado | 3 |
| Interpretabilidad y análisis ético | 3 |
| Despliegue y reproducibilidad | 3 |
| Calidad del informe tipo artículo | 4 |
| Exposición y defensa individual | 3 |
| **Total** | **20** |

---

## Lista de control antes de entregar

- [ ] El README tiene el problema, los resultados y el **enlace a la demo**
- [ ] La demo **abre y predice** (pruébenla desde otra computadora)
- [ ] La comparación con el Producto 1 es **fold a fold**, no solo dos promedios
- [ ] El análisis no supervisado **dice algo útil** del problema, no solo un gráfico
- [ ] Explican **qué variables pesan** y si el modelo trata distinto a algún grupo
- [ ] Hay una sección de **limitaciones** honesta
- [ ] Todos los integrantes pueden explicar **cualquier parte** del código
- [ ] Declararon el uso de IA generativa, si la usaron

## Consejos

- 💡 **Si la optimización o la red no mejoran, díganlo.** Un empate bien demostrado vale más que una mejora inventada.
- 💡 **Ensayen la demo antes.** Tengan una captura de pantalla de respaldo por si falla el internet.
- 💡 **Cuenten una historia:** problema → datos → modelo → qué aprendimos → cómo se usaría.
