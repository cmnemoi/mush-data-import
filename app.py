import requests
import streamlit as st

from bs4 import BeautifulSoup
from google.cloud import bigquery, storage
from google.oauth2.service_account import Credentials

from links import *
from models import *
from texts import *

GCP_SERVICE_ACCOUNT = st.secrets["gcp_service_account"]

LANGUAGE_SITE_MAP = {
    "Français": 41,
    "English": 77,
    "Spanish": 76,
}

LANGUAGE_MUSH_SERVER_MAP = {
    "Français": "http://mush.vg",
    "English": "http://mush.twinoid.com",
    "Spanish": "http://mush.twinoid.es",
}

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

def get_mush_data(access_token: str, language: str, fields: str) -> Optional[dict]:
    if language == "Spanish": # todo add env var to allow if the app runs on Cloud run
        st.warning("Spanish profiles are not supported. Skipping fetching Mush API data.")
        return None
    
    url = build_mush_api_me_uri(access_token, LANGUAGE_MUSH_SERVER_MAP[language], fields)
    response = requests.get(url)
    json_response = response.json()
    if "error" in json_response:
        error = json_response["error"]
        st.error(f"Error getting Mush data: {error}")
        st.stop()
    
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
        error = json_response["error"]
        st.error(f"Error getting Twinoid API token: {error}")
        if error == "invalid_grant":
            st.error(translate("tokenExpired", language))
        st.stop() 

    return response.json()["access_token"]

def get_twinoid_data(access_token: str) -> dict:
    fields = twinoid_api_me_fields()
    url = build_twinoid_api_me_uri(access_token, fields)
    
    response = requests.get(url)
        
    return response.json()

def create_cookie_from_server_and_sid(server_url: str, sid: str) -> dict:
    if server_url == "http://mush.twionid.com":
        return {"mush_sid": sid}
    
    return {"sid": sid}

def scrap_mush_profile(server_url: str, sid: Optional[str]) -> Optional[dict]:
    if sid is None:
        st.info("No cookie given. Skipping Mush profile scraping.")
        return None
    if server_url == "http://mush.twinoid.es": # todo add env var to allow if the app runs on Cloud run
        st.warning("Spanish profiles are not supported. Skipping Mush profile scraping.")
        return None
    
    cookie = create_cookie_from_server_and_sid(server_url, sid)
    htmlContent = requests.get(f"{server_url}/me", cookies=cookie).content
    soup = BeautifulSoup(htmlContent, "html.parser")

    return {
        "character_levels": scrap_character_levels(soup),
        "klix": scrap_klix(soup),
        "skins": scrap_skins(soup),
        "flairs": scrap_flairs(soup),
    }

def scrap_character_levels(soup: BeautifulSoup) -> Optional[Dict]:
    character_level_divs = soup.find_all("div", {"class": "level"})
    if len(character_level_divs) == 0:
        st.error("Could not find your character levels")
        return None

    character_names = [div.next_sibling.text.strip() for div in character_level_divs]
    character_levels = [int(div.text.strip()) for div in character_level_divs]
    character_levels = dict(zip(character_names, character_levels))

    return character_levels

def scrap_klix(soup: BeautifulSoup) -> Optional[int]:
    klix_img = soup.find("img", {"class": "klix"})
    if klix_img is None:
        st.error("Could not find your klix")
        return None

    klix_str = klix_img.parent.text
    klix = int("".join(filter(str.isdigit, klix_str)))

    return klix

def scrap_skins(soup: BeautifulSoup) -> Optional[List[str]]:
    style_to_skin_map = {
        'background-position : 0px 	-1512px !important;': 'jin_su_gangnam_style',
        'background-position : 0px 	-1604px !important;': 'jin_su_vampire',
        'background-position : 0px 	-2063px !important;': 'frieda',
        'background-position : 0px 	-1875px !important;': 'kuan_ti',
        'background-position : 0px 	-1185px !important;': 'janice',
        'background-position : 0px 	-1056px !important;': 'roland',
        'background-position : 0px 	-1554px !important;': 'hua',
        'background-position : 0px 	-1728px !important;': 'paola',
        'background-position : 0px 	-1282px !important;': 'chao',
        'background-position : 0px 	-1921px !important;': 'finola',
        'background-position : 0px 	-1681px !important;': 'stephen',
        'background-position : 0px 	-1233px !important;': 'ian',
        'background-position : 0px 	-2017px !important;': 'chun',
        'background-position : 0px 	-1391px !important;': 'raluca',
        'background-position : 0px 	-1970px !important;': 'gioele',
        'background-position : 0px 	-1335px !important;': 'eleesha',
        'background-position : 0px 	-1444px !important;': 'terrence',
    }

    skin_divs = soup.find_all("div", {"class": "inl-blck"})
    if len(skin_divs) == 0:
        st.info('No skins found')
        return None
    
    skins = []
    for skin_div in skin_divs:
        skin_style = skin_div.attrs.get("style")
        if not skin_style is None:
            skin = style_to_skin_map.get(skin_style)
            if not skin is None:
                skins.append(skin)

    return skins

def scrap_flairs(soup: BeautifulSoup) -> Optional[List[str]]:
    flair_inputs = soup.find_all("input", {"onclick": " return Main.onClickVanity( $(this) ); "})
    if len(flair_inputs) == 0:
        st.info('No flairs found')
        return None
    
    flairs = [flair_input.parent.text.split("Activer :")[-1].strip() for flair_input in flair_inputs]

    return flairs

def mush_api_me_fields() -> str:
    return "creationDate,id,xp,historyHeroes.fields(id,charId,date,deathCycle,deathId,deathLocation,epitaph,group,heroId,log,rank,season,shipId,skillList,triumph,user,wasMush),historyShips.fields(conf,counter_all_spore,counter_explo,counter_hunter_dead,counter_mushes,counter_planet_scanned,counter_projects,counter_rebel_bases,counter_research,creationDate,deathCycle,destructionDate,group.fields(avatar,banner,creation,desc,domain,id,invests,name,resultDesc,triumphRemap,xp),id,pilgredDone,projects,researches,season.fields(desc,id,options,picto,publicName,start),shipId,triumphRemap)"

def twinoid_api_me_fields() -> str:
    return "id, name, sites.fields(site.fields(name), stats.fields(id, score, name, description, rare), achievements.fields(id, name, stat, score, points, npoints, description, date))"

if __name__ == "__main__":
    language = st.selectbox("Langue / Language", ["Français", "English"])

    st.title(translate("title", language))

    if "code" not in st.experimental_get_query_params():
        st.info(translate("intro", language))
        st.markdown(f"[{translate('connectToTwinoid', language)}]({connect_to_twinoid})", unsafe_allow_html=True)
    
    if "code" in st.experimental_get_query_params():
        # Declaring some interface elements
        st.info(translate("tutorial", language))
        st.video(open("tutorial.mp4", "rb").read())
        st.components.v1.html(cookies, height=40)
        profile_language_to_save = st.selectbox(translate("profileToSave", language), LANGUAGE_SITE_MAP.keys())
        sid = st.text_input("Cookie", "", type="password")
        st.markdown(f"[{translate('connectToTwinoid', language)}]({connect_to_twinoid})", unsafe_allow_html=True)
        
        code = st.experimental_get_query_params()["code"][0]
       
        if st.button(translate("getMyMushData", language)):
            access_token = get_twinoid_api_token(code)
            
            with st.spinner(translate("gettingData", language)):
                # Fetch data
                twinoid_data = get_twinoid_data(access_token)
                mush_data = get_mush_data(access_token, profile_language_to_save, mush_api_me_fields())
                scrapped_data = scrap_mush_profile(LANGUAGE_MUSH_SERVER_MAP[profile_language_to_save], sid)

                # Build user
                site = list(filter(lambda site: site["site"]["id"] == LANGUAGE_SITE_MAP[profile_language_to_save], twinoid_data["sites"]))[0]
                user = LegacyUser(
                    twinoid_id=twinoid_data["id"],
                    twinoid_username=twinoid_data["name"],
                    stats=[TwinoidUserStat(**stat) for stat in site["stats"]],
                    achievements=[TwinoidUserAchievement(**achievement) for achievement in site["achievements"]],
                    available_experience=mush_data["xp"] if not mush_data is None else None,
                    history_ships=[MushUserHistoryShip(**history_ship) for history_ship in mush_data["historyShips"]] if not mush_data is None else None,
                    history_heroes=[MushUserHistoryHero.from_history_hero_data(history_hero) for history_hero in mush_data["historyHeroes"]] if not mush_data is None else None,
                    character_levels=None if scrapped_data is None else [MushUserCharacterLevel(name=name, level=level) for name, level in scrapped_data["character_levels"].items()],
                    klix=None if scrapped_data is None else scrapped_data["klix"],
                    skins=None if scrapped_data is None else scrapped_data["skins"],
                    flairs=None if scrapped_data is None else scrapped_data["flairs"],
                )
                st.success(translate("dataRetrieved", language))

            # Save data
            with st.spinner(translate("savingData", language)):
                bq_client = bigquery.Client(project=GCP_SERVICE_ACCOUNT.project_id, credentials=Credentials.from_service_account_info(GCP_SERVICE_ACCOUNT))
                table_id = GCP_SERVICE_ACCOUNT.table_id
                job_config = bigquery.LoadJobConfig(
                    write_disposition="WRITE_APPEND",
                    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
                )
                try:
                    job = bq_client.load_table_from_json([user.model_dump()], table_id, job_config=job_config)
                    job.result() 
                except Exception as e:         
                    st.warning(f"Could not save user in database: {e}. Will save it in a bucket still.")

                # Always save in bucket 
                cs_client = storage.Client(project=GCP_SERVICE_ACCOUNT.project_id, credentials=Credentials.from_service_account_info(GCP_SERVICE_ACCOUNT))
                bucket = cs_client.bucket(GCP_SERVICE_ACCOUNT.bucket_name)
                blob = bucket.blob(f"{user.twinoid_username}_{user.twinoid_id}.json")
                blob.upload_from_string(user.model_dump_json(indent=4))

            # Success : display data          
            st.balloons()
            st.success(translate("congratulations", language))
            st.write(user.model_dump())

            