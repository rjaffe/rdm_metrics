import csv, sys
from collections import Counter
import config_v2

# View now produces Date/Time End and Library Division columns so the row no.'s have shifted

# Column headers (row to be removed):
#    [0] Title ("Question asked")
#    [1] Date/Time (Start)
#    [2] Date/Time (End)
#    [3] Is this question answered?
#    [4] Referral in
#    [5] Referral out
#    [6] Department
#    [7] Library division
#    [8] Organizational partners
#    [9] Patron status
#    [10] Consultation complexity

filename = sys.argv[1]
report_period_descriptor = sys.argv[2]
#TO-DO: Add code to accept report_period_date_filter arguments
myrows = []

# Read data into a list of lists, clean as required
with open(filename) as csvfile:
    for row in csv.reader(csvfile, delimiter=","):
        # Remove rows in which "Is this question answered?" is blank -- i.e., 'FYI only' engagements
        if not row[3]: continue

        # Referrals in, Referrals out, plus controlled-vocabularies "columns"
        # Department, Library division, Organizational partner, Patron status and Consultation complexity:
        # replace empty values with appropriate label
        for n, label in zip(config_v2.dictable_cols, config_v2.labels):
            if row[n] == '':
                row[n] = label
            # make every cell into a list (some cells have comma separated values)
            row[n] = row[n].split(', ')
        # Replace individual names with the corresponding org name in Referral In and Referral Out fields
        # (positional elements [4] and [5])
        for n in [4, 5]:
            ref_x = row[n]
            row[n] = []  # Empty cell to ready it for being re-filled
            for term in ref_x:
                for key in config_v2.refs.keys():
                    if term in config_v2.refs[key][1]:
                        term = config_v2.refs[key][0]
                        row[n].append(term)
        myrows.append(row)
    # Remove header row -- it throws off counts.
    myrows = myrows[1:]


# ***** COUNT THE DATA *****
# Each row (list) except first (header) row represents a consulting engagement
print('\nIn %s, RDM Consulting provided %d consultations.' % (report_period_descriptor, (len(myrows))))

# Count how many engagements are resolved successfully
yesrows = [r for r in myrows if r[3] == 'Yes, we have an answer!']
print('We reached a successful resolution in %d of those engagements.' % len(yesrows))

# Gather and count (subtotal) the values for referrals in, referrals out, departments,
# organizational partners, patron status, and consultation complexity (only those six "columns" for now).
for i, n in enumerate(config_v2.dictable_cols):
    counter = Counter()
    for row in myrows:
        for z in row[n]:
            counter[z] += 1
    print('\n' + config_v2.headings[i] + ':')
    for (k, v) in counter.most_common():
        print(k + ', ' + str(v))
