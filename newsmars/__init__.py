"""
NewSMARS - Enhanced SMARS robot implementation
"""

from .smars import SMARS
from .rangefinder import HCSR04

__version__ = '1.0.0'
__all__ = ['SMARS', 'HCSR04']
