import random
from locust import FastHttpUser, TaskSet, between
from faker import Faker
import datetime

# Initialize Faker to generate realistic user data (emails, addresses, etc.)
fake = Faker()

# A sample list of product IDs from the microservices demo app (e.g., Online Boutique)
products = [
    '0PUK6V6EV0',
    '1YMWWN1N4O',
    '2ZYFJ3GM2N',
    '66VCHSJNUP',
    '6E92ZMYYFZ',
    '9SIQT8TOJO',
    'L9ECAV7KIM',
    'LS4PSXUNUM',
    'OLJCESPC7Z'
]

# -------------------------------
#   Task definitions (user actions)
# -------------------------------

# Visit the homepage
def index(l):
    l.client.get("/")

# Change currency on the site (simulates user switching currency)
def setCurrency(l):
    currencies = ['EUR', 'USD', 'JPY', 'CAD', 'GBP', 'TRY']
    l.client.post("/setCurrency", {
        'currency_code': random.choice(currencies)
    })

# Browse a random product detail page
def browseProduct(l):
    l.client.get("/product/" + random.choice(products))

# View the shopping cart
def viewCart(l):
    l.client.get("/cart")

# Add a random product to the cart
def addToCart(l):
    product = random.choice(products)
    # Load the product page first (mimics realistic flow)
    l.client.get("/product/" + product)
    # Then add product to cart with random quantity
    l.client.post("/cart", {
        'product_id': product,
        'quantity': random.randint(1, 10)
    })

# Empty the cart completely
def empty_cart(l):
    l.client.post('/cart/empty')

# Perform checkout with randomly generated fake user data
def checkout(l):
    # Add at least one item to the cart before checkout
    addToCart(l)
    current_year = datetime.datetime.now().year + 1
    # Simulate a realistic checkout payload with credit card and address info
    l.client.post("/cart/checkout", {
        'email': fake.email(),
        'street_address': fake.street_address(),
        'zip_code': fake.zipcode(),
        'city': fake.city(),
        'state': fake.state_abbr(),
        'country': fake.country(),
        'credit_card_number': fake.credit_card_number(card_type="visa"),
        'credit_card_expiration_month': random.randint(1, 12),
        'credit_card_expiration_year': random.randint(current_year, current_year + 70),
        'credit_card_cvv': f"{random.randint(100, 999)}",
    })

# Simulate user logging out
def logout(l):
    l.client.get('/logout')


# -------------------------------
#   User Behavior Configuration
# -------------------------------

class UserBehavior(TaskSet):
    """
    Defines a sequence of user actions and their relative frequency (weights).
    Each Locust user will execute tasks from this set during the test.
    """

    def on_start(self):
        # Called when a simulated user starts — load the homepage first.
        index(self)

    # The 'tasks' dictionary maps functions to weights.
    # Higher weight = more frequent execution.
    tasks = {
        index: 1,
        setCurrency: 2,
        browseProduct: 10,
        addToCart: 2,
        viewCart: 3,
        checkout: 1
    }


# -------------------------------
#   Load Test Configuration
# -------------------------------

class WebsiteUser(FastHttpUser):
    """
    Represents a simulated user that performs actions defined in UserBehavior.
    'FastHttpUser' is used for improved performance compared to the default HttpUser.
    """

    # Assign the task set for this user type
    tasks = [UserBehavior]

    # Define random wait time between user actions (1 to 10 seconds)
    # This simulates real-world user "think time"
    wait_time = between(1, 10)
