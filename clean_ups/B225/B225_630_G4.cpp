#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

// Function to check card type based on prefix and length
string getCardType(const string& cardNumber) {
    int prefix = stoi(cardNumber.substr(0, 2));
    int length = cardNumber.length();

    if (prefix == 34 || prefix == 37) {
        if (length == 15) {
            return "American Express";
        }
    } else if (prefix >= 51 && prefix <= 55) {
        if (length == 16) {
            return "MasterCard";
        }
    } else if (prefix == 4) {
        if (length == 13 || length == 16) {
            return "Visa";
        }
    } else if (prefix == 60) {
        if (length >= 16 && length <= 19) {
            return "Discover";
        }
    }

    return "Unknown";
}

// Function to check if a credit card number is valid using the Luhn algorithm
bool isCreditCardValid(const string& cardNumber) {
    // Remove spaces and non-digit characters
    string cleanCardNumber = "";
    for (char c : cardNumber) {
        if (isdigit(c)) {
            cleanCardNumber += c;
        }
    }

    // Check if the cleaned card number is empty or not a valid length
    if (cleanCardNumber.empty() || cleanCardNumber.length() < 13 || cleanCardNumber.length() > 19) {
        return false;
    }

    // Reverse the card number
    reverse(cleanCardNumber.begin(), cleanCardNumber.end());

    int sum = 0;
    for (size_t i = 0; i < cleanCardNumber.length(); ++i) {
        int digit = cleanCardNumber[i] - '0';

        // Double every second digit
        if (i % 2 == 1) {
            digit *= 2;

            // If doubling results in a two-digit number, subtract 9
            if (digit > 9) {
                digit -= 9;
            }
        }

        sum += digit;
    }

    // The card is valid if the sum is a multiple of 10
    return (sum % 10 == 0);
}

// Function to process a batch of credit card numbers
void processCreditCardBatch(const vector<string>& cardNumbers) {
    for (const string& cardNumber : cardNumbers) {
        if (isCreditCardValid(cardNumber)) {
            string cardType = getCardType(cardNumber);
            cout << cardNumber << " is valid (" << cardType << ")\n";
        } else {
            cout << cardNumber << " is not valid\n";
        }
    }
}

int main() {
    vector<string> cardNumbers;
    int numCards;

    cout << "Enter the number of credit cards: ";
    cin >> numCards;

    cout << "Enter credit card numbers (one per line):\n";
    for (int i = 0; i < numCards; ++i) {
        string cardNumber;
        cin >> cardNumber;
        cardNumbers.push_back(cardNumber);
    }

    processCreditCardBatch(cardNumbers);

    return 0;   
}