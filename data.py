from dataclasses import dataclass, field
from typing import Dict, List

@dataclass(eq=True)
class House:
    type: str = None
    address:str = None
    url: str = None
    price:Dict[str, int] = field(default_factory=dict)
    total_price: float = None
    area: float = None
    bedrooms:int = None
    bathrooms:int = None
    parking:int = None
    amenities: List[str] = field(default_factory=list)
    description: str = None
    transport: str = None
    publisher_name: str = None
    code:str = None
    title:str = None

links = list()
