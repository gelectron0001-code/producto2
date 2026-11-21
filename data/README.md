# Datos

**Fuente:** [Bank Marketing](https://archive.ics.uci.edu/dataset/222/bank+marketing), UCI Machine Learning Repository (archivo `bank-additional-full.csv`, Moro et al., 2014)
**Licencia:** CC BY 4.0
**Cómo se obtienen:** los notebooks los descargan de una copia pública en GitHub. Si falla, descarguen el zip de UCI, extraigan `bank-additional-full.csv` y súbanlo al panel **Archivos** de Colab.

**Contexto:** campañas de telemarketing de un banco portugués (mayo 2008 – noviembre 2010). 41 188 llamadas.

## Variables usadas (19)

| Variable | Original | Tipo | Descripción |
|---|---|---|---|
| `edad` | age | numérica | Edad del cliente |
| `ocupacion` | job | categórica | Tipo de trabajo |
| `estado_civil` | marital | categórica | Casado, soltero, divorciado |
| `educacion` | education | categórica | Nivel educativo |
| `en_mora` | default | categórica | ¿Tiene crédito en mora? (`unknown` en 21 %) |
| `hipoteca` | housing | categórica | ¿Tiene crédito hipotecario? |
| `prestamo` | loan | categórica | ¿Tiene préstamo personal? |
| `tipo_contacto` | contact | categórica | Celular o teléfono fijo |
| `mes`, `dia_semana` | month, day_of_week | categórica | Momento de la llamada |
| `contactos_campana` | campaign | numérica | Llamadas en esta campaña (incluida la actual) |
| `dias_ultimo_contacto` | pdays | numérica | Días desde el contacto previo (999 → faltante = nunca contactado) |
| `contactos_previos` | previous | numérica | Contactos en campañas anteriores |
| `resultado_previo` | poutcome | categórica | Resultado de la campaña anterior |
| `tasa_var_empleo`, `ipc`, `confianza_consumidor`, `euribor3m`, `num_empleados` | emp.var.rate, cons.price.idx, cons.conf.idx, euribor3m, nr.employed | numéricas | Indicadores macroeconómicos del mes |
| **`suscribe`** | **y** | **objetivo** | **1 = abrió el depósito a plazo (11,3 %)** |

**Excluida a propósito:** `duracion_llamada` (duration). Solo se conoce cuando la llamada ya terminó; UCI advierte que debe descartarse para un modelo predictivo realista (fuga de datos).
