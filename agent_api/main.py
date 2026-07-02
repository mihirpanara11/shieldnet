from fastapi import FastAPI, Depends
from agent_api.routers import health, devices, threats, airo
from agent_api.auth.jwt_handler import JWTHandler

app = FastAPI(title="ShieldNet Edge Agent API", version="1.0.0")

jwt_handler = JWTHandler()

auth_dependency = Depends(jwt_handler.require_auth)

app.include_router(health.router, dependencies=[auth_dependency])
app.include_router(devices.router, dependencies=[auth_dependency])
app.include_router(threats.router, dependencies=[auth_dependency])
app.include_router(airo.router, dependencies=[auth_dependency])


@app.get("/")
async def root():
    return {"service": "ShieldNet Agent API", "status": "operational"}
