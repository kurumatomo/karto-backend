from decimal import Decimal as PyDecimal
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List
from datetime import datetime, date

# - - - User Schemas - - -
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    pass

class UserUpdate(BaseModel):
    pass

# - - - Car Schemas - - -
class CarBase(BaseModel):
    pass

class CarCreate(CarBase):
    pass

class CarResponse(CarBase):
    pass

class CarUpdate(CarBase):
    pass

# - - - Car Images - - -
class CarImage(BaseModel):
    pass

class CarImageResponse(CarImage):
    pass

class CarImageUpdate(CarImage):
    pass

# - - - Maintenance Schemas - - -
class MaintenanceBase(BaseModel):
    pass

class MaintenanceUpdate(MaintenanceBase):
    pass

class MaintenanceResponse(MaintenanceBase):
    pass

# - - - Maintenance Detail Schemas - - -
class MaintenanceDetailBase(BaseModel):
    pass

class MaintenanceDetailCreate(MaintenanceDetailBase):
    pass

class MaintenanceDetailResponse(MaintenanceDetailBase):
    pass

class MaintenanceDetailUpdate(MaintenanceDetailBase):
    pass

class MaintenanceReciptBase(BaseModel):
    pass

class MaintenanceReciptResponse(MaintenanceReciptBase):
    pass

# - - - Gas Station Schemas - - -
class GasStationBase(BaseModel):
    pass

class GasStationCreate(GasStationBase):
    pass

class GasStationResponse(GasStationBase):
    pass

class GasStationUpdate(GasStationBase):
    pass

# - - - Gas Price Schemas - - - 
class GasPriceBase(BaseModel):
    pass

class GasPriceUpdate(GasPriceBase):
    pass

class GasPriceResponse(GasPriceBase):
    pass

# - - - Gas Type Schemas - - -
class GasTypeBase(BaseModel):
    pass

class GasTypeResponse(GasTypeBase):
    pass

class GasTypeUpdate(GasTypeBase):
    pass
