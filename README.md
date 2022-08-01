# Checking Ledger
This application allows one to track transactions via a Tkinter application.
It creates a local CSV file called ledger.csv, set to append instead of write
for users who have previously logged transactions.
The application contains three buttons:
  Button 1 modifies a remote CSV file to add transactions.
  Button 2 does the same to remove transactions.
  Button 3 loads the CSV as a dataframe to allow the user to view the transactions.
The first and second buttons' respective functions each feature error detection
to catch some potential typos, e.g. regular expressions to detect non-numerical characters.
