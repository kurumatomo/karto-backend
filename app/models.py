from typing import List, Optional
from datetime import datetime, date

from decimal import Decimal as PyDecimal

from sqlalchemy import (
    CheckConstraint, Column, Integer, String, ForeignKey, 
    Text, Date, TIMESTAMP, func, LargeBinary
)

from sqlalchemy.orm import (
    relationship, DeclarativeBase, Mapped, mapped_column
)

from sqlalchemy.dialects.mysql import (
    TINYINT, SMALLINT, MEDIUMINT, INTEGER, BIGINT, DECIMAL, MEDIUMBLOB
)

class Base(DeclarativeBase):
    pass


class GasType(Base):
    __tablename__ = "gas_types"

    id: Mapped[int] = mapped_column(SMALLINT(unsigned=True), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(15), nullable=False)

    # Relationships
    cars: Mapped[List["Car"]] = relationship(back_populates="gas_type_info")
    gas_prices: Mapped[List["GasPrice"]] = relationship(back_populates="gas_type_info")


class MaintenanceTypeDescription(Base):
    __tablename__ = "maintenance_type_descriptions"

    id: Mapped[int] = mapped_column(MEDIUMINT(unsigned=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)

    # Relationship
    items: Mapped[List["MaintenanceItemDetail"]] = relationship(back_populates="type_description")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(31), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    # Relationships
    cars: Mapped[List["Car"]] = relationship(back_populates="owner", cascade="all, delete-orphan")    
    trusted_links: Mapped[List["TrustedGasStation"]] = relationship(back_populates="user")
    
    # Shortcut to access stations directly
    trusted_stations: Mapped[List["GasStation"]] = relationship(
        secondary="trusted_gas_stations", 
        viewonly=True
    )


class GasStation(Base):
    __tablename__ = "gas_stations"

    # CRITICAL FIX: Added primary_key=True
    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    
    # Geo-coordinates
    longitude: Mapped[PyDecimal] = mapped_column(DECIMAL(9, 6), nullable=False)
    latitude: Mapped[PyDecimal] = mapped_column(DECIMAL(8, 6), nullable=False) # Lat is usually -90 to 90 (8,6)
    
    name: Mapped[str] = mapped_column(String(25), nullable=False)
    address_line: Mapped[str] = mapped_column(String(63), nullable=False)
    city: Mapped[str] = mapped_column(String(53), nullable=False)
    state: Mapped[str] = mapped_column(String(2), nullable=False) # e.g. "OH"
    zip: Mapped[str] = mapped_column(String(10), nullable=False)

    # Relationships
    trusted_by_links: Mapped[List["TrustedGasStation"]] = relationship(back_populates="station")
    prices: Mapped[List["GasPrice"]] = relationship(back_populates="station")


class TrustedGasStation(Base):
    __tablename__ = "trusted_gas_stations"

    trusted_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Foreign Keys
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    station_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), ForeignKey("gas_stations.id"), nullable=False)

    # Relationships to Parents
    user: Mapped["User"] = relationship(back_populates="trusted_links")
    station: Mapped["GasStation"] = relationship(back_populates="trusted_by_links")


class GasPrice(Base):
    __tablename__ = "gas_prices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    price: Mapped[PyDecimal] = mapped_column(DECIMAL(7, 4, unsigned=True), nullable=False)
    last_updated: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    station_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), ForeignKey("gas_stations.id"), nullable=False)
    gas_type_id: Mapped[int] = mapped_column(SMALLINT(unsigned=True), ForeignKey("gas_types.id"), nullable=False)

    # Relationships
    station: Mapped["GasStation"] = relationship(back_populates="prices")
    gas_type_info: Mapped["GasType"] = relationship(back_populates="gas_prices")


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)    
    car_vin: Mapped[str] = mapped_column(String(17), unique=True, nullable=False)
    make: Mapped[str] = mapped_column(String(20), nullable=False)
    model: Mapped[str] = mapped_column(String(40), nullable=False)
    color: Mapped[str | None] = mapped_column(String(15), nullable=True)    
    mileage: Mapped[int] = mapped_column(MEDIUMINT(unsigned=True), nullable=False)
    year: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint('year >= 1800 AND year <= 2200', name='check_year_range')
    )

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    gas_type_id: Mapped[int | None] = mapped_column(SMALLINT(unsigned=True), ForeignKey("gas_types.id"))
        
    # Relationships
    owner: Mapped["User"] = relationship(back_populates="cars")
    images: Mapped[List["CarImage"]] = relationship(back_populates="car", cascade="all, delete-orphan")
    gas_type_info: Mapped["GasType"] = relationship(back_populates="cars")
    maintenance_records: Mapped[List["Maintenance"]] = relationship(back_populates="car", cascade="all, delete-orphan")


class CarImage(Base):
    __tablename__ = "car_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image_data: Mapped[bytes] = mapped_column(MEDIUMBLOB, nullable=False)

    car_id: Mapped[int] = mapped_column(Integer, ForeignKey("cars.id"), nullable=False)
    
    # Relationships
    car: Mapped["Car"] = relationship(back_populates="images")


class Maintenance(Base):
    __tablename__ = "maintenance"

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    mileage: Mapped[int] = mapped_column(MEDIUMINT(unsigned=True), nullable=False)
    cost: Mapped[PyDecimal] = mapped_column(DECIMAL(7, 4, unsigned=True), nullable=False)

    car_id: Mapped[int] = mapped_column(Integer, ForeignKey("cars.id"), nullable=False)

    # Relationships
    car: Mapped["Car"] = relationship(back_populates="maintenance_records")
    items: Mapped[List["MaintenanceItemDetail"]] = relationship(back_populates="maintenance")
    receipt: Mapped["MaintenanceReceipt"] = relationship(back_populates="maintenance", uselist=False)


class MaintenanceItemDetail(Base):
    __tablename__ = "maintenance_item_details"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quantity: Mapped[int] = mapped_column(TINYINT(unsigned=True), default=1)
    comments: Mapped[str | None] = mapped_column(String(255), nullable=True)

    maintenance_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), ForeignKey("maintenance.id"), nullable=False)
    maintenance_type_id: Mapped[int] = mapped_column(MEDIUMINT(unsigned=True), ForeignKey("maintenance_type_descriptions.id"), nullable=False)

    # Relationships
    maintenance: Mapped["Maintenance"] = relationship(back_populates="items")
    type_description: Mapped["MaintenanceTypeDescription"] = relationship(back_populates="items")


class MaintenanceReceipt(Base):
    __tablename__ = "maintenance_receipts"

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True)
    image_data: Mapped[bytes] = mapped_column(MEDIUMBLOB)

    maintenance_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), ForeignKey("maintenance.id"), unique=True, nullable=False)

    # Relationship
    maintenance: Mapped["Maintenance"] = relationship(back_populates="receipt")
