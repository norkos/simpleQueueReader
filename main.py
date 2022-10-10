import json
import pika
import os

params = pika.URLParameters(os.getenv('CLOUDAMQP_URL'))
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='main', durable=True)

messages = []


def callback(ch, method, properties, body):
    data = json.loads(body)
    messages.append(data)
    print(data)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=False)
print('Started consuming')

channel.start_consuming()


