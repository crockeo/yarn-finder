from sqlalchemy.orm import Mapped, mapped_column

from yarn_finder.database import Base


class Yarn(Base):
    __tablename__ = "yarn"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    url: Mapped[str]
    image: Mapped[bytes]

    # Using HSLuv as the color space: https://www.hsluv.org/
    # X/Y/Z here so we can compute Euclidian distance
    x: Mapped[float]
    y: Mapped[float]
    z: Mapped[float]
