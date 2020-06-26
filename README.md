# CS50 Project 3

### It is a web application for handling a pizza restaurant’s online orders.  Once logged in, users see a representation of the restaurant’s menu. They can add items (along with toppings or extras, if appropriate) to their shopping cart. Once there is at least one item in a shopping cart, the user can place an order.
### Site administrators have access to a page where they can view and change any orders that have already been placed. My personal touch to this application is an opportunity for the customer to view their previous orders and repeat them if necessary.

Project Pizza has two installed apps - users and orders. 
Project Pizza folder contains file urls.py with project-level URL configurations.
In users app directory there are files for providing users registration and login:
* view.py module - the views for users app;
* forms.py module - the forms for users app;
* folder "templates" contains registration and login HTML files.

In orders app directory there are files for providing the whole process of handling an online order: adding items in the cart, placing orders, viewing order history and so on.
* folder "templates" contains HTML files for displaying the main page and carts;
* folder "static" contains CSS, javascript and jpg files;
* admin.py - app’s models registered with the Django admin application;
* models.py - the models to work with data and database;
* view.py module - the views for orders app.

Detailed requirements can be found [here](https://docs.cs50.net/web/2020/x/projects/3/project3.html)