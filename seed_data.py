import asyncio
import io
import math
import random

import faker_commerce
import hsluv
from faker import Faker
from PIL import Image

from yarn_finder.database import create_engine, create_schema, create_session
from yarn_finder.models import Yarn


def f_to_byte(float_value: float) -> int:
    byte_value = float_value * 255
    if byte_value < 0:
        byte_value = 0
    if byte_value > 255:
        byte_value = 255
    return int(math.floor(byte_value))


def _generate_jpeg(r: float, g: float, b: float) -> bytes:
    img = Image.new(
        mode="RGB",
        size=(1, 1),
        color=(f_to_byte(r), f_to_byte(g), f_to_byte(b)),
    )
    f = io.BytesIO()
    img.save(f, format="jpeg")
    return f.getvalue()


def _generate_random_yarn(faker: Faker) -> Yarn:
    r, g, b = (random.random(), random.random(), random.random())
    h, s, l = hsluv.rgb_to_hsluv((r, g, b))
    jpeg = _generate_jpeg(r, g, b)
    return Yarn(
        name=faker.ecommerce_name(),
        url=faker.uri(),
        image=jpeg,
        hue=h,
        saturation=s,
        lightness=l,
    )


async def main() -> None:
    engine = create_engine()
    await create_schema(engine)

    faker = Faker()
    faker.add_provider(faker_commerce.Provider)
    async with create_session(engine) as sess:
        for _ in range(10_000):
            yarn = _generate_random_yarn(faker)
            sess.add(yarn)


if __name__ == "__main__":
    asyncio.run(main())
