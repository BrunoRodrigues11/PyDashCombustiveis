import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

st.set_page_config(layout='wide')

@st.cache_data
def gerar_df():
    df = pd.read_excel(
        io = "database_anp.xlsx",
        engine = "openpyxl",
        sheet_name = "Planilha1",
        usecols = "A:Q",
        nrows = 19964
    )
    return df

df = gerar_df()

colunasUteis = ['MÊS', 'PRODUTO', 'REGIÃO', 'ESTADO', 'PREÇO MÉDIO REVENDA']
df = df[colunasUteis]

with st.sidebar:
    # Titulo e logo
    st.subheader('PETROL VALUES')
    logo_teste = Image.open('oil-price.png')
    st.image(logo_teste, use_column_width=True)

    # Filtros    
    st.subheader('FILTROS')
    fProduto = st.selectbox(
        "Produto:",
        options=df['PRODUTO'].unique()
    )
    fEstado = st.selectbox(
        "Estado:",
        options=df['ESTADO'].unique()
    )

    dadosUsuario = df.loc[
        (df['PRODUTO'] == fProduto) & (df['ESTADO'] == fEstado)
    ]

updateDatas = dadosUsuario['MÊS'].dt.strftime('%Y/%b')
dadosUsuario['MÊS'] = updateDatas[0: ]

st.header("PREÇO DOS COMBUSTÍVEIS NO BRASIL: 2013 À 2023")  
st.markdown("**Combustível:** " + fProduto)
st.markdown("**Estado:** " + fEstado)

grafCombEstado = alt.Chart(dadosUsuario).mark_line(
    point=alt.OverlayMarkDef(color='red', size=20)
).encode(
    x ='MÊS:T',
    y ='PREÇO MÉDIO REVENDA',
    strokeWidth = alt.value(3)
).properties(
    height = 550,
    width= 1500
)

st.altair_chart(grafCombEstado)

