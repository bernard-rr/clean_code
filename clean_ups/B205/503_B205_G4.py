import requests
from bs4 import BeautifulSoup


def store_recipe(dish_name, ingredients, instructions):
    """
    Stores a recipe in a dictionary format.

    Args:
        dish_name (str): The name of the dish.
        ingredients (list): A list of ingredients required for the dish.
        instructions (str): The cooking instructions for the dish.

    Returns:
        None
    """
    recipes[dish_name.lower()] = {
        "ingredients": ingredients,
        "instructions": instructions
    }


def retrieve_recipe(dish_name):
    """
    Retrieves the ingredients and instructions for a given dish.

    Args:
        dish_name (str): The name of the dish to retrieve.

    Returns:
        None
    """
    dish_lower = dish_name.lower()
    found = False
    for name, recipe in recipes.items():
        if name.lower() == dish_lower:
            found = True
            print(f"Ingredients for {name}:")
            for ingredient in recipe["ingredients"]:
                print(ingredient)

            print(f"\nInstructions for {name}:")
            print(recipe["instructions"])
            break

    if not found:
        print(f"Recipe for {dish_name} not found.")


def add_recipe():
    """
    Prompts the user to enter details for a new recipe and stores it.

    Args:
        None

    Returns:
        None
    """
    dish_name = input("Enter the dish name: ")
    ingredients = []
    while True:
        ingredient = input("Enter an ingredient (or type 'done' to finish): ")
        if ingredient.lower() == "done":
            break
        ingredients.append(ingredient)
    instructions = input("Enter the instructions: ")
    store_recipe(dish_name, ingredients, instructions)
    print(f"Recipe for {dish_name} added successfully!")


def rate_recipe(dish_name):
    """
    Allows the user to rate a dish.

    Args:
        dish_name (str): The name of the dish to rate.

    Returns:
        None
    """
    dish_lower = dish_name.lower()
    if dish_lower in recipes:
        while True:
            try:
                rating = int(
                    input(f"Enter your rating for {dish_name} (1-5 stars): "))
                if 1 <= rating <= 5:
                    if "ratings" not in recipes[dish_lower]:
                        recipes[dish_lower]["ratings"] = []
                    recipes[dish_lower]["ratings"].append(rating)
                    print("Rating added successfully!")
                    break
                else:
                    print("Invalid rating. Please enter a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 5.")
    else:
        print(f"Recipe for {dish_name} not found.")


def scrape_and_add_recipe(url):
    """
    Scrapes a recipe from the given URL and adds it to the database.

    Args:
        url (str): The URL of the recipe to scrape.

    Returns:
        None
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        dish_name = soup.find('h1', class_='recipe-title').text.strip()
        ingredients = [li.text.strip()
                       for li in soup.find_all('li', class_='ingredient')]
        instructions = soup.find('div', class_='instructions').text.strip()

        store_recipe(dish_name, ingredients, instructions)
        print(f"Recipe for {dish_name} added from {url}")

    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")


# Initialize an empty dictionary to store recipes
recipes = {}

# Example recipe storage
store_recipe(
    "Pasta Carbonara",
    ["200g spaghetti", "100g pancetta", "2 large eggs",
        "50g pecorino cheese", "50g parmesan", "Black pepper", "Salt"],
    "1. Cook the spaghetti. 2. Fry the pancetta. 3. Beat the eggs and mix with cheese. 4. Combine spaghetti with pancetta and egg mixture. 5. Serve with extra cheese and pepper."
)

store_recipe(
    "Pancakes",
    ["150g flour", "2 eggs", "300ml milk", "1 tbsp sugar",
        "Pinch of salt", "Butter for frying"],
    "1. Mix flour, sugar, and salt. 2. Add eggs and milk. 3. Whisk until smooth. 4. Fry in butter until golden."
)

# Main loop
while True:
    choice = input(
        "Do you want to (1) add a recipe, (2) retrieve a recipe, (3) rate a recipe, (4) Scrape and add a recipe or (5) exit? ")

    if choice == "1":
        add_recipe()
    elif choice == "2":
        dish_to_retrieve = input("Enter the name of the dish: ")
        retrieve_recipe(dish_to_retrieve)
    elif choice == "3":
        dish_to_rate = input("Enter the name of the dish to rate: ")
        rate_recipe(dish_to_rate)
    elif choice == "4":
        url_to_scrape = input("Enter the URL of the recipe to scrape: ")
        scrape_and_add_recipe(url_to_scrape)
    elif choice == "5":
        break
    else:
        print("Invalid choice. Please try again.")
