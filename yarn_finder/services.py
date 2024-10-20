import math
from base64 import b64decode, b64encode

import hsluv
from sqlalchemy import Label, func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from yarn_finder.models import Yarn


_MAX_DISTANCE = math.sqrt(360**2 + 100**2 + 100**2)


async def get_yarns_close_to(
    sess: AsyncSession,
    rgb: str,
    *,
    pagination_token: str | None = None,
    page_size: int = 30,
) -> tuple[list[tuple[Yarn, float]], str | None]:
    if not rgb.startswith("#") or not len(rgb) == 7:
        raise ValueError(f"Invalid RGB color code: {rgb}")
    hsl = hsluv.hex_to_hsluv(rgb)
    print(hsl)
    query = (
        select(
            Yarn,
            _distance(hsl).label("distance"),
        )
        .order_by("distance")
        .limit(page_size + 1)
    )
    if pagination_token is not None:
        prev_max_id = int(b64decode(pagination_token).decode())
        query = query.where(Yarn.id > prev_max_id)

    yarns = list(await sess.execute(query))

    next_pagination_token = None
    if len(yarns) > page_size:
        yarns = yarns[:page_size]
        max_id = yarns[-1][0].id
        next_pagination_token = b64encode(str(max_id).encode()).decode()

    yarns = [(yarn, 1 - distance / _MAX_DISTANCE) for yarn, distance in yarns]
    return yarns, next_pagination_token


def _distance(hsl: tuple[float, float, float]) -> Label:
    hue, saturation, lightness = hsl
    return func.sqrt(
        func.power(Yarn.hue - hue, 2)
        + func.power(Yarn.saturation - saturation, 2)
        + func.power(Yarn.lightness - lightness, 2)
    ).label("distance")


async def get_yarn(sess: AsyncSession, id: int) -> Yarn:
    return await sess.get_one(Yarn, id)
