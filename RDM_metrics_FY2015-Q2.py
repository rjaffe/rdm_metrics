import csv, sys
from collections import Counter

# Let's try analyzing the data without using pandas and data frames

# Column headers (row to be removed):
#    [0] Title ("Question asked")
#    [1] Date/Time
#    [2] Is this question answered?
#    [3] Referral In 
#    [4] Referral Out 
#    [5] Department 
#    [6] Organizational partners 
#    [7] Patron status

from config import *

filename = sys.argv[1]
myrows = []

# Read data into a list of lists, clean as required
with open(filename) as csvfile:
    for row in csv.reader(csvfile, delimiter=","):
        # Remove rows in which "Is this question answered?" is blank -- i.e., 'FYI only' engagements
        if not row[2]: continue
        try:
            (startdate, enddate) = row[1].split(' to ')
        except:
            # if there is no 'to', assume startdate == enddate
            (startdate, enddate) = (row[1], row[1])
        # Create positional elements [8] startdate and [9] enddate
        row.extend([startdate, enddate])

        # Referrals in, Referrals out, Clean Department, Organizational partner and Patron status "columns":
        # replace empty values with appropriate label
        for n, label in zip(dictable_cols, labels):
            if row[n] == '':
                row[n] = label
            # make every cell into a list (some cells have comma separated values)
            row[n] = row[n].split(', ')
        # Replace individual names with the corresponding org name in Referral In and Referral Out fields
        # (positional elements [3] and [4])
        for n in [3, 4]:
            ref_x = row[n]
            row[n] = []  # Empty cell to ready it for being re-filled
            for term in ref_x:
                for key in refs.keys():
                    if term in refs[key][1]:
                        term = refs[key][0]
                        row[n].append(term)
        myrows.append(row)

# ***** COUNT THE DATA *****
# Each row (list) except first (header) row represents a consulting engagement
print('\nIn FY2015-Q2, RDM Consulting provided %d consultations.' % (len(myrows) - 1))

# Count how many engagements are resolved successfully
yesrows = [r for r in myrows if r[2] == 'Yes, we have an answer!']
print('We reached a successful resolution in %d of those engagements.' % len(yesrows))

# Gather and count (subtotal) the values for referrals in, referrals out, departments,
# organizational partners and patron status (only those five "columns" for now).
for i, n in enumerate(dictable_cols):
    counter = Counter()
    for row in myrows:
        for z in row[n]:
            counter[z] += 1
    print('\n' + headings[i] + ':')
    for (k, v) in counter.most_common():
        print(k + ' (' + str(v) + ')')
