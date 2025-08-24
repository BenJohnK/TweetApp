# TweetApp
A social media tweet application  
Please follow these steps to setup the project.  
1)inside the root directory of the project folder run the command python3 -m venv myenv  
2)Activate the virtual environment by running source myenv/bin/activate  
3)install the required libraries by running pip install -r requirements.txt  
4)Create a new postgres db in the system and mention the credentials in the django project settings file.  
5)run python manage.py migrate to apply all the db changes.  
6)run python manage.py createsuperuser to create a new admin user (optional)  
7)Create a .env file in the root directory and insert the required variables  
8) Run python manage.py runserver to start the server.  
---------------------------------------------------------------------------------------------------------------

env file sample   

DATABASE_PASS='password'  
SECRET_KEY='django-insecure-9+ddr(rr0^ln^@$83(0qv=3d#j(ahonvqy$a8_-zqt)k^4*l8i'  
