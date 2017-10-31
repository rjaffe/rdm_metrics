import csv, sys
from collections import Counter
import config_v2

# CSV now generated from Google sheet ("Research IT Consulting Engagement Log"), \
# then filtered for date and RDM


# Column headers (row to be removed):
#    [0] Start date
#    [1] Consultant(s)
#    [2] Client(s)
#    [3] PI (Whose project is it?)
#    [4] Department/ORU
#    [5] Research Domain (e.g. Egyptology)
#    [6] Position (grad, postdoc, faculty, undergrad, researcher)
#    [7] Project type (dissertation, etc.)
#    [8] Related course (if applicable)
#    [9] Research IT service
#    [10] Topic (uncontrolled)
#    [11] Category (controlled)
#    [12] Source
#    [13] Hand-off and/or referral
#    [14] Complexity (RDM)
#    [15] Status
#    [16] Link to details
#    [17] Notes
#    [18] (empty)

filename = sys.argv[1]
report_period_descriptor = sys.argv[2]
#TO-DO: Add code to accept report_period_date_filter arguments

myrows = []

# Read data into a list of lists, clean as required
with open(filename) as csvfile:
    for row in csv.reader(csvfile, delimiter=","):
        # Remove rows in which "Is this question answered?" is blank -- i.e., 'FYI only' engagements
        # if not row[3]: continue

        # Remove rows in which Research IT Service does not include RDM
        # Note that this removes the header row since its row element [9] does not contain the text 'RDM'
        RIT_service = row[9]
        if not 'RDM' in RIT_service: continue

        # Consultant(s), Department/ORU, Patron status, (RDM Lifecycle) Category, Source (aka referral in),
        # Hand-off or referral (aka referral out), Consultation complexity, Library division, and
        # Organizational partner: replace empty values with appropriate label
        for n, label in zip(config_v2.dictable_cols, config_v2.labels):
            if row[n] == '':
                row[n] = label
            # make every cell into a list (some cells have new-line separated values)
            row[n] = row[n].split('\n')
        # Replace individual names with the corresponding org name in Source (aka Referral In) and
        # Hand-off or referral (aka Referral Out) fields
        # (positional elements [12] and [13])
        for n in [12, 13]:
            ref_x = row[n]
            row[n] = []  # Empty cell to ready it for being re-filled
            for term in ref_x:
                for key in config_v2.refs.keys():
                    if term in config_v2.refs[key][1]:
                        term = config_v2.refs[key][0]
                        row[n].append(term)
        myrows.append(row)

# ***** COUNT THE DATA *****
# Each row (list) represents a consulting engagement
print('\nIn %s, RDM Consulting provided %d consultations.' % (report_period_descriptor, (len(myrows))))

# Count how many engagements are resolved successfully
yesrows = []

for r in myrows:
    r15 = r[15]
    if 'Resolved' in r15:
        yesrows.append(r)

print('We reached a successful resolution in %d of those engagements.' % len(yesrows))

# Gather and count (subtotal) the values for consultant(s), department/oru, patron status, (RDM lifecycle) category,
# source (referrals in), hand-off or referral (referrals out) and consultation complexity.
# TODO: calculate values for library division and organizational partners fields
for i, n in enumerate(config_v2.dictable_cols):
    counter = Counter()
    for row in myrows:
        for z in row[n]:
            counter[z] += 1
    print('\n' + config_v2.headings[i] + ':')
    for (k, v) in counter.most_common():
        print(k + ', ' + str(v))
