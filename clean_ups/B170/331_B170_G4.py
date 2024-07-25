import json
import os
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer_for_filename
from pygments.formatters import TerminalFormatter

# Install required libraries if not present:
# pip install autopep8 jsbeautifier


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

    def format_code(self, code, language):
        """
        Format code based on the language.

        Args:
            code (str): The code snippet.
            language (str): The programming language of the snippet.

        Returns:
            str: The formatted code.
        """
        if language == "python" or language == "cpp":
            import autopep8
            code = autopep8.fix_code(code)
        elif language == "js" or language == "javascript":
            import jsbeautifier
            code = jsbeautifier.beautify(code)

        return code

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

        code = self.format_code(code, language)

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

    def search_snippets(self):
        """
        Search for snippets that match a query.
        """
        query = input("Search query: ").lower()
        results = [snippet for title, snippet in self.data.items(
        ) if query in title.lower() or query in snippet["code"].lower()]

        if results:
            for i, result in enumerate(results):
                is_favorite = result.get("favorite", False)
                print(f"[{i + 1}] {result.get('title', 'Untitled')} ({result.get('category', 'Uncategorized')}, {result.get('language', 'Unknown')}) {'(Favorite)' if is_favorite else ''}")

            while True:
                try:
                    choice = int(
                        input("Enter number to view/manage snippet (or 0 to exit): "))
                    if 0 <= choice <= len(results):
                        break
                    else:
                        print("Invalid choice.")
                except ValueError:
                    print("Invalid input.")

            if choice != 0:
                selected = results[choice - 1]
                while True:
                    action = input(
                        "Enter 'f' to toggle favorite, 'v' to view code, or 'b' to go back: ").lower()
                    if action == "f":
                        selected["favorite"] = not selected.get(
                            "favorite", False)
                        self.save_data()
                        print("Favorite status toggled.")
                        break
                    elif action == "v":
                        print(f"Code:\n{selected['code']}")
                        break
                    elif action == "b":
                        break
                    else:
                        print("Invalid action.")
        else:
            print("No matching snippets found.")

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
            manager.search_snippets()
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
