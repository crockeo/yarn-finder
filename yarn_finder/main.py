import os
import sys

import uvicorn


def main() -> None:
    uvicorn.run(
        "yarn_finder.wsgi:app",
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "8080")),
        reload=sys.platform == "darwin",
    )


if __name__ == "__main__":
    main()
