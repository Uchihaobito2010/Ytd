from flask import Flask, request, jsonify as Aotpyijson
import requests as Aotpyr
import re as Aotpyre

app = Flask(__name__)

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


@app.route("/api/yt", methods=["GET"])
def Aotpy_api():
    Aotpylink = request.args.get("link")

    if not Aotpylink:
        return Aotpyijson({
            "status": 0,
            "error": "Missing link parameter"
        }), 400

    Aotpypayload = {
        "url": "/media/parse",
        "data": {
            "origin": "source",
            "link": Aotpylink
        },
        "token": ""
    }

    Aotpyheaders = {
        "User-Agent": "Mozilla/5.0 (Linux; Android)",
        "Accept": "*/*",
        "Content-Type": "application/json",
        "Origin": "https://vidssave.com",
        "Referer": "https://vidssave.com/yt"
    }

    try:
        Aotpysession = Aotpyr.Session()
        Aotpysession.get("https://vidssave.com/yt", headers=Aotpyheaders)
        Aotpyres = Aotpysession.post(
            "https://vidssave.com/api/proxy",
            headers=Aotpyheaders,
            json=Aotpypayload,
            timeout=20
        )

        Aotpydata = Aotpyres.json()

        if Aotpydata.get("status") != 1:
            return Aotpyijson({
                "status": 0,
                "error": "Invalid response from source"
            }), 500

        Aotpyinfo = Aotpydata["data"]
        Aotpyout = []

        Aotpythumb = Aotpyinfo.get("thumbnail")
        Aotpythumb = Aotpy_shorten_url(Aotpythumb)

        for Aotpyrsc in Aotpyinfo.get("resources", []):
            if Aotpyrsc.get("download_mode") == "check_download":
                Aotpyout.append({
                    "quality": Aotpyrsc.get("quality"),
                    "format": Aotpyrsc.get("format"),
                    "size": Aotpyrsc.get("size"),
                    "download": Aotpy_shorten_url(Aotpyrsc.get("download_url"))
                })

        return Aotpyijson({
            "status": 1,
            "response": {
                "title": Aotpyinfo.get("title"),
                "duration": Aotpyinfo.get("duration"),
                "thumbnail": Aotpythumb,
                "data": Aotpyout
            }
        })

    except Exception as Aotpye:
        return Aotpyijson({
            "status": 0,
            "error": str(Aotpye)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
