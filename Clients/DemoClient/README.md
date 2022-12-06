# Demo Client

Demo client for exploring collaboratives API.

# Deployement
## Local run:

**Requirements:**
- Python >= 3.9

```bash
git clone https://github.com/MrEthic/FAIC-Collaborative-API-Project.git
cd FAIC-Collaborative-API-Project/Clients/DemoClient/app
pip3 install -r requirements.txt
streamlit run main.py
```

## Docker run:

**Requirements:**
- Docker

```bash
git clone https://github.com/MrEthic/FAIC-Collaborative-API-Project.git
cd FAIC-Collaborative-API-Project/Clients/DemoClient/app
docker build -t demo-client .
docker run -d -p 80:80 demo-client
```

You can also run the remote hosted docker images:
```bash
docker pull push methicc/st-api-demo-client:latest
docker run -d -p 80:80 methicc/st-api-demo-client:latest
```

# Usage

1. Input a compatible API endpoint in en the `API Endpoint` field.
2. (Optional) Add an API Key in `API Key` field.
3. (Optional) Add a dimension endpoint.
4. (Optional) Add a dimension name.
5. Click on `Load`.
6. You can unselect columns in the `Columns` selection box.
7. If you added a dimension, you can select it's value.

Every column has a tab.