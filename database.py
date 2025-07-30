# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
# import gnupg # Временно отключаем gnupg

# Путь к домашней директории GnuPG
GPG_HOME_DIR = os.getenv("GPG_HOME_DIR", os.path.expanduser("~/.gnupg"))

# gpg = gnupg.GPG(gnupghome=GPG_HOME_DIR) # Временно отключаем
# Добавьте ваш публичный ключ для шифрования и приватный ключ для дешифрования
# Например, IMPORTER_PUBLIC_KEY = "..."
# gpg.import_keys(IMPORTER_PUBLIC_KEY)

# Ваш email, связанный с PGP ключом для шифрования/дешифрования
PGP_RECIPIENT_EMAIL = os.getenv("PGP_RECIPIENT_EMAIL", "your_email@example.com")

def encrypt_data(data: str) -> str:
    # Временно отключаем шифрование
    return data
    # if not PGP_RECIPIENT_EMAIL:
    #     print("PGP_RECIPIENT_EMAIL не установлен, данные не будут зашифрованы.")
    #     return data
    # try:
    #     encrypted_data = gpg.encrypt(data, recipients=[PGP_RECIPIENT_EMAIL])
    #     if encrypted_data.ok:
    #         return str(encrypted_data)
    #     else:
    #         print(f"Ошибка шифрования: {encrypted_data.status} - {encrypted_data.stderr}")
    #         return data # Возвращаем несшифрованные данные в случае ошибки
    # except Exception as e:
    #     print(f"Исключение при шифровании: {e}")
    #     return data

def decrypt_data(encrypted_data: str) -> str:
    # Временно отключаем дешифрование
    return encrypted_data
    # try:
    #     decrypted_data = gpg.decrypt(encrypted_data)
    #     if decrypted_data.ok:
    #         return str(decrypted_data)
    #     else:
    #         print(f"Ошибка дешифрования: {decrypted_data.status} - {decrypted_data.stderr}")
    #         return encrypted_data # Возвращаем зашифрованные данные в случае ошибки
    # except Exception as e:
    #     print(f"Исключение при дешифровании: {e}")
    #     return encrypted_data


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./airdrop_hunter.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Модель пользователя
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    wallet_address = Column(String, unique=True, nullable=True) # Теперь будет хранить зашифрованные данные
    email = Column(String, unique=True, nullable=True) # Теперь будет хранить зашифрованные данные
    is_premium = Column(Boolean, default=False)
    rating = Column(Integer, default=0)
    premium_until = Column(DateTime, nullable=True)
    referrer_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    referred_users = relationship("User", backref='referrer', remote_side=[id])
    hunt_tokens = Column(Float, default=0.0)
    email_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)
    daily_airdrops_count = Column(Integer, default=0)
    last_airdrop_date = Column(DateTime, nullable=True)

# Модель для аирдропов
class Airdrop(Base):
    __tablename__ = "airdrops"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    source_url = Column(String, unique=True, nullable=False)
    referral_link = Column(String, nullable=True)  # Реферальная ссылка
    blockchain = Column(String, nullable=True)
    difficulty = Column(String, nullable=True)
    status = Column(String, default="new")
    reward = Column(String, nullable=True)
    end_date = Column(DateTime, nullable=True)
    is_moderated = Column(Boolean, default=False)

# Модель для NFT-бейджей
class NftBadge(Base):
    __tablename__ = "nft_badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    user_id = Column(Integer, index=True)


# Создание таблиц в базе данных
def init_db():
    Base.metadata.create_all(bind=engine) 