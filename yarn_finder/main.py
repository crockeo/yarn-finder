import os

import uvicorn


def main() -> None:
    profile = os.environ.get("PROFILE", "dev")
    match profile:
        case "dev":
            uvicorn.run(
                "yarn_finder.wsgi:app",
                host="127.0.0.1",
                port=8080,
                reload=True,
            )

        case "prod":
            uvicorn.run(
                "yarn_finder.wsgi:app",
                uds="/tmp/uvicorn.sock",
            )


if __name__ == "__main__":
    main()
