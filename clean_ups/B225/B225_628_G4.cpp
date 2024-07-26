#include <iostream>
#include <string>
#include <algorithm>

using namespace std;

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

int main() {
    string cardNumber;

    cout << "Enter credit card number: ";
    cin >> cardNumber;

    if (isCreditCardValid(cardNumber)) {
        cout << "Credit card is valid.\n";
    } else {
        cout << "Credit card is not valid.\n";
    }

    return 0;
}