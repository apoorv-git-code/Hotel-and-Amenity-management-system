class Customer:
    def __init__(self, name, contact, customer_id):
        self.name = name
        self.contact = contact
        self.id = customer_id

    def to_dict(self):
        return {
            "name": self.name,
            "contact": self.contact,
            "id": self.id
        }

