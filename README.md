# Rental Management System

## Overview

This web application is designed to facilitate the management of rental properties. It allows users to add new customers, staff, and houses, as well as to view and edit these details. The system also provides dedicated dashboards for admin and staff members, along with authentication capabilities.

## Features

- **User Authentication**: Secure login and registration system for both customers and staff.
- **Admin Dashboard**: For overseeing the entire rental management operations.
- **Customer Dashboard**: Customers can view and manage their rental details.
- **Staff Dashboard**: Allows staff to manage assignments and interact with customers.
- **Property Management**: Add and view details of houses available for rent.
- **Account Management**: Add, view, and edit customer and staff details.

## File Structure

- `static/`: Contains CSS and image assets for the web application's front end.
- `templates/`: Holds the HTML templates for the various views in the application.
  - `add_customer.html`: Form to add new customers.
  - `add_house.html`: Form to add new rental properties.
  - `add_staff.html`: Form to add new staff members.
  - `admin_dashboard.html`: Main dashboard view for admins.
  - `customer_dashboard.html`: Main dashboard view for customers.
  - `edit_customer.html`: Form to edit customer details.
  - `edit_staff.html`: Form to edit staff details.
  - `house_details.html`: View for individual house details.
  - `login.html`: Authentication view.
  - `register.html`: Registration view.
  - `staff_dashboard.html`: Main dashboard view for staff.
- `app.py`: The main application file for the web app.
- `connect.py`: Handles the database connection logic.
- `__init__.py`: Initializes the Python package.