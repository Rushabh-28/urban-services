"""
Builds a static HTML demo of the Urban Services pages into docs/,
so GitHub Pages can show them without installing Django.

Run from the project root:   python tools/build_demo.py
"""
import re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates" / "user"
STATIC = ROOT / "static"
OUT = ROOT / "docs"

# template file -> output file
PAGES = {
    "home.html": "index.html",
    "aboutus.html": "aboutus.html",
    "contact.html": "contact.html",
    "terms.html": "terms.html",
    "submit.html": "submit.html",
    "payment.html": "payment.html",
}
# {% url 'name' %} -> demo page
URLS = {
    "home": "index.html", "aboutus": "aboutus.html", "contact": "contact.html",
    "terms": "terms.html", "submit": "submit.html", "payment": "payment.html",
    "login": "#", "customer-register": "#",
}
SAMPLES = [
    ("AC Repair & Service", "1500.00", "Split and window AC servicing by verified technicians.", "AC-Repair.jpg"),
    ("Haircut & Styling", "499.00", "Salon-quality haircut and styling at your doorstep.", "haircut.jpg"),
    ("Spa at Home", "1999.00", "Relaxing full-body spa session by trained therapists.", "spa.jpg"),
]
CARD = """      <div class="col-md-4 mb-4">
        <div class="card" style="width: 18rem;border-radius: 20px;box-shadow: 5px 5px 16px 4px rgba(0,0,0,0.2);margin: 1em;min-width: 280px;max-width: 300px;border-style: none;">
          <div style="width:100%;height:200px;background:url('assets/images/{img}') center / cover;border-top-left-radius:20px;border-top-right-radius:20px;"></div>
          <div class="card-body d-flex flex-column" style="height: 262px;">
            <div>
              <h4 style="font-family:'Source Sans Pro',sans-serif;font-weight:700;color:rgb(255,160,0);">{title}</h4>
              <h6 class="text-muted mb-2" style="font-family:'Source Sans Pro',sans-serif;font-weight:600;">&#8377;{price} &middot; Available: True</h6>
              <p style="font-family:'Source Sans Pro',sans-serif;margin-top:16px;">{desc}</p>
            </div>
            <a href="payment.html" class="align-self-end mt-auto" style="padding:4px 14px 6px;background:#b86868;color:#fff;border-radius:17px;box-shadow:2px 2px 16px 1px rgba(117,117,117,.8);">Book Now</a>
          </div>
        </div>
      </div>
"""
BANNER = ('<div style="background:#fff3cd;color:#664d03;text-align:center;padding:8px;'
          'font:14px sans-serif;border-bottom:1px solid #ffecb5;">'
          'Static demo of the Urban Services Django project &ndash; forms and login '
          'need the full app (see README).</div>')

used_assets = set()

def convert(html: str, name: str) -> str:
    html = re.sub(r"\{%\s*comment\s*%\}.*?\{%\s*endcomment\s*%\}", "", html, flags=re.S)
    if name == "home.html":
        cards = "".join(CARD.format(img=i, title=t, price=p, desc=d) for t, p, d, i in SAMPLES)
        html = re.sub(r"\{%\s*for item in items\s*%\}.*?\{%\s*endfor\s*%\}", cards, html, flags=re.S)
    html = re.sub(r"\{%\s*load [^%]*%\}", "", html)
    html = re.sub(r"\{%\s*csrf_token\s*%\}", "", html)

    def static_sub(m):
        path = m.group(1).lstrip("./")
        used_assets.add(path)
        return path
    html = re.sub(r"\{%\s*static\s+['\"]([^'\"]+)['\"]\s*%\}", static_sub, html)

    def url_sub(m):
        return URLS.get(m.group(1), "#")
    html = re.sub(r"\{%\s*url\s+['\"]([^'\"]+)['\"][^%]*%\}", url_sub, html)

    html = html.replace('<script src="assets/js/bs-init.js"></script>', "")
    html = html.replace("http://localhost:8000/user/", "").replace("http://localhost:8000/", "")
    html = re.sub(r"\{\{[^}]*\}\}", "", html)          # leftover variables
    html = re.sub(r"\{%[^%]*%\}", "", html)             # any other leftover tags
    html = re.sub(r"(<body[^>]*>)", r"\1" + BANNER, html, count=1)
    return html

def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for src, dest in PAGES.items():
        html = convert((TEMPLATES / src).read_text(encoding="utf-8"), src)
        (OUT / dest).write_text(html, encoding="utf-8")
    for rel in sorted(used_assets | {f"assets/images/{s[3]}" for s in SAMPLES}):
        f = STATIC / rel
        if f.exists():
            (OUT / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(f, OUT / rel)
        else:
            print("missing asset:", rel)
    (OUT / ".nojekyll").write_text("")
    print("Built", len(PAGES), "pages into", OUT)

if __name__ == "__main__":
    main()
