import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta


@st.experimental_memo
def read_api(
    endpoint: str, key: str, dimension_endpoint: str = "", dimension_name: str = ""
):

    ts = Data(
        endpoint=endpoint,
        key=key,
        dimension_endpoint=dimension_endpoint,
        dimension_name=dimension_name,
    )

    return ts


class Data:
    def __init__(
        self,
        endpoint: str,
        key: str,
        dimension_endpoint: str = "",
        dimension_name: str = "",
    ) -> None:
        self._endpoint = endpoint
        self._key = key
        self.dimension_name = dimension_name
        self.dimensions_data = {}
        self.dim = False

        if dimension_name != "" and dimension_endpoint != "":
            self._init_dimension(dimension_endpoint)
            self.get_dim(dim=self.dimensions[0])
            self.dim = True
        else:
            self.get_dim()

    def get_dim(self, dim=""):

        if self.dim and dim in self.dimensions_data:
            return self.dimensions_data.get(dim)

        to = datetime.now()
        fromm = to - timedelta(days=1)
        to_ts = int(to.timestamp())
        from_ts = int(fromm.timestamp())

        url = (
            f"{self._endpoint}?from={from_ts}&to={to_ts}&{self.dimension_name}={dim}"
            if dim != ""
            else f"{self._endpoint}?from={from_ts}&to={to_ts}"
        )

        data = requests.get(
            url=url,
            headers={"x-api-key": self._key},
        )
        data = data.json()

        self._metadata = data["Metadata"]
        self._records = data["Records"]
        self.string_columns = []
        self.number_columns = []

        if self.source_format == "Timeserie":
            df = self._init_timeseries()
            if self.dim:
                self.dimensions_data[dim] = df
            return df

    @property
    def column_names(self) -> list:
        """Columns names

        Returns:
            list: Columns names
        """
        return self._metadata["ColumnName"]

    @property
    def column_types(self) -> list:
        """Columns python type

        Returns:
            list: Columns python type
        """
        return self._metadata["ColumnType"]

    @property
    def source_type(self) -> str:
        """Source type

        Returns:
            str: Source Type
        """
        return self._metadata["SourceType"]

    @property
    def source_name(self) -> str:
        """Source name

        Returns:
            str: Source Name
        """
        return self._metadata["SourceName"]

    @property
    def source_format(self) -> str:
        """Source formnat (Text, Timeserie or Tabular)

        Returns:
            str: Source Format
        """
        return self._metadata["SourceFormat"]

    def _init_dimension(self, dimension_endpoint):
        data = requests.get(
            url=f"{dimension_endpoint}",
            headers={"x-api-key": self._key},
        )
        self.dimensions = [dim[0] for dim in data.json()["Records"]]

    def _init_timeseries(self):
        df = pd.DataFrame(self._records, columns=self.column_names)
        for col_name, col_type in zip(self.column_names, self.column_types):
            if col_type == "timestamp":
                df[col_name] = pd.to_datetime(df[col_name])
                df[col_name] = (
                    df[col_name].dt.tz_localize("UTC").dt.tz_convert("Australia/ACT")
                )
                if col_name != "time":
                    df["time"] = df[col_name]
                    df = df.drop(col_name, axis=1)
            elif col_type == "float":
                df = df.astype({col_name: "float64"})
                self.number_columns.append(col_name)
            elif col_type == "string":
                df = df.astype({col_name: "str"})
                self.string_columns.append(col_name)

        return df
