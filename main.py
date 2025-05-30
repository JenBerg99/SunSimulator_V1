from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from api import router

app = FastAPI(
    title="Sonnenstand Simulator API",
    description="Simuliert Sonnenstand basierend auf Ort, Zeit und Wetter.",
    version="1.0.0"
)

# Global redirect to docs
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    
    # # Starte LCD-Display-Controller in einem Thread
    # display_thread = threading.Thread(target=main_loop, daemon=True)
    # display_thread.start()
    
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)