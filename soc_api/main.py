from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from soc_api.routers import incidents, zones, devices, federated, websocket

app = FastAPI(title="ShieldNet SOC Central API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(incidents.router)
app.include_router(zones.router)
app.include_router(devices.router)
app.include_router(federated.router)
app.include_router(websocket.router)


@app.get("/")
async def root():
    return {"service": "ShieldNet SOC API", "status": "operational"}


@app.get("/api/v1/health")
async def health():
    return {"status": "ok", "service": "soc-api", "version": "1.0.0"}
