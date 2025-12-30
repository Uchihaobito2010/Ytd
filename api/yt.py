from flask import Flask, request, jsonify as Aotpyijson
import requests as Aotpyr
import re as Aotpyre

app = Flask(__name__)

# ================= CREDITS =================
API_OWNER = "Aotpy"
ADMIN_CONTACT = "https://t.me/Aotpy"
WEBSITE = "https://Aotpy.vercel.app"
POWERED_BY = "Tobi YT Downloader API"
# ===========================================


def Aotpy_shorten_url(Aotpyurl):
    if not Aotpyurl:
        return Aotpyurl
    try:
        Aotpyres = Aotpyr.post(
            "https://freelyshrink.com/shorten.php",
            headers={
                "User-Agent": "Mozilla/5.0",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            data={"long_url": Aotpyurl},
            timeout=15
        )

        if "code=" in Aotpyres.url:
            Aotpycode = Aotpyres.url.split("code=")[1].split("&")[0]
            return f"https://hosturl.link/{Aotpycode}"

        Aotpymatch = Aotpyre.search(r'code=([a-zA-Z0-9]+)', Aotpyres.text)
        if Aotpymatch:
            return f"https://hosturl.link/{Aotpymatch.group(1)}"
    except:
        pass

    return Aotpyurl


# ---------- ROOT ----------
@app.route("/", methods=["GET"])
def root():
    return Aotpyijson({
        "status": 1,
        "name": POWERED_BY,
        "endpoints": {
            "/api/yt?link=": "Download YouTube video"
        },
        "credits": {
            "owner": API_OWNER,
            "contact": ADMIN_CONTACT,
            "website": WEBSITE
        }
    })


# ---------- YT API ----------
@app.route("/yt", methods=["GET"])
def Aotpy_api():
    Aotpylink = request.args.get("link")

    if not Aotpylink:
        return Aotpyijson({
            "status": 0,
            "error": "Missing link parameter",
            "credits": {
                "owner": API_OWNER,
                "contact": ADMIN_CONTACT,
                "website": WEBSITE
            }
        }), 400

    Aotpypayload = {
        "url": "/media/parse",
        "data": {
            "origin": "source",
            "link": Aotpylink
        },
        "token": ""
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json",
        "Origin": "https://vidssave.com",
        "Referer": "https://vidssave.com/yt"
    }

    try:
        s = Aotpyr.Session()
        s.get("https://vidssave.com/yt", headers=headers)

        r = s.post(
            "https://vidssave.com/api/proxy",
            headers=headers,
            json=Aotpypayload,
            timeout=20
        )

        data = r.json()
        if data.get("status") != 1:
            return Aotpyijson({
                "status": 0,
                "error": "Provider blocked or invalid response",
                "credits": {
                    "owner": API_OWNER,
                    "contact": ADMIN_CONTACT,
                    "website": WEBSITE
                }
            }), 500

        info = data["data"]
        out = []

        for res in info.get("resources", []):
            if res.get("download_mode") == "check_download":
                out.append({
                    "quality": res.get("quality"),
                    "format": res.get("format"),
                    "size": res.get("size"),
                    "download": Aotpy_shorten_url(res.get("download_url"))
                })

        return Aotpyijson({
            "status": 1,
            "response": {
                "title": info.get("title"),
                "duration": info.get("duration"),
                "thumbnail": Aotpy_shorten_url(info.get("thumbnail")),
                "data": out
            },
            "credits": {
                "owner": API_OWNER,
                "contact": ADMIN_CONTACT,
                "website": WEBSITE
            }
        })

    except Exception as e:
        return Aotpyijson({
            "status": 0,
            "error": str(e),
            "credits": {
                "owner": API_OWNER,
                "contact": ADMIN_CONTACT,
                "website": WEBSITE
            }
        }), 500
