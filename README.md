# Django Shop-Project

An e-commerce project with functionalities such as user authentication, product commenting, adding products to favorites, adding products to the cart, order processing, and product filtering.

### Installation and Running on Local Machine

These instructions will help you run the project on your local machine for development and testing purposes.

### Prerequisites

Ensure you have the following software installed:

- **Python 3.x**
- **pip** (Python package manager).
- **virtualenv** (optional, for creating an isolated environment).
- **PostgreSQL** (adjust `settings.py` if using a different database).

___
## Installation

1. Create Django `SECRET_KEY`:
2. Clone the repository:
    ```sh
    git clone https://github.com/podrivnick/elec-shop.git
    cd elec_docker
    ```
3. Create the 'media' directory with subdirectories 'avatars' and 'products':
    ```sh
    mkdir -p media/avatars media/products
    ```
4. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
5. Set up environment variables:
    - Create a `.env` file and fill it according to `.env.example`.

6. Apply migrations and run the Django server:
    ```sh
    python manage.py migrate
    python manage.py runserver
    ```

### Using PostgreSQL

The project is designed for **PostgreSQL**, which is especially important for the vector search system.

___
## Structure

```plaintext
    elec_docker/
    │
    ├── app/
    │   ├── carts_products/
    │   │   ├── migrations/
    │   │   ├── templates/
    │   │   │   └── carts_products/
    │   │   │       ├── all_opinions.html
    │   │   │       ├── cart_product.html
    │   │   │       └── finalize_product.html
    │   │   ├── __init__.py
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── forms.py
    │   │   ├── models.py
    │   │   ├── tests.py
    │   │   ├── urls.py
    │   │   ├── views.py
    │   │   ├── config.py
    │   │   ├── exceptions.py
    │   │   ├── services.py
    │   │   └── utils.py
    │   ├── main_favorite/
    │   │   ├── migrations/
    │   │   ├── templates/
    │   │   │   └── main_favorite/
    │   │   │       ├── favorites.html
    │   │   │       ├── index.html
    │   │   │       ├── information.html
    │   │   │       └── mechanizm/
    │   │   │           └── pagination.html
    │   │   ├── __init__.py
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── forms.py
    │   │   ├── models.py
    │   │   ├── tests.py
    │   │   ├── urls.py
    │   │   ├── utils.py
    │   │   ├── views.py
    │   │   └── services.py
    │   ├── users/
    │   │   ├── migrations/
    │   │   ├── templates/
    │   │   │   └── users/
    │   │   │       ├── login.html
    │   │   │       ├── profile.html
    │   │   │       ├── registration.html
    │   │   │       └── packet_profile/
    │   │   │           ├── orders_profile.html
    │   │   │           └── packet_profile.html
    │   │   ├── __init__.py
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── forms.py
    │   │   ├── models.py
    │   │   ├── tests.py
    │   │   ├── urls.py
    │   │   ├── views.py
    │   │   ├── config.py
    │   │   ├── services.py
    │   │   └── templatetags/
    │   │       ├── __init__.py
    │   │       └── get_orders.py
    │   ├── static/
    │   │   ├── css/
    │   │   │   └── main.css
    │   │   ├── js/
    │   │   │   ├── add_to_favorites.js
    │   │   │   ├── cart_management.js
    │   │   │   └── validation/
    │   │   │       ├── login.js
    │   │   │       └── registration.js
    │   ├── templates/
    │   │   ├── base.html
    │   │   └── modal_packet.html
    │   ├── __init__.py
    │   ├── manage.py
    │   ├── requirements.txt
    │   └── settings.py
    │
    └── .git/
```

## Technology
+ **Django**
+ **Python**
+ **HTML/CSS/JS/JQuery**


___
## Design Patterns
+ **Singleton**: Used for classes that should have only one instance, e.g., configuration classes.
+ **Factory Method**: Used for creating objects based on input data. Example: creating different forms depending on the user type.
+ **Repository**: Used for abstracting the data access layer, providing methods for interacting with the database.
+ **Service**: Business logic is moved to separate service classes, making it easier to test and reuse.
+ **MVT** (Model-View-Template): 
  + ***Model***: Represents the data and business logic of the project.
  + ***View***: Handles the requests and sends the response to the user.
  + ***Template***: Defines what data is sent to the user.

## Author
Author of the project: ***Rybakov Artem***

