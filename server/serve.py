import uvicorn

'''
async def app(scope, receive, send):
    ...
'''

if __name__ == "__main__":
    uvicorn.run("blogsley:app", host="0.0.0.0", port=8000, log_level="info")