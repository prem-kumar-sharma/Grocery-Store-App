# Grocery-Store-App

## Description
This project is a web application designed for managing products, sections, user roles, and purchases in a grocery store. Users can:

- Register and log in
- Browse available products
- Add products to their cart
- Make purchases

The system also includes an admin panel for managing products, sections, and user roles.

## Technologies Used

- **Flask**: A simple and extensible micro web framework in Python.
- **Jinja2**: A templating engine for generating dynamic HTML content.
- **SQLAlchemy**: An ORM library for database management.
- **SQLite**: A lightweight relational database management system.
- **Bootstrap**: A frontend framework for creating a responsive and appealing user interface.

## Database Schema Design

**User Table**:
- id
- username
- password
- role

**Section Table**:
- id
- name
- type
- image

**Product Table**:
- id
- name
- manufacture_date
- expiry_date
- rate_per_unit
- section_id (foreign key)

**Purchase Table**:
- id
- user_id (foreign key)
- product_id (foreign key)
- quantity
- purchase_date

The User and Purchase tables are connected using foreign key relationships. The Purchase table also includes the quantity and purchase date.

## Architecture and Features
The project uses the MVC (Model-View-Controller) architecture:

- **Controllers**: Manage the routes and business logic.
- **Templates**: HTML files with Jinja2 for the presentation layer.
- **Models**: Represent the database tables.

### Key Features
- User registration and login/logout
- Role-based access control
- Browsing products by sections
- Adding products to the cart and viewing cart contents
- Admin panel for managing sections and products

### Additional Features (Potential Enhancements)
- Order history
- User profile management
- Enhanced admin controls

---

This README file provides an overview of the Grocery-Store-App, its technologies, database schema, and main features. It is designed to help users and collaborators understand the project's structure and functionality.
