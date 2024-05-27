# Grocery-Store-App

Author
PREM KUMAR
21f1000531
21f1000531@ds.study.iitm.ac.in

# Description
      The project involves creating a web application for managing products, sections, user roles, and purchases. Users can register, log in, and browse available products, add them to their cart, and make purchases. The system also has an admin panel for managing products, sections, and user roles.
      
# Technologies used

Flask: A micro web framework in Python, chosen for its simplicity and extensibility.
Jinja2: A templating engine used to generate dynamic HTML content.
SQLAlchemy: An Object-Relational Mapping (ORM) library for database management.
SQLite: A lightweight relational database management system.
Bootstrap: A frontend framework for responsive and appealing user interface design.

# DB Schema Design

User: id, username, password, role
Section: id, name, type, image
Product: id, name, manufacture_date, expiry_date, rate_per_unit, section_id (foreign key)
Purchase: id, user_id (foreign key), product_id (foreign key), quantity, purchase_date

The User and Purchase tables are linked using foreign key relationships. The Purchase table also includes the quantity and purchase date.

# Architecture and Features
      The project follows an MVC (Model-View-Controller) architecture. Controllers manage the routes and business logic, templates (HTML with Jinja2) handle the presentation layer, and the models represent the database tables. Features include user registration, login/logout, role-based access control, browsing products with sections, adding products to the cart, and viewing the cart contents. Default features include admin panel functionalities for managing sections and products. Additional features could involve order history, user profile management, and enhanced admin controls.
