from enum import Enum
from pydantic import BaseModel

class User_Role(str,Enum):
    Admin = "Admin"
    SERVICEPROVIDER = "Service Provider"
    CUSTOMER = "Customer"

