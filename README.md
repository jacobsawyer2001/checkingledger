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

This project required six days of work, from July 30 to August 4, both dates inclusive.
My main challenges included learning how to manage data and dataframes using Pandas,
thinking through how to arrange my save() function to catch errors,
processing non-whole-numbers without throwing ValueErrors,
and loading the ledger table in Tkinter. But thanks to Stack Overflow, 
I was able to solve every error and construct a working checking ledger!

I chose to complete this project because I wanted to create an application that is
somewhat simple but very useful for the major real-world task of financial management.
This project also taught me basic Pandas and data-analysis skills that will be very helpful
in more advanced projects down the line, 
especially others' projects that I would like to fork and enhance.

I am assigning a GPL license to this project to facilitate expansions and modifications.
