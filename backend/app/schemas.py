from typing import Optional, List
from pydantic import BaseModel, Field


class ProfileBase(BaseModel):
    display_name: str = Field(..., description="User-facing name")
    bio: Optional[str] = Field(default="", description="Bio text")
    height_cm: Optional[int] = Field(default=None, description="Height in centimeters")
    weight_kg: Optional[int] = Field(default=None, description="Weight in kilograms")
    gender: str = Field(..., description="Gender value")
    photo_url: Optional[str] = Field(default="", description="Primary photo URL")
    interests: Optional[list] = Field(default_factory=list, description="List of interest tags")


class ProfileCreate(ProfileBase):
    user_id: int = Field(..., description="Owner user ID")


class ProfileUpdate(BaseModel):
    display_name: Optional[str] = None
    bio: Optional[str] = None
    height_cm: Optional[int] = None
    weight_kg: Optional[int] = None
    gender: Optional[str] = None
    photo_url: Optional[str] = None
    interests: Optional[list] = None


class ProfileOut(ProfileBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class HeightCategoryOut(BaseModel):
    id: int
    name: str
    min_cm: Optional[int] = None
    max_cm: Optional[int] = None

    class Config:
        from_attributes = True


class WeightCategoryOut(BaseModel):
    id: int
    name: str
    min_kg: Optional[int] = None
    max_kg: Optional[int] = None

    class Config:
        from_attributes = True
