# Immigration Case Tracker

This project contains the scripts to get the the immigration case status.

## How to use it

The main script, *ImmiStatusConsole.py*, can be ran with the following command:

```
python ImmiStatusConsole.py <path/to/config.ini>
```

And it can be ran in 3 different modes, defined in the *config.ini* file:

* Search cases
* Retrieve cases
* Compare case status


### 1. Search Cases
This mode allows to provide a list of seed case numbers, and search *N* sequential cases following each of the seed case numbers. An optional parameters can be set to search cases by exact string match, for example: search "I-485" cases, search "Interview Scheduled" cases, etc.

In order to run the script in the "Search Cases" mode, write a configuration file as follows:

config.ini - search all
```
[SearchCases]
SeedCasesFilePath=<path/to/seed_case_numbers.txt>
NumberSequentialCases=<N>
OutputFilePath=<path/to/output/searched_cases.tsv>
```

Or, config.ini - search by exact string match
```
[SearchCases]
SeedCasesFilePath=<path/to/seed_case_numbers.txt>
NumberSequentialCases=<N>
SearchMatch=<search string, for example I-485>
OutputFilePath=<path/to/output/searched_cases.tsv>
```

The *seed_case_numbers.txt* file containing the seed case numbers to search for, should contain one case number per line, such as:
```
LIN2000150001
LIN2000150101
MSC2000150101
etc.
```

Examples can be found in:
* repo/samples/01_search_case_status_all/
* repo/samples/02_search_case_status_search_query/


### 2. Retrieve Cases

This mode allows to retrieve case status given a list of case numbers.

In order to run the script in the "Retrieve Cases" mode, write a configuration file as follows:

config.ini
```
[RetrieveCases]
CasesFilePath=<path/to/case_numbers.txt>
OutputFilePath=<path/to/output/retrieved_cases.tsv>
```

The *case_numbers.txt* file containing the case numbers to be retrieved, should contain one case number per line, such as:
```
LIN2000150001
LIN2000150101
MSC2000150101
etc.
```
Or, it can be a tab separated file with the case numbers in the first column, such as the output of the "1. Search Cases" mode:
```
LIN2000150001 TAB Status title TAB Status description
LIN2000150101 TAB Status title TAB Status description
MSC2000150101 TAB Status title TAB Status description
etc.
```

Example can be found in:
* repo/samples/03_retrieve_case_status/


### 3. Compare Case Status

This mode allows to compare case status from two different lists of cases status. It can be used to compare a file with past cases status with the current online status, or it can be used to compare past and new cases status stored in two separate files.

In order to run the script in the "Compare Cases" mode, write a configuration file as follows:

config.ini - compare cases status with current online status
```
[CompareCases]
ControlCasesFile=<path/to/cases_to_compare.tsv>
```

Or, config.ini - compare cases status between old and new cases
```
[CompareCases]
ControlCasesFile=<path/to/old_cases_status.tsv>
TreatmentCasesFile=<path/to/new_cases_status.tsv>
```

The *case_numbers.txt* file containing the case numbers to be compared, should be tab separated with the case numbers in the first column, the status title in the second column and the status description in the third column, such as the output of the "1. Search Cases" mode or the output of the "2. Retrieve Cases" mode:
```
LIN2000150001 TAB Status title TAB Status description
LIN2000150101 TAB Status title TAB Status description
MSC2000150101 TAB Status title TAB Status description
etc.
```

Examples can be found in:
* repo/samples/04_compare_case_status_with_current_online/
* repo/samples/05_compare_case_status_between_two_files/


