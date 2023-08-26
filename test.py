from pathlib import Path

import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


img = Image.open(Path('assets') / 'deck' / 'clubs_jack.jpg').resize((62, 100), Image.ANTIALIAS)
st.image(img)

# In the second column, display some text
st.write("Your text content here.")