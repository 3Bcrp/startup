from skynet import app
import os

base_path = os.path.dirname(os.path.abspath(__file__))
# Folder creation
try:
    log_path = os.mkdir(os.path.join(base_path,'./skynet', './logs'))
except OSError:
    print('Path already exist')

app.run(debug=True)
