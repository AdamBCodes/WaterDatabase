##########################
# Author: Adam Barnard   #
# Creation Date: 5/27/22 #
##########################
from website import create_app, create_admin

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
    #Creates Admin if it hasnt been already
    create_admin()