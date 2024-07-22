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
    dish_lower = dish_name.lower()  # Convert input to lowercase for comparison
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

# Get dish name from user
dish_to_retrieve = input("Enter the name of the dish: ")
retrieve_recipe(dish_to_retrieve)

while True:
    choice = input(
        "Do you want to (1) add a recipe, (2) retrieve a recipe, or (3) exit? ")
    if choice == "1":
        add_recipe()
    elif choice == "2":
        dish_to_retrieve = input("Enter the name of the dish: ")
        retrieve_recipe(dish_to_retrieve)
    elif choice == "3":
        break
    else:
        print("Invalid choice.")
