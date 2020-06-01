# Immigration Case Tracker

This project contains the scripts to get the the immigration case status.

## How to use it

The main script, ImmiStatusConsole.py, can be ran in 3 different modes:

### 1. Search Cases Configuration Mode: 
This mode allows to provide a list of seed case numbers, and search N sequential cases following each of the seed case numbers. An optional parameters can be set to search cases by exact string match, for example search "I-485" cases, search "Interview Scheduled" cases, etc.

In order to run the script in the "Search Cases" mode, write a configuration file as follows:

config.ini, search all
`
[SearchCases]<br/><br/>
SeedCasesFilePath=<path/to/seed_case_numbers.txt>
NumberSequentialCases=<N>
OutputFilePath=<path/to/output/searched_cases.tsv>
`

config.ini, search by exact string match
`
[SearchCases]
SeedCasesFilePath=<path/to/seed_case_numbers.txt>
NumberSequentialCases=<N>
SearchMatch=<search string, for example I-485>
OutputFilePath=<path/to/output/searched_cases.tsv>
`

The seed_case_numbers.txt file containing the seed case numbers to search for, should be formatted with one case number per line, such as:
`
LIN2000150001
LIN2000150101
MSC2000150101
etc.
`

Examples can be found in:
* repo/samples/01_search_case_status_all/
* repo/samples/02_search_case_status_search_query/

