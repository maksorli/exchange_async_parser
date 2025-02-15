from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, String, DateTime, func


class Base(DeclarativeBase):
    pass


class Spimex(Base):
    __tablename__ = "spimex_trading_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exchange_product_id: Mapped[str] = mapped_column(String, nullable=False)
    exchange_product_name: Mapped[str] = mapped_column(String, nullable=False)
    oil_id: Mapped[str] = mapped_column(String, nullable=False)
    delivery_basis_id: Mapped[str] = mapped_column(String, nullable=False)
    delivery_basis_name: Mapped[str] = mapped_column(String, nullable=False)
    delivery_type_id: Mapped[str] = mapped_column(String, nullable=False)
    volume: Mapped[int] = mapped_column(Integer, nullable=False)
    total: Mapped[int] = mapped_column(Integer, nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    created_on: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_on: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
