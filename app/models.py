from sqlalchemy import CheckConstraint, Column, Integer, Nullable, String, Boolean, ForeignKey, Text, SmallInteger, Date, TIMESTAMP, func, LargeBinary
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from datetime import datetime, date
from decimal import Decimal as PyDecimal
from sqlalchemy.dialects.mysql import (
    TINYINT, 
    SMALLINT, 
    MEDIUMINT, 
    INTEGER, 
    BIGINT,
    DECIMAL
)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(31), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    # Relationships
    # User - Trusted Gas Station
    # User - Car
    # Will implement later

class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    car_vin: Mapped[str] = mapped_column(String(17), unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    make: Mapped[str] = mapped_column(String(20), nullable=False)
    model: Mapped[str] = mapped_column(String(40), nullable=False)

    year: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint('year >= 1800 AND year <= 2200', name='check_year_range')
    )

    color: Mapped[str | None] = mapped_column(String(15), nullable=True)    
    mileage: Mapped[int] = mapped_column(MEDIUMINT(unsigned=True), nullable=False)
    gas_type: Mapped[int] = mapped_column(SMALLINT(unsigned=True), nullable=False)

    # Add this to the Schemas later for validation
    # year: int = Field(
    #     ..., 
    #     ge=1886,             
    #     le=current_year + 1,
    #     description="The manufacturing year of the car"
    # )
    #
    # Relationships
    # Car - Car Image
    # Car - Maintenance Recipt
    # Car - Gas Type
    # Car - Trusted Gas Station

class CarImg(Base):
    __tablename__ = "car_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)

    # Mapping Car - Image
    car: Mapped["Car"] = relationship(back_populates="images")

class GasStation(Base):
    __tablename__ = "gas_stations"

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False)
    longitude: Mapped[PyDecimal] = mapped_column(DECIMAL(9, 6), nullable=False)
    latitude: Mapped[PyDecimal] = mapped_column(DECIMAL(9, 6), nullable=False)
    name: Mapped[str] = mapped_column(String(25), nullable=False)
    address_line: Mapped[str] = mapped_column(String(63), nullable=False)
    city: Mapped[str] = mapped_column(String(53), nullable=False)
    state: Mapped[str] = mapped_column(String(2), nullable=False)
    zip: Mapped[str] = mapped_column(String(10), nullable=False)

    # RelationShips
    # Gas Station - Gas Price
    # Gas Station - Trusted Gas Station

class TrustedGasStation(Base):
    __tablename__ = "trusted_gas_stations"

    trusted_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    station_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), ForeignKey("gas_stations.id"), nullable=False)

    # Relationships
    # Trusted Gas Station - User
    # Trusted Gas Station - Gas Station
    # Trusted Gas Station - Car

class GasPrice(Base):
    __tablename__ = "gas_price"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    station_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), ForeignKey("users.id"), nullable=False)
    price: Mapped[PyDecimal] = mapped_column(DECIMAL(7,4, unsigned=True), nullable=False)

    # Date still needs to be implemented
    last_updated: Mapped[date] = mapped_column()

    gas_type: Mapped[int] = mapped_column(SMALLINT(unsigned=True), nullable=False)

    # Relationships
    # stationid - gas station
    # gas price - gas type

class GasType(Base):
    __tablename__ = "gas_types"

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, index=True)    
    name: Mapped[str] = mapped_column(String(15), nullable=False)

    # Relationships
    # gas type - gas price
    # gas type - car

class Maintenance(Base):
    __tablename__ = "maintenance"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    car_id: Mapped[int] = mapped_column(Integer, ForeignKey("car.id"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    mileage: Mapped[int] = mapped_column(Integer, nullable=False)
    cost: Mapped[PyDecimal] = mapped_column(DECIMAL(7,4, unsigned=True), nullable=False)

    # Relationships
    # maintenance - maintenance item detail
    # maintenance - car id

class MaintenanceDetail(Base):
    __tablename__ = "maintenance_item_details"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    maintenance_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), ForeignKey("maintenance.id"), nullable=False)
    maintenance_type_id: Mapped[int] = mapped_column(MEDIUMINT(unsigned=True), nullable=False)
    quantity: Mapped[int] = mapped_column(TINYINT(unsigned=True), nullable=False)
    comments: Mapped[str | None] = mapped_column(String(255), nullable=True)

class MaintenanceTypeDescription(Base):
    __tablename__ = "maintenance_type_description"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)

    # Relationship
    # maintenance description - Maintenance item detail

class MaintenanceRecipt(Base):
    __tablename__ = "maintenance_recipts"

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, index=True)
    image: Mapped[bytes | None] = mapped_column(LargeBinary)

    # Relationship
    # Recipt to car
