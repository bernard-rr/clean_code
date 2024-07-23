import json
import os
from datetime import datetime
from collections import defaultdict
from pygments import highlight
from pygments.lexers import get_lexer_by_name
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

        # Ensure all snippets have the necessary fields
        for snippet in self.data.values():
            if 'favorite' not in snippet:
                snippet['favorite'] = False
            if 'created_at' not in snippet:
                snippet['created_at'] = datetime.now().strftime("%Y-%m-%d")
            if 'language' not in snippet:
                snippet['language'] = "unknown"

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
            "favorite": False,  # Add favorite field, initially False
            "created_at": datetime.now().strftime("%Y-%m-%d")
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
        result_count = 0
        print("Search results:")
        for title, snippet in self.data.items():
            if (
                query.lower() in title.lower()
                or query.lower() in snippet["code"].lower()
            ):
                result_count += 1
                print(f"Snippet {result_count}:")
                print(
                    f"- **{title}** ({snippet.get('category', 'Uncategorized')})\n{snippet['code']}\n"
                )
        if result_count == 0:
            print("No snippets found matching your query.")
        else:
            print(f"Found {result_count} results")

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

    def get_contributions(self, year=None, month=None):
        """Calculates code contributions by month (optional year/month).

        Args:
            year: Year to filter (optional).
            month: Month to filter (optional).

        Returns:
            dict: Contributions grouped by month (YYYY-MM format).
        """
        contributions = defaultdict(
            lambda: {"snippets": 0, "lines": 0, "languages": set()})
        for title, snippet in self.data.items():
            created_at = datetime.strptime(snippet["created_at"], "%Y-%m-%d")
            if (year is None or created_at.year == year) and (month is None or created_at.month == month):
                month_key = f"{created_at.year}-{created_at.month:02}"
                contributions[month_key]["snippets"] += 1
                contributions[month_key]["lines"] += snippet["code"].count(
                    "\n")
                contributions[month_key]["languages"].add(snippet["language"])

        return contributions

    def show_contributions(self, year=None, month=None):
        """
        Prints code contributions for a specified period (optional).

        Args:
            year: Year to filter (optional).
            month: Month to filter (optional).
        """
        contributions = self.get_contributions(year, month)
        if contributions:
            for month_key, stats in contributions.items():
                print(f"\nContributions for {month_key}:")
                print(f"- Snippets: {stats['snippets']}")
                print(f"- Lines of code: {stats['lines']}")
                print(f"- Languages used: {', '.join(stats['languages'])}")
        else:
            print("No contributions found for the specified period.")

    def delete_snippet(self, title):
        """
        Delete a snippet by title.

        Args:
            title (str): The title of the snippet to delete.
        """
        if title in self.data:
            del self.data[title]
            self.save_data()
            print(f"Snippet '{title}' deleted successfully.")
        else:
            print("Snippet not found.")


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
        print("8. Show contributions")  # Add new choice for contributions
        print("9. Delete snippet")  # Add new choice for deleting snippets

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
        elif choice == "8":  # Add new choice for contributions
            year_input = input("Enter year (optional, press Enter to skip): ")
            year = int(year_input) if year_input else None
            month_input = input("Enter month (1-12, optional): ")
            month = int(month_input) if month_input else None
            manager.show_contributions(year, month)
        elif choice == "9":  # Add new choice for deleting snippets
            title = input("Title of snippet to delete: ")
            manager.delete_snippet(title)
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
