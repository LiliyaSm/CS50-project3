# CS50 Project 3

### It is a web application for handling a pizza restaurant’s online orders.  Once logged in, users see a representation of the restaurant’s menu. They can add items (along with toppings or extras, if appropriate) to their shopping cart. Once there is at least one item in a shopping cart, the user can place an order.
### Site administrators have access to a page where they can view and change any orders that have already been placed. My personal touch to this application is an opportunity for the customer to view their previous orders and repeat them if necessary. Special pizza is a pizza with 4 toppings.

Project Pizza has two installed apps - users and orders. 


Project Pizza folder contains file urls.py with project-level URL configurations.


In users app directory there are files for providing users registration and login:
* view.py module - the views for users app;
* forms.py module - the forms for users app;
* folder "templates" contains registration and login HTML files.

In orders app directory there are files for providing the whole process of handling an online order: adding items in the cart, placing orders, viewing order history and so on:
* folder "templates" contains HTML files for displaying the main page and carts;
* folder "static" contains CSS, javascript and jpg files;
* admin.py - app’s models registered with the Django admin application;
* models.py - the models to work with data and database;
* view.py module - the views for orders app.

In all directories:
* apps.py - defines basic configuration settings

Technologies:
1. Python 3.7
2. Django 2.1.5
3. jQuery
4. Bootstrap 4

![database schema](https://www.planttext.com/api/plantuml/img/RLJ1RiCW3Btp5Vn0A-qwJLEbJ9igRUkcPkUA1TOo1OY073BruqSXE42u1BzdntwsINR64cr7qUCxfBv_MMVntZ9X4F87liTx2kOx4Gp0YrRZ0EX2JAk6WSkp0Uv3yuuT1Udxd7eb-inGB4UvkRJJu8XeXQ89UeAGL6AhKgKpIWGlpBDMekHQLRounT7rHkI4hV8db7JTtPhp3RYQ6Gn5LvHBLw5j6DFdIAJbTbhvawbLNVFqWjY7wmQNKGV9G7s8yc4u6MWQaixqe2dJyqI3lSnpmQ6lZCjs3spi4UUqLvfJ3Ucxqx3cZ_pFzLhH6BQsrflofVR21xUYwette-BSuYmoloxBOjp8ixZQq1ltyHcCK3YztcX-6QOJwDESAB4Cg5PPqWDgbFpXMZ0AoMyP3FBFa3gQ_ZkUKRWR8KafCf6_sLmVCMX9WtPCKlV_S5lw1m00)


Detailed requirements can be found [here](https://docs.cs50.net/web/2020/x/projects/3/project3.html)
