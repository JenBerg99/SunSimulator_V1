from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from api import router

# Create the FastAPI app with metadata
app = FastAPI(
    title="Sun Simulator API",
    description="Simulates sunlight conditions based on location, time, and weather.",
    version="1.0.1"
)

# Temporary redirect from root ("/") to the interactive documentation.
# TODO: This is useful during development, but should be removed or changed before deployment.
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

# Include all API routes from the 'api' module
app.include_router(router)

# Run the application using Uvicorn when the script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
