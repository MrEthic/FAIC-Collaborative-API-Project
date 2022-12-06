import streamlit as st
from statsmodels.tsa.stattools import pacf
import plotly.express as px
import plotly.graph_objects as go


@st.experimental_memo
def timeplot(df, col):
    fig = px.line(df, x="time", y=col)
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    return fig


@st.experimental_memo
def distplot(df, col):
    fig = px.histogram(df, x=col)
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    return fig


@st.experimental_memo
def pautocor(df, col, lags: int = 28):
    df_pacf = pacf(df[col].values.squeeze(), nlags=lags)
    fig = go.Figure(
        data=go.Bar(y=df_pacf),
        layout_title_text=f"",
    )
    fig = px.bar(df_pacf, title=f"Partial autocorrelation (lag={lags})")
    fig.update_layout(showlegend=False)
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    return fig
