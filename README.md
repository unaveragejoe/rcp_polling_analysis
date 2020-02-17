# RealClearPolitics poll filtering/analysis (WIP)
A class to allow for filtering, and weighted/unweighted averages of polling results. Work in progress.

The input is the URL of a RCP url (example: https://www.realclearpolitics.com/epolls/2020/president/us/2020_democratic_presidential_nomination-6730.html).

The ouput allows the following features:
- Aggregate voting percentages by any # of most recent polls
- Filter by polls that sample Registered Voters vs Likely Voters
- Provide both weighted and unweighted averages by sample size
- Exclude specific polls and polls that sampled below or above a certain number of people
- Filter by date (WIP)
