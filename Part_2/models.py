from mongoengine import connect, Document, StringField, BooleanField, IntField

connect(host='mongodb+srv://Oleksandr:567234@goit.5380vln.mongodb.net/')


class Contact(Document):
    fullname = StringField(max_length=50, required=True)
    age = IntField()
    email = StringField(max_length=50, required=True)
    phone = StringField(max_length=50, required=True)
    preferred_send_method = StringField(max_length=10, required=True)
    is_sent = BooleanField(bool=False, required=True)
