import subprocess
from app.app import app

if __name__ == '__main__':
    
    subprocess.Popen(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "http://127.0.0.1:5000/"])

    app.run(debug=True)