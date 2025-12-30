from flask import Flask, request, jsonify
import subprocess, json, tempfile, os

app = Flask(__name__)

CREDITS = "API by @Aotpy | https://aotpy.vercel.app"
ADMIN = "@Aotpy"
WEBSITE = "https://aotpy.vercel.app"


def fetch_instagram(url):
    try:
        with tempfile.TemporaryDirectory() as tmp:
            cmd = [
                "yt-dlp",
                "--dump-json",
                "--no-warnings",
                "--no-playlist",
                url
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                return None, "Failed to extract media"

            data = json.loads(result.stdout)

            media = []

            if "url" in data:
                media.append({
                    "type": "video",
                    "url": data["url"]
                })

            for f in data.get("formats", []):
                if f.get("url") and f.get("ext") in ["mp4", "jpg", "png"]:
                    media.append({
                        "type": "video" if f["ext"] == "mp4" else "image",
                        "url": f["url"]
                    })

            if not media:
                return None, "No media found"

            return media, None

    except Exception as e:
        return None, str(e)


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "endpoint": "/Tobi",
        "usage": "/Tobi?url=INSTAGRAM_URL",
        "admin_contact": ADMIN,
        "website": WEBSITE,
        "credits": CREDITS
    })


@app.route("/Tobi")
def tobi():
    url = request.args.get("url")

    if not url:
        return jsonify({
            "success": False,
            "error": "Missing url",
            "admin_contact": ADMIN,
            "website": WEBSITE
        }), 400

    media, error = fetch_instagram(url)

    if error:
        return jsonify({
            "success": False,
            "error": error,
            "admin_contact": ADMIN,
            "website": WEBSITE
        }), 500

    return jsonify({
        "success": True,
        "count": len(media),
        "media": media,
        "credits": CREDITS,
        "admin_contact": ADMIN,
        "website": WEBSITE
    })
