import json
import datetime
import os

# Define the filename for our data storage
DATA_FILE = 'loans.json'

def load_transactions():
    """Loads transaction data from a JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_transactions(transactions):
    """Saves transaction data to a JSON file."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(transactions, f, indent=4, ensure_ascii=False)

def add_transaction(transactions, transaction_type, friend_name, amount):
    """
    Adds a new loan or repayment transaction.
    This function is central to 'tracking' by recording each financial event.
    """
    if not isinstance(amount, (int, float)) or amount <= 0:
        print("Amount must be a positive number.")
        return

    transaction = {
        "type": transaction_type, # 'loan' or 'repayment'
        "friend": friend_name,
        "amount": amount,
        "date": datetime.date.today().isoformat()
    }
    transactions.append(transaction)
    print(f"Recorded {transaction_type} of {amount} TL with {friend_name}.")

def get_friend_balance(transactions, friend_name):
    """
    Calculates the outstanding balance for a specific friend.
    This aggregates recorded transactions to provide a current financial status.
    """
    balance = 0
    for t in transactions:
        if t["friend"] == friend_name:
            if t["type"] == "loan":
                balance += t["amount"]
            elif t["type"] == "repayment":
                balance -= t["amount"]
    return balance

def get_all_balances(transactions):
    """Calculates and returns balances for all friends."""
    balances = {}
    for t in transactions:
        friend = t["friend"]
        if friend not in balances:
            balances[friend] = 0
        if t["type"] == "loan":
            balances[friend] += t["amount"]
        elif t["type"] == "repayment":
            balances[friend] -= t["amount"]
    return balances

def display_transactions(transactions):
    """Prints all recorded transactions."""
    if not transactions:
        print("No transactions recorded yet.")
        return
    print("\n--- All Transactions ---")
    for i, t in enumerate(transactions):
        print(f"{i+1}. Date: {t['date']}, Friend: {t['friend']}, Type: {t['type'].capitalize()}, Amount: {t['amount']} TL")
    print("------------------------")

def display_balances(balances):
    """Prints the current balances for all friends."""
    if not balances:
        print("No balances to display.")
        return
    print("\n--- Current Balances ---")
    for friend, balance in balances.items():
        status = "owes you" if balance > 0 else "you owe" if balance < 0 else "settled"
        abs_balance = abs(balance)
        print(f"{friend}: {abs_balance} TL ({status})")
    print("------------------------")


def main():
    """Main function to run the loan tracker."""
    transactions = load_transactions()
    print("Welcome to the Friend Loan Tracker!")

    # --- Demonstrating the tracking functionality ---

    # 1. Add some initial loans
    print("\n--- Adding initial loans ---")
    add_transaction(transactions, "loan", "Ayşe", 100) # Recording a loan
    add_transaction(transactions, "loan", "Mehmet", 50)
    add_transaction(transactions, "loan", "Ayşe", 200)

    # 2. Display all transactions to see what's been recorded
    display_transactions(transactions)

    # 3. Record a repayment
    print("\n--- Recording a repayment ---")
    add_transaction(transactions, "repayment", "Ayşe", 150) # Recording a repayment

    # 4. Display updated transactions
    display_transactions(transactions)

    # 5. Get and display current balances
    print("\n--- Calculating and displaying balances ---")
    all_balances = get_all_balances(transactions) # Aggregating transactions to get balances
    display_balances(all_balances)

    # 6. Add another loan and check balance again
    print("\n--- Adding another loan and re-checking balances ---")
    add_transaction(transactions, "loan", "Zeynep", 75)
    add_transaction(transactions, "repayment", "Mehmet", 20)
    all_balances = get_all_balances(transactions)
    display_balances(all_balances)

    # 7. Save the current state
    save_transactions(transactions)
    print(f"\nAll transactions saved to {DATA_FILE}.")

    # --- Example of loading and continuing ---
    print("\n--- Demonstrating loading saved data (simulate new run) ---")
    new_run_transactions = load_transactions()
    print(f"Loaded {len(new_run_transactions)} transactions from {DATA_FILE}.")
    display_balances(get_all_balances(new_run_transactions))


if __name__ == "__main__":
    main()
