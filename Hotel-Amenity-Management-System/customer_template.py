class Customer:
    def __init__(self, name, contact, email_id, city):
        self.name = name
        self.contact = contact
        self.email_id = email_id
        self.city = city

    def to_dict(self):
        return {
            "name": self.name,
            "contact": self.contact,
            "email_id": self.email_id,
            "city": self.city
        }

