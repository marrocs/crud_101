class Product:
    def __init__(self, id, name, quantity) -> None:
        self.id = id
        self.name = name
        self.quantity = quantity

    def __repr__(self) -> str:
        return f'<id: {self.id}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity
        }
    
class Order:
    def __init__(self, id, client_id, items) -> None:
        self.id = id,
        self.client_id = client_id,
        self.items = items

    def __repr__(self) -> str:
        return f'<id: {self.id},\nclient:{self.client_id}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'items': self.items
        }

class Client:
    def __init__(self, id, name) -> None:
        self.id = id,
        self.name = name

    def __repr__(self) -> str:
        return f'<id: {self.id}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }