from fastapi import FastAPI
from uvicorn import run

from src.api import router

app = FastAPI()

app.include_router(router)


def main() -> None:
    run("src.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
