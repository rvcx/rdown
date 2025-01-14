"""
Import hook for rdown
"""

__version__ = "0.1.0.dev"

from rdown import ReceiptLineRenderer
import mistletoe

def markdown(iterable):
    """
    Converts markdown input to ReceiptLine format.
    """
    return mistletoe.markdown(iterable, renderer=ReceiptLineRenderer.ReceiptLineRenderer)
