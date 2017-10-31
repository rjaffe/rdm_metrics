import csv, sys
import re
from collections import Counter
from datetime import date, datetime
import config_v3  # Configuration of the dictionaries. File location relative to this script

# CSV now generated from Google sheet ("Research IT Consulting Engagement Log"), 
# then filtered for date, RIT Service (= 'RDM') and Category 
# (= consultation-related categories: 'user support' + all categories beginning 'RDM')

# These are the arguments that must be provided to the script
# 1 & 2. The filepath and filename that points to the .csv containing our data,   \
#        (which is now being generated from the "Research IT Consulting Engagements Log.")
# 3.     The 'report_period_descriptor' will be the text included in the first line \
#        of the report created by the script.
# 4 & 5. Report_start and report_end are the beginning and end dates (inclusive) \
#        of the period covered by the report.

# Uncomment these if you want to provide arguments at the command line.
# TODO: Add way to import these from a metrics_args... file.
filepath =  sys.argv[1] # Path to csv file
filename =  sys.argv[2] # csv file name
report_period_descriptor = sys.argv[3]
report_start = sys.argv[4]
report_end = sys.argv[5]

# To help keep us humans from confusion, here's a list of the column headers \
# in the original Google sheet. We will refer to these "columns" in the script \
# by their position in each row, with the first column being element [0].

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


# CLEAN THE DATA
# TODO - Catch and handle missing arguments or errors in the arguments

# Convert report_start and report_end arguments to datetime format
reportstart = datetime.strptime(report_start, '%Y-%m-%d')
reportend = datetime.strptime(report_end, '%Y-%m-%d')


myrows = []

# Read data into a list of lists, clean as required
with open(filepath + filename) as csvfile:
    for row in csv.reader(csvfile, delimiter=","):

        # Filter Google sheet to include only RDM consultations during the desired period.
        
        # Remove header row (first header value is 'Start Date')
        if row[0] == 'Start Date': continue

        
        # Convert start date values (first column) to datetime format and \
        # compare against report-start and report-end arguments. Skip if start date is not in report period range
        startdate = datetime.strptime(row[0], '%Y-%m-%d')
        if not reportstart <= startdate <= reportend: continue
            
        # Remove rows in which Research IT Service does not include RDM
        RIT_service = row[9]
        if not 'RDM' in RIT_service: continue

        # Remove rows that are not consultations. For RDM, consultations were listed as 'User support' \
        # or (once) 'Library user support' until late February 2017. \
        # After that, they were coded as 'RDM [service area]', sometimes with multiple values listed
        p = re.compile(r'^.*[Uu]ser support.*$')  # Matches 'User support' or 'Library user support'
        p1 = re.compile(r'^.*(RDM)')  # Matches an instance of 'RDM [service area]'
        category = row[11]
        if not ((p.match(category)) or (p1.match(category))): continue
 

        # Now clean, split multiple values, and aggregate (roll up) values as appropriate
        
        # Consultant(s), Department/ORU, Patron status, (RDM Lifecycle) Category, Source (aka referral in),
        # Hand-off or referral (aka referral out), Consultation complexity: \
        # replace empty values with appropriate label
        # NOTE: We didn't port Library division and Organizational partner fields to the Google sheet
        
        for n, label in zip(config_v3.dictable_cols, config_v3.labels):  ## USE THIS IN PYCHARM
        #for n, label in zip(dictable_cols, labels):  ## USE THIS IN A JUPYTER NOTEBOOK

            # Fill in empty cells with appropriate label
            if row[n] == '':
                row[n] = label
                    
            # Remove trailing soft returns (i.e.,\n) -- it's hard to control these in Google Sheets.
            val = row[n]
            suffix = '\n'
            if(val.endswith(suffix)):
                val = val[:-1]
                row[n] = val  # I don't completely trust this, but I don't seem to be losing any data!
            
            # make every cell into a list (some cells have new-line separated values)
            row[n] = row[n].split('\n')
        # Replace individual names with the corresponding org name in Source (aka Referral In) and
        # Hand-off or referral (aka Referral Out) fields
        # (positional elements [12] and [13])
        for n in [12, 13]:
            ref_x = row[n]
            row[n] = []  # Empty cell to ready it for being re-filled
            for term in ref_x:
                for key in config_v3.refs.keys():        ## USE THIS IN PYCHARM
                #for key in refs.keys():                 ## USE THIS IN A JUPYTER NOTEBOOK
                    if term in config_v3.refs[key][1]:   ## USE THIS IN PYCHARM
                    #if term in refs[key][1]:            ## USE THIS IN A JUPYTER NOTEBOOK
                        term = config_v3.refs[key][0]    ## USE THIS IN PYCHARM
                        #term = refs[key][0]             ## USE THIS IN A JUPYTER NOTEBOOK
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
for i, n in enumerate(config_v3.dictable_cols):
    counter = Counter()
    for row in myrows:
        for z in row[n]:
            counter[z] += 1
    print('\n' + config_v3.headings[i] + ':')
    for (k, v) in counter.most_common():
        print(k + ', ' + str(v))
