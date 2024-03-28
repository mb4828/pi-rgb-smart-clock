import sys
import os

# Add rgbmatrix to path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
module_path = os.path.join(parent_dir, 'rpi-rgb-led-matrix', 'bindings', 'python')
sys.path.append(module_path)
