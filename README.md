# Little Lemon Backend

> Little Lemon Backend is a robust Django backend designed to power the Little Lemon app, the API offers endpoints for managing customers, menu items, categories, orders, delivery crew users and user groups.

## Project Requirements

- Users should be able to register, login and logout
- Customers should be able to browse menu items and categories, add items to cart, clear their cart, make orders
- Managers should be able to fully manage categories and menu items, they can also update orders, assign delivery crew orders and assign customers a group
- Delivery crew users should be able to update their assigned orders

## Installation

1. Clone the repository

```bash
git clone git@github.com:mehdiaitouchrif/little-lemon-backend.git
```

2. Create a virtual environment and activate it

```python
python3 -m venv env
source env/bin/activate
```

3. Install the dependencies
   pip install -r requirements.txt

4. Run the server

```bash
   python manage.py runserver
```

## Endpoints

### User Authentication Endpoints

| Endpoint               | Role                                | Method | Purpose                                                                     |
| ---------------------- | ----------------------------------- | ------ | --------------------------------------------------------------------------- |
| /api/auth/users/       | No role required                    | POST   | Registers a new user and returns 201 - Created HTTP status code             |
| /api/auth/users/me/    | Anyone with a valid user token      | POST   | Displays only the current user                                              |
| /api/auth/token/login/ | Anyone with valid login credentials | POST   | Generates access tokens that can be used in other API calls in this project |

### Menu-items endpoints

| Endpoint                   | Role                    | Method                   | Purpose                                                       |
| -------------------------- | ----------------------- | ------------------------ | ------------------------------------------------------------- |
| `/api/menu-items`          | Customer, delivery crew | GET                      | Lists all menu items. Return a 200 – Ok HTTP status code      |
| `/api/menu-items`          | Customer, delivery crew | POST, PUT, PATCH, DELETE | Denies access and returns 403 – Unauthorized HTTP status code |
| `/api/menu-items/{itemId}` | Customer, delivery crew | GET                      | Lists single menu item                                        |
| `/api/menu-items/{itemId}` | Customer, delivery crew | POST, PUT, PATCH, DELETE | Returns 403 - Unauthorized                                    |
| `/api/menu-items`          | Manager                 | GET                      | Lists all menu items                                          |
| `/api/menu-items`          | Manager                 | POST                     | Creates a new menu item and returns 201 - Created             |
| `/api/menu-items/{itemId}` | Manager                 | GET                      | Lists single menu item                                        |
| `/api/menu-items/{itemId}` | Manager                 | PUT, PATCH               | Updates single menu item                                      |
| `/api/menu-items/{itemId}` | Manager                 | DELETE                   | Deletes menu item                                             |

## Category endpoints

| Endpoint                     | HTTP Method | Role    | Description                            |
| ---------------------------- | ----------- | ------- | -------------------------------------- |
| /api/categories              | GET         | All     | Returns a list of all categories       |
| /api/categories              | POST        | Manager | Creates a new category                 |
| /api/categories/{categoryId} | GET         | All     | Returns details of a specific category |
| /api/categories/{categoryId} | PUT         | Manager | Updates a specific category            |
| /api/categories/{categoryId} | DELETE      | Manager | Deletes a specific category            |

### User group management endpoints

| Endpoint                                   | Role    | Method | Purpose                                                                                                                                                |
| ------------------------------------------ | ------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `/api/groups/manager/users`                | Manager | GET    | Returns all managers                                                                                                                                   |
| `/api/groups/manager/users`                | Manager | POST   | Assigns the user in the payload to the manager group and returns 201-Created                                                                           |
| `/api/groups/manager/users/{userId}`       | Manager | DELETE | Removes this particular user from the manager group and returns 200 – Success if everything is okay. If the user is not found, returns 404 – Not found |
| `/api/groups/delivery-crew/users`          | Manager | GET    | Returns all delivery crew                                                                                                                              |
| `/api/groups/delivery-crew/users`          | Manager | POST   | Assigns the user in the payload to delivery crew group and returns 201-Created HTTP                                                                    |
| `/api/groups/delivery-crew/users/{userId}` | Manager | DELETE | Removes this user from the manager group and returns 200 – Success if everything is okay. If the user is not found, returns 404 – Not found            |

### Cart management endpoints

| Endpoint               | Role     | Method | Purpose                                                                                         |
| ---------------------- | -------- | ------ | ----------------------------------------------------------------------------------------------- |
| `/api/cart/menu-items` | Customer | GET    | Returns current items in the cart for the current user token                                    |
| `/api/cart/menu-items` | Customer | POST   | Adds the menu item to the cart. Sets the authenticated user as the user id for these cart items |
| `/api/cart/menu-items` | Customer | DELETE | Deletes all menu items created by the current user token                                        |

### Order Management

| Endpoint                | Role          | Method     | Purpose                                                                                                                                                                                           |
| ----------------------- | ------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/api/orders`           | Customer      | GET        | Returns all orders with order items created by this user                                                                                                                                          |
| `/api/orders`           | Customer      | POST       | Creates a new order item for the current user. Gets current cart items from the cart endpoints and adds those items to the order items table. Then deletes all items from the cart for this user. |
| `/api/orders/{orderId}` | Customer      | GET        | Returns all items for this order id. If the order ID doesn’t belong to the current user, it displays an appropriate HTTP error status code.                                                       |
| `/api/orders`           | Manager       | GET        | Returns all orders with order items by all users                                                                                                                                                  |
| `/api/orders/{orderId}` | Manager       | PUT, PATCH | Updates the order. A manager can use this endpoint to set a delivery crew to this order, and also update the order status                                                                         |
| `/api/orders/{orderId}` | Manager       | DELETE     | Deletes this order                                                                                                                                                                                |
| `/api/orders`           | Delivery crew | GET        | Returns all orders with order items assigned to the delivery crew                                                                                                                                 |
| `/api/orders/{orderId}` | Delivery crew | PATCH      | Updates the order status to 0 or 1                                                                                                                                                                |

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Author

Created by [Mehdi Ait Ouchrif](https://github.com/mehdiaitouchrif).
