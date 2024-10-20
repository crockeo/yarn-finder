from base64 import b64encode
from pathlib import Path

import hsluv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import NoResultFound
from starlette.responses import HTMLResponse, Response

from yarn_finder import database, services

app = FastAPI()
env = Jinja2Templates(Path.cwd() / "templates")


@app.get("/")
async def index() -> HTMLResponse:
    return env.TemplateResponse("index.html", {"request": {}})


@app.get("/yarns/search/{rgb}")
async def search_yarns(rgb: str) -> HTMLResponse:
    if len(rgb) != 6:
        raise HTTPException(400, "Malformed RGB")
    async with database.create_session() as sess:
        yarns, pagination_token = await services.get_yarns_close_to(
            sess,
            f"#{rgb}",
            page_size=8,
        )
    return env.TemplateResponse(
        "yarns.html",
        {
            "request": {},
            "yarns": [yarn for yarn, _ in yarns],
            "yarn_data": {
                yarn.id: {
                    "match_pct": match_pct,
                    "image": b64encode(yarn.image).decode(),
                    "hex": hsluv.hsluv_to_hex(
                        (yarn.hue, yarn.saturation, yarn.lightness)
                    ),
                }
                for yarn, match_pct in yarns
            },
        },
    )


@app.get("/yarns/{id}/image")
async def get_yarn_image(id: int) -> Response:
    async with database.create_session() as sess:
        try:
            yarn = await services.get_yarn(sess, id)
        except NoResultFound:
            raise HTTPException(404, "Not found")
    return Response(
        content=yarn.image,
        media_type="image/jpeg",
    )


app.mount("/", StaticFiles(directory="static"), name="static")
