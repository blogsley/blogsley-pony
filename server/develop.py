import uvicorn

if __name__ == "__main__":
    #uvicorn.run("blogsley:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
    uvicorn.run("blogsley:app", host="0.0.0.0", port=8000, reload=True, log_level="info")