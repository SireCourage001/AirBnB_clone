#!/usr/bin/python3
"""
class Review that inherits from BaseModel
"""

from models.base_model import BaseModel

class Review(BaseModel):
    """
    Summation: Defines the Review class that inherits from BAseModel
    Public class attributes:
        text string - empty string
        place_id - empty string
        user_id - empty string
    """

    text = ""
    place_id = ""
    user_id = ""
