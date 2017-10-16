#!/usr/bin/env python
# -*- coding: utf-8 -*-



class HearsayError(Exception):
    pass

class WeBeMessin(HearsayError):
    """We messed up."""
    pass
class YouBeMessin(HearsayError):
    """You messed up."""
    pass
