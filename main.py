from app.routes.invoice import router_invoice
from fastapi import FastAPI

app = FastAPI()

app.include_router(router=router_invoice)
