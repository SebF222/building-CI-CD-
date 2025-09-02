from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Date, ForeignKey, Float, Table, Integer, Column, ForeignKey, DateTime
from datetime import datetime, date






class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class= Base)

ticket_mechanics = Table(
    'ticket_mechanic',
    Base.metadata,
    Column('ticket_id', Integer, ForeignKey('service_tickets.id')),
    Column('mechanic_id', Integer, ForeignKey('mechanics.id'), nullable=False)
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


    customer: Mapped['Customers'] = relationship('Customers', back_populates='service_tickets')

    mechanics: Mapped[list['Mechanics']] = relationship(
        'Mechanics',
        secondary=ticket_mechanics,
        back_populates='service_tickets'
    )

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


