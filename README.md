# Store Payment Django 

1. clone repository or download zip.

2. create an environment and install requirements.txt (optional).

3. create .env file in parent folder and add

  SECRET_KEY={}

  Default currency

  STRIPE_PUBLIC_KEY_USD={}
  STRIPE_SECRET_KEY_USD={}

  Secondary currency

  STRIPE_PUBLIC_KEY_POUND={}
  STRIPE_SECRET_KEY_POUND={}

  

4. Run docker-compose build to build image Run docker-compose up to start container

# Usage

1. / -products or items page
2. /item/id -product detail or item page
3. /buy/id -buy product
4. /checkout/id -buy product(s)
5. /order_item/id -add item to order
6. /order_item/add/id -increase quantity
7. /order_item/remove/id -decrease quantity


# Database

Using default sqlite database for developement and postgresql in deployment, test products already added

# Admin

Username: shopadmin
Email: shopadmin@gmail.com
Password: 0

# Payment

Supports stripe session and payment intent, two hard coded buttons to execute each method of payment in cart checkout

# Live url

https://testshoppayment.onrender.com/
