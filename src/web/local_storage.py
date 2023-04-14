import json
from streamlit_javascript import st_javascript

def get_from_local_storage(k):
    v = st_javascript(
        f"JSON.parse(localStorage.getItem('{k}'));"
    )
    return v or {}

def set_to_local_storage(k, v):
    jdata = json.dumps(v,separators=(',', ':'))
    st_javascript(
        f"localStorage.setItem('{k}', JSON.stringify({jdata}));"
    )
    