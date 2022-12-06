import json
import streamlit as st
from dataloader import read_api
from plots import timeplot, distplot, pautocor

st.set_page_config(layout="wide", page_title="Demo Client")


def sidebar():
    st.sidebar.title("Configuration")
    api_endpoint = st.sidebar.text_input(label="API Endpoint", value="https://...")
    api_key = st.sidebar.text_input(label="API Key", value="")
    dimension_endpoint = st.sidebar.text_input(
        label="Dimension Endpoint",
        value="https://jov3dcr05d.execute-api.ap-southeast-2.amazonaws.com/v1/sensordata/sensors",
    )
    dimension_name = st.sidebar.text_input(label="Dimension Name", value="device")

    if st.sidebar.button("Load") and api_endpoint != "https://...":
        st.session_state["data"] = read_api(
            api_endpoint,
            key=api_key,
            dimension_endpoint=dimension_endpoint,
            dimension_name=dimension_name,
        )


def main():

    st.title("Standard Client for API lookhup")
    sidebar()

    if "data" not in st.session_state:
        st.session_state["data"] = None
        return

    if st.session_state["data"].dim:
        selected_dimension = st.sidebar.selectbox(
            label=st.session_state["data"].dimension_name.capitalize(),
            options=st.session_state["data"].dimensions,
            index=0,
        )
        df = st.session_state["data"].get_dim(dim=str(selected_dimension))
    else:
        df = st.session_state["data"].get_dim()

    selected_column = st.sidebar.multiselect(
        label="Columns",
        options=[col for col in df.columns if col != "time"],
        default=[col for col in df.columns if col != "time"],
    )

    tabs = st.tabs(["INFO"] + [col.upper() for col in selected_column])

    info = tabs[0]
    info.table(df.describe())
    info.code(json.dumps(st.session_state["data"]._metadata, indent=4), language="json")

    for tab, col in zip(tabs[1:], selected_column):
        with tab:
            if df[col].dtype in ("float64", "int64"):
                st.plotly_chart(timeplot(df, col), use_container_width=True)
                st.plotly_chart(distplot(df, col), use_container_width=True)
                st.plotly_chart(pautocor(df, col), use_container_width=True)
            else:
                for i in range(min((10, df.shape[0]))):
                    st.code(df.iloc[i][col])


if __name__ == "__main__":
    main()
