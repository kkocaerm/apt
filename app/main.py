import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine
from .routes.auth import router as auth_router
from .routes.units import router as units_router
from .routes.expenses import router as expenses_router
from .routes.payments import router as payments_router
from .routes.dashboard import router as dashboard_router
from .routes.exports import router as exports_router

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Apartment SaaS MVP")
origins = [x.strip() for x in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",") if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins or ["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth_router)
app.include_router(units_router)
app.include_router(expenses_router)
app.include_router(payments_router)
app.include_router(dashboard_router)
app.include_router(exports_router)

@app.get("/health")
def health():
    return {"ok": True}
