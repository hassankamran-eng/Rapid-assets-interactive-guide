"""Give a hidden (headless) browser profile the owner's saved prod login, then screenshot Home to prove it.

The Firebase web SDK restores its session from IndexedDB firebaseLocalStorageDb/firebaseLocalStorage.
We write the saved refresh token there; the SDK refreshes the access token itself. Nothing is printed.
"""
import base64, importlib.util, json, os, sys, time
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
PROFILE = os.path.join(HERE, os.environ.get("RA_PROFILE", "profile"))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

os.environ["RAPIDASSETS_ENV"] = os.environ.get("RA_FB_ENV", "prod")
SITE = os.environ.get("RA_SITE", "https://rapidassets.ai")
spec = importlib.util.spec_from_file_location("rmcp", r"C:\Users\Hassan\Desktop\ImaginationAI\rapidassets-mcp\rapidassets_mcp.py")
mod = importlib.util.module_from_spec(spec)
argv, sys.argv = sys.argv, ["x"]
spec.loader.exec_module(mod)
sys.argv = argv
id_token = mod._ensure_token()[0]
tok = mod._load_token()
claims = json.loads(base64.urlsafe_b64decode(id_token.split(".")[1] + "=="))
api_key = mod.FIREBASE_API_KEY
now_ms = int(time.time() * 1000)
user = {
    "uid": claims["user_id"], "email": claims.get("email"), "emailVerified": bool(claims.get("email_verified")),
    "displayName": claims.get("name"), "photoURL": claims.get("picture"), "isAnonymous": False,
    "providerData": [{"providerId": "google.com", "uid": claims.get("firebase", {}).get("identities", {}).get("google.com", [claims["user_id"]])[0],
                      "displayName": claims.get("name"), "email": claims.get("email"), "phoneNumber": None, "photoURL": claims.get("picture")}],
    "stsTokenManager": {"refreshToken": tok["refresh_token"], "accessToken": id_token, "expirationTime": int(float(tok["expires_at"]) * 1000)},
    "createdAt": str(now_ms), "lastLoginAt": str(now_ms), "apiKey": api_key, "appName": "[DEFAULT]",
}
key = f"firebase:authUser:{api_key}:[DEFAULT]"

INJECT = """([key, value]) => new Promise((ok, bad) => {
  const r = indexedDB.open('firebaseLocalStorageDb', 1);
  r.onupgradeneeded = () => r.result.createObjectStore('firebaseLocalStorage', { keyPath: 'fbase_key' });
  r.onerror = () => bad(r.error);
  r.onsuccess = () => { const tx = r.result.transaction('firebaseLocalStorage', 'readwrite');
    tx.objectStore('firebaseLocalStorage').put({ fbase_key: key, value }); tx.oncomplete = () => ok(true); tx.onerror = () => bad(tx.error); };
})"""

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(PROFILE, headless=True, viewport={"width": 1440, "height": 900}, device_scale_factor=1.5)
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto(SITE + "/login", wait_until="domcontentloaded", timeout=60000)
    page.evaluate(INJECT, [key, user])
    page.goto(SITE + "/home", wait_until="networkidle", timeout=90000)
    page.wait_for_timeout(4000)
    print("url:", page.url)
    page.screenshot(path=os.path.join(OUT, "_login_check.png"))
    ctx.close()
