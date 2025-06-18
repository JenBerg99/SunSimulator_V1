from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from api import router
from rpi.led_service import start_led_thread, shutdown_led
from rpi.rotary_service import start_rotary_thread, stop_rotary
from rpi.lcd.I2CLCD1602 import lcd_setup, lcd_destroy

# Create the FastAPI app with metadata
app = FastAPI(
    title="Sun Simulator API",
    description="Simulates sunlight conditions based on location, time, and weather.",
    version="1.0.1"
)

@app.on_event("startup")
async def startup_event():
    #start the thread for the LED Service
    start_led_thread()
    start_rotary_thread()
    lcd_setup()

@app.on_event("shutdown")
async def startup_event():
    #start the thread for the LED Service
    shutdown_led()
    stop_rotary()
    lcd_destroy()

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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)