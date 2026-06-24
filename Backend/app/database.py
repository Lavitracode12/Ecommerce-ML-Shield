from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "sqlite:///./shield_matrix.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    
    # Relationship to isolate products per user
    products = relationship("ProductModel", back_populates="owner")

class ProductModel(Base):
    __tablename__ = "user_products"
    
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, index=True)
    name = Column(String)
    base_price = Column(Float)
    competitor_price = Column(Float)
    stock_level = Column(Integer)
    days_to_restock = Column(Integer)
    search_velocity_multiplier = Column(Float)
    recommended_price = Column(Float)
    is_applied = Column(Boolean, default=False)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserModel", back_populates="products")

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()