# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 21:47:15 2021

@author: Xu
"""
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(os.path.split(rootPath)[0])