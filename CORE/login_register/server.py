from app import app

from app.controllers.auth import *



if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)