#!/usr/bin/env python3

import asyncio
import io
import json
import math
import subprocess
from pathlib import Path

import hsluv
from PIL import Image

from yarn_finder import database
from yarn_finder.models import Yarn


def _ensure_git_checkout(cwd: Path) -> None:
    if (cwd / "Temperature-Blanket-Web-App").is_dir():
        return
    subprocess.check_call(
        ("git", "clone", "https://github.com/jdvlpr/Temperature-Blanket-Web-App")
    )


def _extract_yarn_json(cwd: Path) -> dict:
    output = subprocess.check_output(
        ("bun", "run", cwd / "scripts" / "extract_yarns.ts"),
        text=True,
    )
    return json.loads(output)


def _f_to_byte(float_value: float) -> int:
    byte_value = float_value * 255
    if byte_value < 0:
        byte_value = 0
    if byte_value > 255:
        byte_value = 255
    return int(math.floor(byte_value))


def _generate_jpeg(hsl: tuple[float, float, float]) -> bytes:
    r, g, b = hsluv.hsluv_to_rgb(hsl)
    img = Image.new(
        mode="RGB",
        size=(1, 1),
        color=(_f_to_byte(r), _f_to_byte(g), _f_to_byte(b)),
    )
    f = io.BytesIO()
    img.save(f, format="jpeg")
    return f.getvalue()


async def main() -> None:
    cwd = Path.cwd()
    _ensure_git_checkout(cwd)
    yarn_json = _extract_yarn_json(cwd)

    engine = database.create_engine()
    await database.create_schema(engine)
    async with database.create_session(engine) as sess:
        for yarn_blob in yarn_json:
            h, s, l = hsluv.hex_to_hsluv(yarn_blob["hex"])
            yarn = Yarn(
                name=yarn_blob["name"],
                url=yarn_blob["url"],
                image=_generate_jpeg((h, s, l)),
                hue=h,
                saturation=s,
                lightness=l,
            )
            sess.add(yarn)


if __name__ == "__main__":
    asyncio.run(main())
