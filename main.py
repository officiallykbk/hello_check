from fastapi import FastAPI
import socket

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World from Jenkins!", "container_id": socket.gethostname()}

@app.get("/health")
def health():
    return {"message": "At long last we ended with bang...maybe!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
