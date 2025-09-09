from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Date, ForeignKey, Float, Table, Integer, Column, ForeignKey, DateTime
from datetime import datetime, date
from .extensions import db

class Base(db.Model):
    __abstract__ = True
    pass

ticket_mechanics = Table(
    'ticket_mechanic',
    Base.metadata,
    Column('ticket_id', Integer, ForeignKey('service_tickets.id')),
    Column('mechanic_id', Integer, ForeignKey('mechanics.id'), nullable=False)
)

# Simple junction table for tickets and parts
ticket_parts = Table(
    'ticket_parts',
    Base.metadata,
    Column('ticket_id', Integer, ForeignKey('service_tickets.id')),
    Column('part_id', Integer, ForeignKey('parts.id'))
)



class Customers(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(250), nullable=False)
    last_name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(360), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(13), unique=True, nullable=False)
    address: Mapped[str] = mapped_column(String(1000), nullable=True)

    service_tickets: Mapped[list['Service_tickets']] = relationship('Service_tickets', back_populates='customer')



class Service_tickets(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    customers_id: Mapped[int] = mapped_column(ForeignKey('customers.id'), nullable=False)
    description: Mapped[str] = mapped_column(String(500))
    price: Mapped[float] = mapped_column(Float)
    vin: Mapped[str] = mapped_column(String(17), unique=True, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


    customer: Mapped['Customers'] = relationship('Customers', back_populates='service_tickets')

    mechanics: Mapped[list['Mechanics']] = relationship(
        'Mechanics',
        secondary=ticket_mechanics,
        back_populates='service_tickets'
    )
    
    parts: Mapped[list['Parts']] = relationship('Parts', back_populates='ticket')

class Mechanics(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(250), nullable=False)
    last_name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(360), unique=True, nullable=False)
    DOB: Mapped[date] = mapped_column()
    password: Mapped[str] = mapped_column(String(15), nullable=False)
    salary: Mapped[float] = mapped_column(Float, nullable=False)
    address: Mapped[str] = mapped_column(String(1000), nullable=False)


    service_tickets: Mapped[list['Service_tickets']] = relationship(
        'Service_tickets',
        secondary=ticket_mechanics,
        back_populates='mechanics'
    )



# Inventory model (part description)
class Inventory(Base):
    __tablename__ = 'inventory'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    parts: Mapped[list['Parts']] = relationship('Parts', back_populates='inventory')

# Parts model (actual part used on a ticket)
class Parts(Base):
    __tablename__ = 'parts'

    id: Mapped[int] = mapped_column(primary_key=True)
    desc_id: Mapped[int] = mapped_column(ForeignKey('inventory.id'), nullable=False)
    ticket_id: Mapped[int] = mapped_column(ForeignKey('service_tickets.id'), nullable=True)

    inventory: Mapped['Inventory'] = relationship('Inventory', back_populates='parts')
    ticket: Mapped['Service_tickets'] = relationship('Service_tickets', back_populates='parts')



    