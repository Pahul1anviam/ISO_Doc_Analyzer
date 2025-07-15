import requests
from utils.config import SERPER_API_KEY

def search_iso_update(iso_code: str) -> str:
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY}
    query = f"{iso_code} amendment OR latest version OR update site:iso.org"
    
    res = requests.post(url, headers=headers, json={"q": query})
    data = res.json()
    results = data.get("organic", [])
    
    if not results:
        return "No update found."
    
    return "\n\n".join([r["snippet"] for r in results[:3]])

