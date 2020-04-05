import uvicorn

if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# WARNING:  You must pass the application as an import string to enable 'reload' or 'workers'.
def develop(app):
    uvicorn.run('blogsley:app', host="127.0.0.1", port=5000, reload=True, log_level="info")

if __name__ == "__main__":
    from blogsley.application import create_app
    app = create_app()
    develop(app)
