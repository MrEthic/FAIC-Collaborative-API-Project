# Collaborative API

API definition:

# GET /{data}
## Parameters
| Parameter      | Description |
| ----------- | ----------- |
| from | Timestamp in the utc unix(s) format of the starting datetime of query |
| to | Timestamp in the utc unix(s) format of the ending datetime of query |
| (Optional) {dimension} | Dimension |

## Examples:

Query data from 1/1/2022 to 30/1/2022: `GET /data?from=1640995200&to=1643500800`

Query data from 1/1/2022 to 30/1/2022 with a dimension named `dim` equals to indoor: `GET /data?from=1640995200&to=1643500800&dim=indoor`

## Response format
JSON
```python
{
    'Records': [
        [Objects],
        ...
    ],
    'Metadata': {
        'SourceName': String,
        'SourceType': String,
        'SourceFormat': String('Timeserie'|'Tabular'|'Text'),
        'ColumnName': [
            Strings,
            ...
        ],
        'ColumnType': [
            Strings('timestamp'|'float'|'str')
        ]
    },
    'ExecutionInfo': {}
}
```

| Field      | Description |
| ----------- | ----------- |
| Records | List of records as list |
| Metadata | Metadata anout API |
| SourceName | Name of the source (ex: BrewAI) |
| SourceType | Type of the source (ex: SensorData) |
| SourceFormat | Format of the source, either Timeserie, Tabular or Text |
| ColumnName | List of column names (same size as records size) |
| ColumnType | List of column types (same size as records size) |
| ExecutionInfo | Information about execution (ex: Query ids, etc.) |

# GET /{data}/{dimension}
Return a list of the dimensions tuples.

## Response format
JSON
```python
{
    'Records': [
        [Objects],
        ...
    ],
    'Metadata': {
        'SourceName': String,
        'SourceType': String,
        'SourceFormat': String('Timeserie'|'Tabular'|'Text'),
        'ColumnName': [
            Strings,
            ...
        ],
        'ColumnType': [
            Strings('timestamp'|'float'|'str')
        ]
    },
    'ExecutionInfo': {}
}
```

| Field      | Description |
| ----------- | ----------- |
| Records | List of dimensions as list |
| Metadata | Metadata anout API |
| SourceName | Name of the source (ex: BrewAI) |
| SourceType | Type of the source (ex: SensorData) |
| SourceFormat | Format of the source, either Timeserie, Tabular or Text |
| ColumnName | List of column names (same size as records size) |
| ColumnType | List of column types (same size as records size) |
| ExecutionInfo | Information about execution (ex: Query ids, etc.) |