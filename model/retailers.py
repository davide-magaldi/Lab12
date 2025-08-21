from dataclasses import dataclass


@dataclass(order=True)
class Retailer:
    Retailer_code:int
    Retailer_name:str
    Type:str
    Country:str

    def __hash__(self):
        return hash(self.Retailer_code)

    def __eq__(self, other):
        return self.Retailer_code == other.Retailer_code

