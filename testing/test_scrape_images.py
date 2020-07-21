"""
test file for fridge detection file
"""
import pytest
from scrape_images import scrape_from_imagenet

def test_scrape_from_imagenet():
    scrape_from_imagenet("Aubergine", 2, "http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07713074")
    assert True
