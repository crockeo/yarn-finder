from base64 import b64decode, b64encode

from hsluv import hex_to_hsluv, hex_to_rgb, rgb_to_xyz
from sqlalchemy import Label, func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from yarn_finder.models import Yarn


async def get_yarns_close_to(
    sess: AsyncSession,
    rgb: str,
    *,
    pagination_token: str | None = None,
    page_size: int = 30,
) -> tuple[list[tuple[Yarn, float]], str | None]:
    xyz = rgb_to_xyz(hex_to_rgb(rgb))
    query = (
        select(
            Yarn,
            _distance(xyz).label("distance"),
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

    yarns = [(yarn, distance) for yarn, distance in yarns]
    return yarns, next_pagination_token


def _distance(xyz: tuple[int, int, int]) -> Label:
    x, y, z = xyz
    return func.sqrt(
        func.power(Yarn.x - x, 2)
        + func.power(Yarn.y - y, 2)
        + func.power(Yarn.z - z, 2)
    ).label("distance")


async def get_yarn(sess: AsyncSession, id: int) -> Yarn:
    return await sess.get_one(Yarn, id)
