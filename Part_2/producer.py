import pika
import pickle
import random

from faker import Faker

from models import Contact

NUMBER_CONTACTS = 50


def generate_contacts(num):
    fake = Faker()
    for _ in range(num):
        contact = Contact(
            fullname=fake.name(),
            age=random.randint(18, 130),
            email=fake.email(),
            phone=fake.phone_number(),
            preferred_send_method=fake.random_element(['email', 'sms']),
            is_sent=False
        ).save()


def main():
    credentials = pika.PlainCredentials('guest', 'guest')

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))

    channel = connection.channel()

    exchange = "Web16_Service"
    email_queue_name = "web_16_campaign_email"
    sms_queue_name = "web_16_campaign_sms"

    channel.exchange_declare(exchange=exchange, exchange_type='topic')

    channel.queue_declare(queue=email_queue_name, durable=True)
    channel.queue_bind(exchange=exchange, queue=email_queue_name, routing_key='email')

    channel.queue_declare(queue=sms_queue_name, durable=True)
    channel.queue_bind(exchange=exchange, queue=sms_queue_name, routing_key='sms')

    generate_contacts(NUMBER_CONTACTS)
    contacts = Contact.objects.all()
    for contact in contacts:
        message = pickle.dumps(contact.id)
        routing_key = contact.preferred_send_method
        # print(routing_key)
        # print(contact.fullname)
        channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
        print(f" [x] Message {routing_key} for '{contact.fullname}' id '{contact.id}' sent to queue")

    connection.close()


if __name__ == '__main__':
    main()
