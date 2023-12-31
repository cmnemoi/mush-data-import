from streamlit import secrets

connect_to_twinoid = f"https://twinoid.com/oauth/auth?response_type=code&client_id={secrets.TWINOID_CLIENT_ID}&redirect_uri={secrets.TWINOID_REDIRECT_URI}&scope=mush.twinoid.com+mush.twinoid.es+mush_ship_data+mush.vg+groups&state=auth&access_type=offline"
cookies = """
<a href="javascript:(function(){let e=function e(i){let t=`; ${document.cookie}`,o=t.split('; sid=');if(2===o.length)return o.pop().split(';').shift()}('sid');if(e){let i=document.createElement('input');document.body.appendChild(i),i.value=e,i.focus(),i.select(),document.execCommand('copy'),i.remove(),alert('SID copied to clipboard')}})()">French Mush Cookie</a> 
<a href="javascript:(function(){let e=function e(i){let t=`; ${document.cookie}`,o=t.split('; mush_sid=');if(2===o.length)return o.pop().split(';').shift()}('mush_sid');if(e){let i=document.createElement('input');document.body.appendChild(i),i.value=e,i.focus(),i.select(),document.execCommand('copy'),i.remove(),alert('SID copied to clipboard')}})()">English Mush Cookie</a> 
<a href="javascript:(function(){let e=function e(i){let t=`; ${document.cookie}`,o=t.split('; sid=');if(2===o.length)return o.pop().split(';').shift()}('sid');if(e){let i=document.createElement('input');document.body.appendChild(i),i.value=e,i.focus(),i.select(),document.execCommand('copy'),i.remove(),alert('SID copied to clipboard')}})()">Spanish Mush Cookie</a>
"""
