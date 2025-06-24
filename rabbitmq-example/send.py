# Producer

import pika
import time

time.sleep(5)  # Wait for RabbitMQ to start

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()

channel.queue_declare(queue='hello')
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello from Producer!')
print(" [x] Sent 'Hello from Producer!'")

connection.close()
