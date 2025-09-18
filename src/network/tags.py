# this file is meant for tags
from enum import Enum


class WPILibVersion:
  class Status(Enum):
    BAD = "<bad>"
    GOOD = "<good>"
    PREFERRED = "<preferred>"

  def __init__(self):
    self.status:str = None
    self.version:str = None
  ...

class Tags(Enum):
  WPILIB_VERSION = WPILibVersion
  ...
  
"""
In ds_net.py call from the Tags enum like this:

tag = Tags.WPILIB_VERSION()
tag.status = WPILibVersion.Status.GOOD
...
"""
