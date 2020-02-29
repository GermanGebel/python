#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 11:13:39 2020

@author: dodo
"""

import json
with open('planes_data.json','r') as read_file:
    planes = json.load(read_file)
    read_file.close()

