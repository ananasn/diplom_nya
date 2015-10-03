# -*- coding: utf-8 -*-
def rs_hash(str):
    """ Robert Sedgewick's string hashing algorithm"""
    a = 63689
    b = 378551
    hash = 0
    for key in str:
        hash = hash*a + ord(key)
        a = a * b
    return hash