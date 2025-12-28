from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://easyretain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fake customers data (no database)
customers = [
    {"id": 1, "name": "John Doe", "age": 30, "phone": "+1 555 123"},
    {"id": 2, "name": "Anna Smith", "age": 25, "phone": "+1 555 456"},
    {"id": 3, "name": "Michael Brown", "age": 40, "phone": "+1 555 789"},
    {"id": 4, "name": "Sophia Wilson", "age": 35, "phone": "+1 555 111"},
    {"id": 5, "name": "David Lee", "age": 28, "phone": "+1 555 222"},
]

@app.get("/")
def root():
    return {"status": "Backend is running"}

@app.get("/customers")
def get_customers():
    return customers
