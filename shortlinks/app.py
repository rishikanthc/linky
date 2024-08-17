import os
import fire
import uvicorn
from jinja2 import Environment, FileSystemLoader
from loguru import logger
import sys
import string
import random
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from datetime import datetime, timedelta

logger.add(sys.stdout, format="{time} {level} {message}", level="DEBUG")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

package_dir = os.path.dirname(__file__)
static_dir = os.path.join(package_dir, "static")
fonts_dir = os.path.join(static_dir, "fonts/IBM_Plex")
app.mount("/static", StaticFiles(directory=static_dir), name="static")
app.mount("/fonts", StaticFiles(directory=fonts_dir), name="fonts")

templates_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = Environment(loader=FileSystemLoader(templates_dir))
templates = Jinja2Templates(directory="templates")
templates.env = jinja_env

# In-memory store for shortened URLs with expiry times
url_store = {}


def generate_short_url():
    """Generate a random 6-character string for the short URL."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=6))


@app.get("/")
async def render_page(request: Request):
    return templates.TemplateResponse("page.html", {"request": request})


@app.post("/shorten")
async def shorten_url(url: str = Form(...), expiry: str = Form(...)):
    short_url = generate_short_url()
    while short_url in url_store:
        short_url = generate_short_url()

    # Calculate expiry time
    if expiry == "never":
        expiry_time = None
    else:
        duration = int(expiry)  # Extract the number of seconds from the expiry string
        expiry_time = datetime.now() + timedelta(seconds=duration)

    url_store[short_url] = {"url": url, "expiry": expiry_time}
    short_url_full = f"http://localhost:8000/{short_url}"
    return JSONResponse(content={"short_url": short_url_full})


@app.get("/{short_url}")
async def redirect_to_original(request: Request, short_url: str):
    url_data = url_store.get(short_url)
    if url_data:
        if url_data["expiry"] is None or datetime.now() < url_data["expiry"]:
            return RedirectResponse(url_data["url"])
        else:
            # Remove expired URL
            del url_store[short_url]
            return templates.TemplateResponse("expired.html", {"request": request})
    else:
        raise HTTPException(status_code=404, detail="Short URL not found")


class LinkServer:
    @staticmethod
    def run(host: str = "0.0.0.0", port: int = 8000, reload: bool = True):
        """Run the FastAPI server using Uvicorn."""
        uvicorn.run("shortlinks.app:app", host=host, port=port, reload=reload)


def main():
    fire.Fire(LinkServer)


if __name__ == "__main__":
    main()
