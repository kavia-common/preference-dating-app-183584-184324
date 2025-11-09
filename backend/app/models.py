from datetime import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from sqlalchemy import String, Integer, BigInteger, Boolean, Text, ForeignKey, DateTime, JSON, UniqueConstraint

Base = declarative_base()


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class User(Base, TimestampMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    profile: Mapped["Profile"] = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    filter_settings: Mapped["FilterSettings"] = relationship("FilterSettings", back_populates="user", uselist=False, cascade="all, delete-orphan")


class Profile(Base, TimestampMixin):
    __tablename__ = "profiles"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    bio: Mapped[str] = mapped_column(Text, default="", nullable=False)
    height_cm: Mapped[Optional[int]] = mapped_column(Integer)
    weight_kg: Mapped[Optional[int]] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(String(32), nullable=False)
    photo_url: Mapped[str] = mapped_column(String(200), default="", nullable=False)
    interests: Mapped[dict] = mapped_column(JSON, default=list, nullable=False)

    user: Mapped[User] = relationship("User", back_populates="profile")
    photos: Mapped[list["Photo"]] = relationship("Photo", back_populates="profile", cascade="all, delete-orphan")


class Photo(Base, TimestampMixin):
    __tablename__ = "photos"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id", ondelete="CASCADE"), index=True)
    url: Mapped[str] = mapped_column(String(250), nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    profile: Mapped[Profile] = relationship("Profile", back_populates="photos")


class Match(Base, TimestampMixin):
    __tablename__ = "matches"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    matched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    user_a_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    user_b_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    __table_args__ = (UniqueConstraint("user_a_id", "user_b_id", name="uq_match_pair"),)


class Message(Base, TimestampMixin):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id", ondelete="CASCADE"), index=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)


class HeightCategory(Base):
    __tablename__ = "height_categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    min_cm: Mapped[Optional[int]] = mapped_column(Integer)
    max_cm: Mapped[Optional[int]] = mapped_column(Integer)


class WeightCategory(Base):
    __tablename__ = "weight_categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    min_kg: Mapped[Optional[int]] = mapped_column(Integer)
    max_kg: Mapped[Optional[int]] = mapped_column(Integer)


class FilterSettings(Base, TimestampMixin):
    __tablename__ = "filter_settings"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    height_category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("height_categories.id", ondelete="SET NULL"))
    weight_category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("weight_categories.id", ondelete="SET NULL"))
    genders: Mapped[dict] = mapped_column(JSON, default=list, nullable=False)

    user: Mapped[User] = relationship("User", back_populates="filter_settings")


class Session(Base, TimestampMixin):
    __tablename__ = "sessions"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    token: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
