import math

import hsluv
from sqlalchemy import Label, func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from yarn_finder.models import Yarn


_MAX_DISTANCE = math.sqrt(360**2 + 100**2 + 100**2)


# TODO: this does offset pagination because the original methid (paginating through IDs)
# doesn't actually matter, since we're sorting by another (float-valued!!!) key
async def get_yarns_close_to(
    sess: AsyncSession,
    rgb: str,
    *,
    offset: int | None = None,
    page_size: int = 30,
) -> tuple[list[tuple[Yarn, float]], int]:
    if not rgb.startswith("#") or not len(rgb) == 7:
        raise ValueError(f"Invalid RGB color code: {rgb}")
    if offset is None:
        offset = 0

    hsl = hsluv.hex_to_hsluv(rgb)
    query = (
        select(
            Yarn,
            _distance(hsl).label("distance"),
        )
        .order_by("distance")
        .offset(offset)
        .limit(page_size + 1)
    )

    yarns = list(await sess.execute(query))

    yarns = [
        (yarn, 1 - distance / _MAX_DISTANCE)
        for yarn, distance in yarns
        if distance / _MAX_DISTANCE <= 0.10
    ]
    return yarns, offset + page_size + 1


def _distance(hsl: tuple[float, float, float]) -> Label:
    hue, saturation, lightness = hsl
    return func.sqrt(
        func.power(Yarn.hue - hue, 2)
        + func.power(Yarn.saturation - saturation, 2)
        + func.power(Yarn.lightness - lightness, 2)
    ).label("distance")


async def get_yarn(sess: AsyncSession, id: int) -> Yarn:
    return await sess.get_one(Yarn, id)
