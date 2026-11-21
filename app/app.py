"""Demo: priorización de llamadas para una campaña de depósitos a plazo.

Se ejecuta con:  streamlit run app/app.py
modelo.joblib guarda {"modelo": pipeline completo, "umbral": umbral elegido} (notebooks/05_interpretacion.ipynb).
"""
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="¿A quién llamar?", page_icon="📞")
st.title("📞 ¿A quién llamar primero?")
st.write("Ingrese los datos de un cliente **antes de llamarlo**. El modelo estima la probabilidad "
         "de que acepte abrir un depósito a plazo.")

paquete = joblib.load(Path(__file__).parent / "modelo.joblib")
modelo, UMBRAL = paquete["modelo"], paquete["umbral"]
onehot = modelo.named_steps["prep"].named_transformers_["cat"].named_steps["onehot"]
opciones = dict(zip(onehot.feature_names_in_, [list(c) for c in onehot.categories_]))  # categorías vistas al entrenar

def elegir(etiqueta, col, defecto=None):
    ops = opciones[col]
    return st.selectbox(etiqueta, ops, index=ops.index(defecto) if defecto in ops else 0)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Cliente")
    edad = st.number_input("Edad", 17, 98, 40)
    ocupacion = elegir("Ocupación", "ocupacion", "admin.")
    estado_civil = elegir("Estado civil", "estado_civil", "married")
    educacion = elegir("Educación", "educacion", "university.degree")
    en_mora = elegir("¿Tiene crédito en mora?", "en_mora", "no")
    hipoteca = elegir("¿Tiene hipoteca?", "hipoteca", "no")
    prestamo = elegir("¿Tiene préstamo personal?", "prestamo", "no")
with col2:
    st.subheader("Historial de contacto")
    tipo_contacto = elegir("Tipo de contacto", "tipo_contacto", "cellular")
    mes = elegir("Mes de la llamada", "mes", "may")
    dia_semana = elegir("Día de la semana", "dia_semana", "mon")
    contactos_campana = st.number_input("Llamadas en esta campaña (incluida esta)", 1, 60, 1)
    contactos_previos = st.number_input("Contactos en campañas anteriores", 0, 10, 0)
    resultado_previo = elegir("Resultado de la campaña anterior", "resultado_previo", "nonexistent")
    contactado = st.checkbox("Fue contactado en una campaña anterior")
    dias = st.number_input("Días desde el último contacto", 0, 30, 6, disabled=not contactado)

with st.expander("Contexto económico (indicadores del mes)"):
    escenario = st.radio("Escenario", ["Tasas altas (como 2008)", "Tasas bajas (como 2010)"], horizontal=True)
    alto = escenario.startswith("Tasas altas")
    tasa_var_empleo = st.number_input("Variación del empleo", -4.0, 2.0, 1.1 if alto else -1.8)
    ipc = st.number_input("Índice de precios al consumidor", 92.0, 95.0, 93.99 if alto else 93.0)
    confianza = st.number_input("Confianza del consumidor", -51.0, -26.0, -36.4 if alto else -40.0)
    euribor = st.number_input("Euribor a 3 meses (%)", 0.5, 5.1, 4.86 if alto else 1.0)
    empleados = st.number_input("Número de empleados (miles)", 4900.0, 5250.0, 5191.0 if alto else 5017.5)

caso = pd.DataFrame([{
    "edad": edad, "contactos_campana": contactos_campana,
    "dias_ultimo_contacto": dias if contactado else float("nan"), "contactos_previos": contactos_previos,
    "tasa_var_empleo": tasa_var_empleo, "ipc": ipc, "confianza_consumidor": confianza,
    "euribor3m": euribor, "num_empleados": empleados,
    "ocupacion": ocupacion, "estado_civil": estado_civil, "educacion": educacion, "en_mora": en_mora,
    "hipoteca": hipoteca, "prestamo": prestamo, "tipo_contacto": tipo_contacto, "mes": mes,
    "dia_semana": dia_semana, "resultado_previo": resultado_previo,
}])

if st.button("Estimar probabilidad", type="primary"):
    prob = modelo.predict_proba(caso)[0, 1]
    st.metric("Probabilidad de que suscriba", f"{prob:.0%}", help="Tasa promedio en los datos: 11 %")
    if prob >= UMBRAL:
        st.success(f"📞 Prioridad de llamada (supera el umbral de {UMBRAL:.0%}).")
    else:
        st.info(f"Baja prioridad (no alcanza el umbral de {UMBRAL:.0%}).")
    if contactos_campana > 10:
        st.warning("Este cliente ya recibió muchas llamadas en esta campaña: insistir rara vez funciona.")

st.caption("Proyecto académico · Machine Learning · Maestría en Ciencia de Datos e IA · EPG UNAJ. "
           "Datos: Bank Marketing (UCI). El modelo sirve para ordenar llamadas, no para decidir sobre créditos.")
