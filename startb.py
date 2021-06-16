from webapp import app
import sys
sys.path.insert(0, './subdirectory')

app.run(host='0.0.0.0', debug=True)