import requests
import streamlit as st

def get_twinoid_oauth_link() -> str:
    responseType = "code"
    clientId = st.secrets["TWINOID_CLIENT_ID"]
    redirectUri = st.secrets["TWINOID_REDIRECT_URI"]
    scope = "mush.twinoid.com+mush.twinoid.es+mush_ship_data+mush.vg+groups"
    state = "auth"
    url = f"https://twinoid.com/oauth/auth?response_type={responseType}&client_id={clientId}&redirect_uri={redirectUri}&scope={scope}&state={state}"

    return "[Connect to Twinoid](" + url + ")"

def twinoid_api_me_fields() -> str:
    return "id, name, sites.fields(site.fields(name), stats.fields(id, score, name, description, rare), achievements.fields(id, name, stat, score, points, npoints, description, date))"

def build_twinoid_api_me_uri(access_token: str, fields: str) -> str:
    return f"https://twinoid.com/graph/me?access_token={access_token}&fields={fields}"

def build_twinoid_api_token_url(code: str) -> str:
    clientId = st.secrets["TWINOID_CLIENT_ID"]
    clientSecret = st.secrets["TWINOID_CLIENT_SECRET"]
    redirectUri = st.secrets["TWINOID_REDIRECT_URI"]
    grantType = "authorization_code"
    url = f"https://twinoid.com/oauth/token?client_id={clientId}&client_secret={clientSecret}&redirect_uri={redirectUri}&grant_type={grantType}&code={code}"

    return url

def get_twinoid_api_token(code: str) -> str:
    url = build_twinoid_api_token_url(code)
    response = requests.post(url)
    json_response = response.json()
    if "error" in json_response:
        raise Exception("Error getting Twinoid API token: " + json_response["error"])

    return response.json()["access_token"]

def get_twinoid_data(code: str) -> dict:
    access_token = get_twinoid_api_token(code)
    fields = twinoid_api_me_fields()
    url = build_twinoid_api_me_uri(access_token, fields)
    
    response = requests.get(url)
    
    st.write(response.json())
    
    return response.json()

if __name__ == "__main__":
    st.title("Import Twinoid")

    connect_to_twinoid_link = get_twinoid_oauth_link()
    st.markdown(connect_to_twinoid_link, unsafe_allow_html=True)
    
    if "code" in st.experimental_get_query_params():
        code = st.experimental_get_query_params()["code"][0]
        if st.button("Get my Twinoid data"):
            data = get_twinoid_data(code)
            st.write(data)