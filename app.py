import requests
import streamlit as st

from bs4 import BeautifulSoup
from google.cloud import bigquery
from google.oauth2.service_account import Credentials

from links import *
from models import *

GCP_SERVICE_ACCOUNT = st.secrets["gcp_service_account"]

LANGUAGE_SITE_MAP = {
    "French": 41,
    "English": 77,
}

LANGUAGE_MUSH_SERVER_MAP = {
    "French": "http://mush.vg",
    "English": "http://mush.twinoid.com",
}

TUTO = f"""
You can backup your original Mush account with this app.

Here is the list of items saved :
- Your Twinoid username
- Your achievements and titles
- Your ships

You can additionally save :
- Your character levels
- Your klix

If you fill the "Cookie" field. For that you wll find below two links to copy your cookies : one for the French server and one for the English server.

Save the link that interests you as a new bookmark (right-click and save the bookmark). 

Next, go to the corresponding Mush site and log in to your account. Click on the bookmark saved previously while being logged into the Mush site.

This will automatically save the cookie in your clipboard. Return to the eMush import page, and paste the cookie into the 'cookie' field below.

You can only backup the profile from **one server**. Choose wisely! 

Do not leave the page during the profile import!

It's possible to make as many imports as you want. Please use "Connect to Twinoid" link each time you want to import a new profile.

If you have any questions or encounter issues, feel free to contact us on the [Eternaltwin Discord](https://discord.gg/Kd8DUkWy4N).
"""

def build_mush_api_me_uri(access_token: str, server: str, fields: str) -> str:
    return f"{server}/tid/graph/me?access_token={access_token}&fields={fields}"

def build_twinoid_api_me_uri(access_token: str, fields: str) -> str:
    return f"https://twinoid.com/graph/me?access_token={access_token}&fields={fields}"

def build_twinoid_api_token_url(code: str) -> str:
    clientId = st.secrets["TWINOID_CLIENT_ID"]
    clientSecret = st.secrets["TWINOID_CLIENT_SECRET"]
    redirectUri = st.secrets["TWINOID_REDIRECT_URI"]
    grantType = "authorization_code"
    url = f"https://twinoid.com/oauth/token?client_id={clientId}&client_secret={clientSecret}&redirect_uri={redirectUri}&grant_type={grantType}&code={code}"

    return url

def get_mush_data(access_token: str, language: str, fields: str) -> list:
    url = build_mush_api_me_uri(access_token, LANGUAGE_MUSH_SERVER_MAP[language], fields)
    response = requests.get(url)
    json_response = response.json()
    if "error" in json_response:
        raise Exception("Error getting Mush data: " + json_response["error"])

    return response.json()

def get_twinoid_oauth_link() -> str:
    responseType = "code"
    clientId = st.secrets["TWINOID_CLIENT_ID"]
    redirectUri = st.secrets["TWINOID_REDIRECT_URI"]
    scope = "mush.twinoid.com+mush.twinoid.es+mush_ship_data+mush.vg+groups"
    state = "auth"
    access_type = "offline"
    url = f"https://twinoid.com/oauth/auth?response_type={responseType}&client_id={clientId}&redirect_uri={redirectUri}&scope={scope}&state={state}&access_type={access_type}"

    return "[Connect to Twinoid](" + url + ")"


def get_twinoid_api_token(code: str) -> str:
    url = build_twinoid_api_token_url(code)
    response = requests.post(url)
    json_response = response.json()
    if "error" in json_response:
        raise Exception("Error getting Twinoid API token: " + json_response["error"])

    return response.json()["access_token"]

def get_twinoid_data(access_token: str) -> dict:
    fields = twinoid_api_me_fields()
    url = build_twinoid_api_me_uri(access_token, fields)
    
    response = requests.get(url)
        
    return response.json()

def create_cookie_from_server_and_sid(server_url: str, sid: str) -> dict:
    if server_url == "http://mush.vg":
        return {"sid": sid}
    
    return {"mush_sid": sid}

def scrap_mush_profile(server_url: str, sid: Optional[str]) -> dict:
    if sid is None:
        st.info("No cookie given. Skipping Mush profile scraping.")
        return {}
    
    cookie = create_cookie_from_server_and_sid(server_url, sid)
    htmlContent = requests.get(f"{server_url}/me", cookies=cookie).content
    soup = BeautifulSoup(htmlContent, "html.parser")

    return {
        "character_levels": scrap_character_levels(soup),
        "klix": scrap_klix(soup)
    }

def scrap_character_levels(soup) -> Optional[Dict]:
    character_level_divs = soup.find_all("div", {"class": "level"})
    if len(character_level_divs) == 0:
        st.error("Could not find your character levels")
        return None

    character_names = [div.next_sibling.text.strip() for div in character_level_divs]
    character_levels = [int(div.text.strip()) for div in character_level_divs]
    character_levels = dict(zip(character_names, character_levels))

    return character_levels

def scrap_klix(soup) -> Optional[int]:
    klix_img = soup.find("img", {"class": "klix"})
    if klix_img is None:
        st.error("Could not find your klix")
        return None

    klix_str = klix_img.parent.text
    klix = int("".join(filter(str.isdigit, klix_str)))

    return klix

def mush_api_me_fields() -> str:
    return "creationDate,id,xp,historyHeroes.fields(id,date,deathCycle,deathId,deathLocation,epitaph,group,heroId,log,rank,season,shipId,skillList,triumph,user,wasMush),historyShips.fields(conf,counter_all_spore,counter_explo,counter_hunter_dead,counter_mushes,counter_planet_scanned,counter_projects,counter_rebel_bases,counter_research,creationDate,deathCycle,destructionDate,group.fields(avatar,banner,creation,desc,domain,id,invests,name,resultDesc,triumphRemap,xp),id,pilgredDone,projects,researches,season.fields(desc,id,options,picto,publicName,start),shipId,triumphRemap)"

def twinoid_api_me_fields() -> str:
    return "id, name, sites.fields(site.fields(name), stats.fields(id, score, name, description, rare), achievements.fields(id, name, stat, score, points, npoints, description, date))"

if __name__ == "__main__":
    st.title("Save Mush data")

    if "code" not in st.experimental_get_query_params():
        st.info("You can backup your original Mush account with this app. Connect to Twinoid to proceed.")

    st.markdown(connect_to_twinoid, unsafe_allow_html=True)
    
    if "code" in st.experimental_get_query_params():
        st.info(TUTO)
        st.video(open("tutorial.mp4", "rb").read())
        st.components.v1.html(cookies, height=40)
        code = st.experimental_get_query_params()["code"][0]
        profile_language_to_save = st.selectbox("Profile to save", ["French", "English"])
        sid = st.text_input("Cookie", "")
        if st.button("Get my Twinoid data"):
            access_token = get_twinoid_api_token(code)
            
            with st.spinner("Getting your data..."):
                twinoid_data = get_twinoid_data(access_token)
                mush_data = get_mush_data(access_token, profile_language_to_save, mush_api_me_fields())
                scrapped_data = scrap_mush_profile(LANGUAGE_MUSH_SERVER_MAP[profile_language_to_save], sid)

                site = list(filter(lambda site: site["site"]["id"] == LANGUAGE_SITE_MAP[profile_language_to_save], twinoid_data["sites"]))[0]
                user = LegacyUser(
                    twinoid_id=twinoid_data["id"],
                    twinoid_username=twinoid_data["name"],
                    stats=[TwinoidUserStat(**stat) for stat in site["stats"]],
                    achievements=[TwinoidUserAchievement(**achievement) for achievement in site["achievements"]],
                    available_experience=mush_data["xp"],
                    history_heroes=[MushUserHistoryHero.from_history_hero_data(history_hero) for history_hero in mush_data["historyHeroes"]],
                    history_ships=[MushUserHistoryShip(**history_ship) for history_ship in mush_data["historyShips"]],
                    character_levels=None if scrapped_data["character_levels"] is None else [MushUserCharacterLevel(name=name, level=level) for name, level in scrapped_data["character_levels"].items()],
                    klix=scrapped_data["klix"]
                )
                st.success("Data successfully retrieved!")

            with st.spinner("Saving your data..."):
                bq_client = bigquery.Client(project=GCP_SERVICE_ACCOUNT.project_id, credentials=Credentials.from_service_account_info(GCP_SERVICE_ACCOUNT))
                table_id = GCP_SERVICE_ACCOUNT.table_id
                job_config = bigquery.LoadJobConfig(
                    write_disposition="WRITE_APPEND",
                    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
                )
                job = bq_client.load_table_from_json([user.model_dump()], table_id, job_config=job_config)
                job.result()
            
            st.balloons()
            st.success("Congratulations! Your profile has been successfully saved! Here is a preview of your data:")
            st.write(user.model_dump())

            