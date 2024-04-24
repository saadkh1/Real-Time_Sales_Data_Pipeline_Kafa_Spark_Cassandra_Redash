from fastapi import FastAPI, status
from pydantic import BaseModel
from kafka import KafkaProducer
import json

def serializer(message):
    return json.dumps(message).encode('utf-8')

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=serializer
)

class SalesItem(BaseModel):
    pos_id: int
    pos_name: str
    article: str
    quantity: float
    unit_price: float
    total: float
    sale_type: str
    payment_mode: str
    sale_time: str

app = FastAPI()

@app.post("/salesitem", status_code=status.HTTP_201_CREATED)
async def create_sales(item: SalesItem):

    producer.send("Sales", value=item.dict())

    return {"status": "success", "message": "Stock entry created"}