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

if __name__ == "__main__":
    sample_customer = Customer("Test User", "1234567890", "test@example.com", "Test City")
    print("Sample Customer:")
    print(sample_customer.to_dict())


