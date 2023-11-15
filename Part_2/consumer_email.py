import pika
import pickle

from producer import Contact
from time import sleep

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

email_queue_name = "web_16_campaign_email"

channel.queue_declare(queue=email_queue_name, durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def send_email(email):
    print(f"Message for email:{email} was sent")
    sleep(0.3)


def callback(ch, method, properties, body):
    object_id = pickle.loads(body)
    contact = Contact.objects(id=object_id)[0]
    email = contact.email

    print(f" [x] Received task for sending e-mail for {contact.fullname}")
    send_email(email)
    contact.is_sent = True
    contact.save()
    print(f" [x] Done: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=email_queue_name, on_message_callback=callback)


if __name__ == '__main__':
    channel.start_consuming()
