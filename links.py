from streamlit import secrets

connect_to_twinoid = "[Connect to Twinoid](" + f"https://twinoid.com/oauth/auth?response_type=code&client_id={secrets.TWINOID_CLIENT_ID}&redirect_uri={secrets.TWINOID_REDIRECT_URI}&scope=mush.twinoid.com+mush.twinoid.es+mush_ship_data+mush.vg+groups&state=auth&access_type=offline" + ")"