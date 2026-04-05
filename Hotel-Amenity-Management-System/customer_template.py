class customer:
    def __init__(self,name,contact,id):
        self.name=name
        self.contact=contact
        self.id=id
    
    def conversion_to_dict(c1):
        return {
            "name":c1.name,
            "contact":c1.contact,
            "id":c1.id
        }
        
