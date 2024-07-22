import json
import os
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter


class SnippetManager:
    """
    A class to manage code snippets.

    Attributes:
        data_file (str): The file where snippets are stored.
        data (dict): A dictionary to hold the snippet data.
    """

    def __init__(self, data_file="snippets.json"):
        """
        Initialize SnippetManager with an optional data file.

        Args:
            data_file (str): The file where snippets are stored.
        """
        self.data_file = data_file
        self.load_data()

    def load_data(self):
        """
        Load snippet data from the data file.
        If the file does not exist, initialize an empty dictionary.
        """
        try:
            with open(self.data_file, "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {}

        # Ensure all snippets have a 'favorite' field
        for snippet in self.data.values():
            if 'favorite' not in snippet:
                snippet['favorite'] = False

    def save_data(self):
        """
        Save the current snippet data to the data file.
        """
        with open(self.data_file, "w") as f:
            json.dump(self.data, f, indent=4)

    def add_snippet(self, title, code, category, language):
        """
        Add a new snippet to the collection.

        Args:
            title (str): The title of the snippet.
            code (str): The code snippet.
            category (str): The category of the snippet.
            language (str): The programming language of the snippet.
        """
        if title not in self.data:
            self.data[title] = {"code": code, "category": category}
            self.save_data()
            print("Snippet added successfully!")
        else:
            print("Snippet with this title already exists.")

        highlighted_code = highlight(
            code.replace("```", ""),
            get_lexer_by_name(language),
            TerminalFormatter(),
        )
        self.data[title] = {
            "code": highlighted_code,
            "category": category,
            "language": language,
            "favorite": False  # Add favorite field, initially False
        }

    def categorize_snippet(self, title, category):
        """
        Update the category of an existing snippet.

        Args:
            title (str): The title of the snippet.
            category (str): The new category for the snippet.
        """
        if title in self.data:
            self.data[title]["category"] = category
            self.save_data()
            print("Snippet category updated!")
        else:
            print("Snippet not found.")

    def search_snippets(self, query):
        """
        Search for snippets that match a query.

        Args:
            query (str): The search query.
        """
        resultCount = 0
        print("Search results:")
        for title, snippet in self.data.items():
            if (
                query.lower() in title.lower()
                or query.lower() in snippet["code"].lower()
            ):
                resultCount += 1
                print(f"Snippet {resultCount}:")
                print(
                    f"- **{title}** ({snippet.get('category', 'Uncategorized')})\n{snippet['code']}\n"
                )
        if resultCount == 0:
            print("No snippets found matching your query.")
        else:
            print(f"Found {resultCount} Results")

    def show_all_snippets(self):
        """
        Display all saved snippets.
        """
        if self.data:
            for title, snippet in self.data.items():
                print(
                    f"- **{title}** ({snippet.get('category', 'Uncategorized')})\n{snippet['code']}\n"
                )
        else:
            print("No snippets saved yet.")

    def toggle_favorite(self, title):
        """
        Toggle the favorite status of a snippet.

        Args:
            title (str): The title of the snippet.
        """
        if title in self.data:
            self.data[title]["favorite"] = not self.data[title]["favorite"]
            self.save_data()
            print(
                f"Snippet '{title}' marked as favorite"
                if self.data[title]["favorite"]
                else f"Snippet '{title}' removed from favorites"
            )
        else:
            print("Snippet not found.")

    def show_favorites(self):
        """
        Display all favorite snippets.
        """
        favorite_count = 0
        for title, snippet in self.data.items():
            if snippet["favorite"]:
                favorite_count += 1
                print(
                    f"- **{title}** ({snippet.get('category', 'Uncategorized')})\n{snippet['code']}\n"
                )
        if favorite_count == 0:
            print("No favorite snippets found.")


def main():
    """
    The main function to run the SnippetManager.
    Provides a menu to interact with the snippet manager.
    """
    manager = SnippetManager()

    while True:
        print("\nChoose an action:")
        print("1. Add snippet")
        print("2. Categorize snippet")
        print("3. Search snippets")
        print("4. Show all snippets")
        print("5. Exit")
        print("6. Toggle favorite")
        print("7. Show favorite snippets")

        choice = input("> ")

        if choice == "1":
            title = input("Title: ")

            print("Enter your code snippet. End with triple backticks (```)")
            code_lines = ["```"]
            while True:
                line = input()
                if line.strip() == "```":
                    break
                code_lines.append(line)

            code = "\n".join(code_lines)

            language = input("Language: ")
            category = input("Category (optional): ")
            manager.add_snippet(title, code, category, language)
        elif choice == "2":
            title = input("Title of snippet to categorize: ")
            category = input("New category: ")
            manager.categorize_snippet(title, category)
        elif choice == "3":
            query = input("Search query: ")
            manager.search_snippets(query)
        elif choice == "4":
            manager.show_all_snippets()
        elif choice == "5":
            break
        elif choice == "6":
            title = input("Title of snippet to toggle favorite: ")
            manager.toggle_favorite(title)
        elif choice == "7":
            manager.show_favorites()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
