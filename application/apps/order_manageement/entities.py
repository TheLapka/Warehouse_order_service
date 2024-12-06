from dataclasses import dataclass

@dataclass
class ProductInOrderEntity:
    product_id: int
    amount: int
    
@dataclass
class UserEntity:
    user_id:int
    email:str