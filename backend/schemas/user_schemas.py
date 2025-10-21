from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    FullName: str
    Email: str
    Password: str
    Role: str = "Customer"
    
class UserUpdate(BaseModel):
    username: Optional[str] = None
    Email: Optional[str] = None
    Password: Optional[str] = None
    Phone: Optional[str] = None
    Address: Optional[str] = None
    City: Optional[str] = None
    Country: Optional[str] = None
    