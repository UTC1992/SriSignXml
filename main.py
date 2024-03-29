from app.routes.invoice import routerInvoice
from fastapi import FastAPI

app = FastAPI()

app.include_router(router=routerInvoice)
