from faststream import FastStream
from faststream.kafka import KafkaBroker
from pydantic import BaseModel

broker = KafkaBroker("localhost:29092")  # Your external Kafka listener
app = FastStream(broker)

# Define your message schema
class MyMessage(BaseModel):
    name: str
    age: int

# Kafka consumer
@broker.subscriber("my-topic")
async def handle_message(msg: MyMessage):
    print(f"Received: {msg.name} (age {msg.age})")

# Kafka producer (runs once at startup)
@app.after_startup
async def send_example(app):
    await broker.publish(
        MyMessage(name="Rami", age=30),
        topic="my-topic"
    )
