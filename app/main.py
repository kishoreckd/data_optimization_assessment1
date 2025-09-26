from fastapi import FastAPI
from app.api.routes.route import router
from app.core.startup import lifespan  

app = FastAPI(title="Data Optimization Microservice", lifespan=lifespan)

app.include_router(router)
