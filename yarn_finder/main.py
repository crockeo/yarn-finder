import uvicorn


def main() -> None:
    uvicorn.run(
        "yarn_finder.wsgi:app",
        host="127.0.0.1",
        port=8080,
        reload=True,
    )


if __name__ == "__main__":
    main()
