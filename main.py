##########################
# Author: Adam Barnard   #
# Creation Date: 5/27/22 #
##########################
from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")