import os
import re
from typing import Dict, List, Literal, Optional, TypeVar, Union

from pydantic import BaseModel, Field, ValidationError
from yaml import safe_load


class HexColor(str):
    PATTERN = r"^#([A-Fa-f0-9]{6})$"
    regex = re.compile(PATTERN)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(pattern=PATTERN,)

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("string required")
        m = cls.regex.fullmatch(v.upper())
        if not m:
            raise ValueError("invalid color hex format")
        return cls(f"#{m.group(1)}")

    def __repr__(self):
        return f"HexColor({super().__repr__()})"


class Action(BaseModel):
    type: str
    kwargs: Optional[Dict[str, str]] = Field({})


class Button(BaseModel):
    icon: str
    text: str
    action: Action


class NotImplementedLayout(BaseModel):
    type: Literal["not_implemented"]


class MovementLayout(BaseModel):
    type: Literal["movement"]


class GridLayout(BaseModel):
    type: Literal["grid"]
    buttons: List[Button]
    columns: int
    rows: int


class Frame(BaseModel):
    layout: Union[NotImplementedLayout, MovementLayout, GridLayout]


class Screen(BaseModel):
    width: int = 480
    height: int = 320


class Colors(BaseModel):
    icon: HexColor
    background: HexColor
    background_acent: HexColor
    primary_font: HexColor
    button_background: HexColor
    button_background_secondary: HexColor
    button_background_tertiary: HexColor
    icon_fill: HexColor


class Config(BaseModel):
    """
    Representation of the YAML configuration. Can load more than one.
    """

    name: str
    colors: Colors
    frames: Dict[str, Frame]
    screen: Screen = Screen()
    status_poll_interval_ms: int = Field(1000)

    @classmethod
    def load(cls, path):
        with open(os.path.join(path, "config.yml"), "r") as file:
            data = safe_load(file)
        self = cls.parse_obj(data)
        object.__setattr__(self, "path", path)
        return self
