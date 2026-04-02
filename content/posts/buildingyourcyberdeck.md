+++
date = '2025-10-29T10:50:49Z'
draft = false
title = 'Building your Cyberdeck'
weight = 24
+++
Building your own Cyberdeck  
  
The Cyberdeck is a new approach to using computers that can be applied to reusing by up-cycling old hardware to  
using high end hardware creating a local super computer.  
  
The difference needs to be understood to a single computer.  
  
This is a LAN. The Cyberdeck is not one single Computer, is having hands on several computers using standard  
components to increase efficiency of computer use.  
  
Working with a Cyberdeck means also understanding the capability of each computer. Simple things like moving   
the task bar in Firefox by changing the settings to the side bar increase productivity a very lot on a Raspberry  
Pi 5 with an AI Kit, if used horizontally with its 7inch touch screen, while if used for reading text files the  
little helper will stand vertically.  
  
In my personal case old hardware turns a high end system outperforming high end gaming computers being  
way more efficient in energy use, even so I cannot play one main Game on it.  
  
This Cyberdeck called design is a work station optimized for efficiency.  
  
At this moment I am researching what AI models can do realistically opposing the idea that AI exchanges   
humans as a well understood lesson from Help Desk jobs that are considered a cost factor and not a main  
USP to create long term Happy Customers.  
  
I am also under the strong impression that most AI start ups simply create pipes to the large  
Online AIs instead of breaking down AI models into local assistance systems in combinations with scripting  
languages and actual use cases.  
  
Running on several small computers dedicated AI models is a logic step from having to work with several computers  
to listen smoothly to the own music library (Navidrome on a Raspi 4 1GB RAM, headless), searching the internet smoothly  
(M920 with Linux), creating music with open source software, (was ubuntu studio on the L420) and this without performance  
laags.  
  
Building this Cyberdeck can mean to give a small Office company with several employees way stronger computational  
abilities. The Beowulf layer being deeply embedded into the Linux OS architecture supports not all software, but a lot of  
software uses libraries and OS parts that are supporting the mpich layer that is the core of the Beowulf Cluster.  
  
Rendering music projects into mp3s or video projects into mp4 is such a case of non-parallel designed software that uses  
parallelized system packages speeding up rendering times.  
  
Spreadsheet calculations might be other more standard use cases and as much as mpich is since recently installable by a   
standard command especially office systems parallelized will create tremendous productivity increases.  
  
This means that Cyberdeck design workstations are always custom projects dedicated to given hardware and need.  
  
This AI research heavy Cyberdeck needs a strong OS layer and dedicated Python Environment.   
  
Hence I had the opportunity to change to Ubuntu Server on my headnode, the M920, I used this situation to create with   
DeepSeek a set up manual for the needed Python libraries.  
  
After having installed Python 3.13 and build a Python Environment, this is the next step:  
  
```batch
Here's a comprehensive setup guide to install all the 
required libraries for your Python environment:

## 1. First, Update System Packages

sudo apt update
sudo apt upgrade -y


## 2. Install System Dependencies

# Essential build tools and libraries
sudo apt install -y python3-pip python3-venv build-essential cmake
sudo apt install -y libssl-dev libffi-dev libxml2-dev libxslt-dev
sudo apt install -y python3-dev curl wget git

# For matplotlib and visualization
sudo apt install -y libfreetype6-dev libpng-dev libjpeg-dev

# For data processing
sudo apt install -y pkg-config


## 3. Create and Activate Virtual Environment

python3 -m venv cyberdeck-env313
source cyberdeck-env313/bin/activate


## 4. Upgrade pip and setuptools

pip install --upgrade pip setuptools wheel


## 5. Install Core Python Packages
Create a `requirements.txt` file with the following content:


# Web scraping and HTTP
requests>=2.31.0
beautifulsoup4>=4.12.0
tldextract>=5.1.0

# AI/ML and embeddings
ollama>=0.1.0
langchain>=0.1.0
langchain-community>=0.0.10
chromadb>=0.4.0
sentence-transformers>=2.2.0
faiss-cpu>=1.7.0
torch>=2.0.0
transformers>=4.30.0

# Data processing and analysis
pandas>=2.0.0
numpy>=1.24.0

# Visualization
matplotlib>=3.7.0
networkx>=3.0

# YAML and configuration
PyYAML>=6.0
python-frontmatter>=1.0.0

# Cryptocurrency trading
python-binance>=1.0.19

# Progress bars
tqdm>=4.65.0

# Utilities
colorama>=0.4.0
typing-extensions>=4.5.0


Then install:

pip install -r requirements.txt


## 6. Install Additional Packages
Some packages might need separate installation:


# For FAISS with GPU support 
  (optional - remove -cpu if you have GPU)
pip install faiss-cpu

# For HuggingFace embeddings
pip install huggingface-hub

# Alternative: Install everything in one command
pip install requests beautifulsoup4 ollama tldextract langchain 
langchain-community chromadb sentence-transformers faiss-cpu 
torch transformers pandas numpy matplotlib networkx PyYAML 
python-frontmatter python-binance tqdm colorama typing-extensions 
huggingface-hub


## 7. Install Development Dependencies (Optional)

pip install jupyter ipython black flake8 mypy


## 8. Verify Installation
Create a test script `verify_imports.py`:


#!/usr/bin/env python3

import argparse
import requests
from bs4 import BeautifulSoup
import ollama
import time
import os
import textwrap
import tldextract
from collections import OrderedDict
import sys
import re
import datetime
import readline
import json
import html
import shutil
import glob
import logging
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
import yaml
import cmd
import webbrowser
import urllib.parse
import networkx as nx
import subprocess
import tempfile
import threading
import colorsys
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from collections import defaultdict, deque
from textwrap import wrap
import math
from frontmatter import Frontmatter
from binance.client import Client
from binance.exceptions import BinanceAPIException
import pandas as pd
from tqdm import tqdm
import gzip
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

print("All imports successful! Environment is properly configured.")

Run it:

python verify_imports.py


1. **If you get build errors**, make sure all system 
   dependencies are installed:

   sudo apt install -y build-essential python3-dev cmake


2. **For GPU support** with FAISS/PyTorch:
   
   pip uninstall faiss-cpu
   pip install faiss-gpu
   

3. **If Ollama connection fails**:
   
   # Check if Ollama is running
   ollama pull llama2  # Download a model to test
   

4. **For memory issues**, consider installing packages 
   individually rather than all at once.

This setup should cover all the imports in your scripts. The environment 
will be ready for your cyberdeck project!
```
