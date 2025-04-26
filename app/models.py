from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from datetime import date
from typing import List

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

service_mechanic = db.Table(
    "service_mechanic",
    Base.metadata,
    db.Column("service_ticket_id", db.ForeignKey("service_tickets.id")),
    db.Column("mechanic_id", db.ForeignKey("mechanics.id"))                                         
)

class Customer(Base):
    __tablename__ = "customers"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(20))
    
    service_tickets: Mapped[List["ServiceTicket"]] = db.relationship(back_populates="customer")
    
class ServiceTicket(Base):
    __tablename__ = "service_tickets"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(String(100))
    service_date: Mapped[str] = mapped_column(String(100))
    service_desc: Mapped[str] = mapped_column(String(100))
    customer_id: Mapped[int] = mapped_column(db.ForeignKey("customers.id"))
    
    customer: Mapped["Customer"] = db.relationship(back_populates="service_tickets")
    mechanics: Mapped[List["Mechanic"]] = db.relationship(secondary = service_mechanic, back_populates="service_tickets")
    
class Mechanic(Base):
    __tablename__ = "mechanics"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(100))
    salary: Mapped[float]
    
    service_tickets: Mapped[List["ServiceTicket"]] = db.relationship(secondary = service_mechanic, back_populates="mechanics")
    