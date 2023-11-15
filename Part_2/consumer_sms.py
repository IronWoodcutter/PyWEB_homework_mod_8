import pika
import pickle

from producer import Contact
from time import sleep

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

sms_queue_name = "web_16_campaign_sms"

channel.queue_declare(queue=sms_queue_name, durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def send_sms(phone):
    print(f"SMS for phone:{phone} was sent")
    sleep(0.3)


def callback(ch, method, properties, body):
    object_id = pickle.loads(body)
    contact = Contact.objects(id=object_id)[0]
    phone = contact.phone

    print(f" [x] Received task to send SMS for {contact.fullname}")
    send_sms(phone)
    contact.is_sent = True
    contact.save()
    print(f" [x] Done: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=sms_queue_name, on_message_callback=callback)


if __name__ == '__main__':
    channel.start_consuming()
