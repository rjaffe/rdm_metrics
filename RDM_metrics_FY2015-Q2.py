#! python3.4.2

import csv, sys

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

# Positional elements (columns) with the following indices -- and only those elements, at present --
# will be gathered and counted using a dictionary
# TODO: Move this to a configuration file?
dictable_cols = [3, 4, 5, 6, 7]


##########################
#  Define our functions  #
##########################
def remove_headers(rows):
    """
    Removes the first list within a list of lists ("The first row of the table").
    
    Returns a list of lists without the list containing the headers.
    """
    rows.pop(0)
    return rows


def parse_date(rows):
    """
    Accepts a list of lists, splits the textual 'Date/Time' field (positional element [1]) in each row
    into the two values: start date and end date, and adds those values to the end of the row,
    i.e., as positional elements [8] (startdate) and [9] (enddate).

    Creates two new positions in list ("columns")
    [8] startdate
    [9] enddate

    Returns a list of lists with each row modified to include the date parts.
    
    >>> origrows = [['a', 'Tuesday, December 8, 2015 to Thursday, December 10, 2015', 'c', 'd', 'e', 'f', 'g', 'h'], ['i', 'Monday, October 26, 2015 to Wednesday, October 28, 2015', 'k', 'l', 'm', 'n', 'o', 'p']]
    >>> modrows = parse_date(origrows)
    >>> print(modrows)
    [['a', 'Tuesday, December 8, 2015 to Thursday, December 10, 2015', 'c', 'd', 'e', 'f', 'g', 'h', 'Tuesday, December 8, 2015', 'Thursday, December 10, 2015'], ['i', 'Monday, October 26, 2015 to Wednesday, October 28, 2015', 'k', 'l', 'm', 'n', 'o', 'p', 'Monday, October 26, 2015', 'Wednesday, October 28, 2015']]
    """
    for r in rows:
        datetime = r[1]
        splitbefore = datetime.find(" to ")
        splitafter = splitbefore + 4
        startdate = datetime[:splitbefore]
        enddate = datetime[splitafter:]
        r.extend([startdate, enddate])
    return rows


def remove_fyi_rows(rows):
    """
    Accepts a list of lists, removes the lists that have no value for 
    'Is this question answered?', i.e. the ones that weren't really requests for help.
    
    Returns a 'cleaned' list of lists
    
    >>> fulllist = [['a','b','c','d'], ['e','f','','h'], ['i','j','k','l']]
    >>> cleanlist = remove_fyi_rows(fulllist)
    >>> print(cleanlist)
    [['a', 'b', 'c', 'd'], ['i', 'j', 'k', 'l']]
    """
    rows = [r for r in rows if r[2]]  # empty string is not 'truthy'
    return rows


def resolved_count(rows):
    """
    Accepts a list of lists, passes the lists that have the value 'Yes, we have an answer!' 
    for the column 'Is this question answered?'
    
    NOTE: This function counts engagements that have been answered prior to the moment
    that the data were exported, not by the end of the reporting period.
    
    Returns the count of engagements that have been successfully resolved.
    
    >>> fulllist = [['a','b','c','d'], ['e','f','Yes, we have an answer!','h'], ['i','j','k','l']]
    >>> resolvedcount = resolved_count(fulllist)
    >>> print(resolvedcount)
    1
    """
    rows = [r for r in rows if r[2] == 'Yes, we have an answer!']
    return len(rows)


def group_referrals(rows):
    """
    Parses list of lists for string values in Referral In and Referral Out fields
    (positional elements [3] and [4]), and replaces individual names with the corresponding org name
    
    Returns list of lists
    
    >>> referrals_in = [[0, 1, 2, 'Harrison Dekker', '4'], [5, 6, 7, 'Quinn Dombrowski', '9']]
    >>> group_referrals(referrals_in)
    [[0, 1, 2, 'Library', '4'], [5, 6, 7, 'Digital Humanities', '9']]
    """
    # Group individuals involved in referrals into organizational units 
    # Rules: 
    # 1. Referrals from Jamie or Harrison are credited to the Library, 
    #    while referrals from Chris or Rick are credited to RDM Consulting.
    # 2. RDM Consultations done by any of the four of us are not considered to be referred out.
    # TODO: Move this to a configuration file?
    ref_lib = ['Harrison Dekker', 'Jamie Wittenberg', 'Susan Edwards', 'Steve Mendoza', 'Steven Mendoza',
               'Margaret Phillips', 'data-consult list (Library)']
    ref_css = ['Brett Larsen']
    ref_dlab = ['D-Lab Consulting List', 'D-Lab', 'Jon Stiles', 'Zawadi Rucks Ahidiana']
    ref_scf = ['Chris Paciorek', 'Ryan Lovett']
    ref_brc = ['Patrick Schmitz', 'Aron Roberts', 'Aaron Culich', 'Jason Christopher', 'Kelly Rowland',
               'BRC Cloud Consulting']
    ref_dh = ['Quinn Dombrowski', 'Camille Villa', 'Digital Humanities']
    ref_rdm = ['researchdata@berkeley.edu', 'Rick Jaffe', 'Chris Hoffman']

    for r in rows:
        ref_ins = []
        ref_outs = []
        # Referrals In always has a value, sometimes multiple values.
        # Note: these data come from a comma-separated taxonomy (tag) field in Drupal -
        # there is no way for a value to contain a comma; commas only separate values.
        if r[3].find(', '):
            ref_ins = r[3].split(', ')
        else:
            ref_ins = r[3]
        r[3] = []  # Empty cell to ready it for being re-filled
        for term in ref_ins:
            if term in ref_lib:
                term = 'The Library'
                r[3].append(term)
            if term in ref_css:
                term = 'Campus Shared Services - IT'
                r[3].append(term)
            if term in ref_dlab:
                term = 'D-Lab'
                r[3].append(term)
            if term in ref_scf:
                term = 'Statistical Computing Facility'
                r[3].append(term)
            if term in ref_brc:
                term = 'Berkeley Research Computing'
                r[3].append(term)
            if term in ref_dh:
                term = 'Digital Humanities @ Berkeley'
                r[3].append(term)
            if term in ref_rdm:
                term = 'RDM Consulting'
                r[3].append(term)
        # Referrals Out may be blank. (Does that matter here?)
        # Note: these data come from a comma-separated taxonomy (tag) field in Drupal -
        # there is no way for a value to contain a comma; commas only separate values.
        if r[4].find(', '):
            ref_outs = r[4].split(', ')
        else:
            ref_outs = r[4]
        r[4] = []  # Empty cell to ready it for being re-filled
        for term in ref_outs:
            if term in ref_lib:
                term = 'The Library'
                r[4].append(term)
            if term in ref_css:
                term = 'CSS-IT'
                r[4].append(term)
            if term in ref_dlab:
                term = 'D-Lab'
                r[4].append(term)
            if term in ref_scf:
                term = 'Statistical Computing Facility'
                r[4].append(term)
            if term in ref_brc:
                term = 'Berkeley Research Computing'
                r[4].append(term)
            if term in ref_dh:
                term = 'Digital Humanities @ Berkeley'
                r[4].append(term)
            if term in ref_rdm:  # Shouldn't ever happen
                term = 'RDM Consulting'
                r[4].append(term)
    return rows


def clean_cols(rows, n, returnstatement):
    """ Accepts a list of lists (rows), an integer, and a string. Replaces empty values
    in positional element n of each row ("Referrals In," "Referrals Out," "Department," "Organizational
    partners," or "Patron status") with the text passed to the function as returnstatement.

    Returns list of lists (rows) with field n cleaned of empty values

    >>> list_with_empty_dept_values = [['a', 'b', 'c', 'd', 'e', 'Music Dept.', 'g', 'h'], ['i', 'j', 'k', 'l', 'm', 'School of Public Health', 'o', 'p'], ['q', 'r', 's', 't', 'u', '', 'w', 'x']]
    >>> list_with_cleaned_dept_values = clean_cols(list_with_empty_dept_values, 5, 'Unknown department')
    >>> print(list_with_cleaned_dept_values)
    [['a', 'b', 'c', 'd', 'e', 'Music Dept.', 'g', 'h'], ['i', 'j', 'k', 'l', 'm', 'School of Public Health', 'o', 'p'], ['q', 'r', 's', 't', 'u', 'Unknown department', 'w', 'x']]
    """
    assert n in dictable_cols, 'Only Referrals In, Referrals Out, Department, Organizational partners and ' \
                               'Patron status can be cleaned using a dictionary at this time.'
    for r in rows:
        if r[n] == '':
            r[n] = returnstatement
    return rows


def dict_from_cols(rows, n, startvalue=0):
    """ Accepts a list of lists, an integer n representing a position in the row
    (i.e, the slot for "Referrals in, Referrals out, etc.), and an integer startvalue.

    For each positional element n of each row (i.e., for each "column"),
    creates a dictionary with each unique string found in that column as a key,
    and a count of the number of times that the key appears as the value.
    """
    assert n in dictable_cols, 'Only Referrals In, Referrals Out, Department, Organizational partners ' \
                               'and Patron status can be cleaned using a dictionary at this time.'
    # Handles multi-valued fields in a way consistent with what we did when grouping referrals in and out,
    # so that all entries are alike. Then tests to see if the string has already
    # been added as a key to the dictionary, adds it if not, and increments its value if so.
    entries = []
    dict = {}
    for r in rows:
        if type(r[n]) == list:
            entries = r[n]
        else:
            if r[n].find(', '):
                entries = r[n].split(', ')
            else:
                entries = r[n]
        for e in entries:
            if e in dict:
                k = e
                v = dict[k]
                dict[k] = v + 1
            else:
                k = e
                dict[k] = startvalue + 1
    return dict


def print_dict(dict, heading):
    """
    Accepts a dictionary and a string (label text).

    Prints an empty line, then the heading followed by a colon, then - starting on a new line -
    the list of keys, with the associated values in parentheses.
    """
    print('\n' + heading + ':')
    for k, v in dict.items():
        print(k + ' (' + str(v) + ')')


def print_sorted(sorted_list, heading):
    """
    Accepts a list of tuples (key, value pairs from a dictionary) and a string (label text).

    Prints an empty line, then the heading followed by a colon, then - starting on a new line -
    the list of keys, with the associated values in parentheses.
    """
    print('\n' + heading + ':')
    for (k, v) in sorted_list:
        print(k + ' (' + str(v) + ')')


##############################
#  Here we begin the 'work'  #
##############################

# ***** READ THE DATA *****
# Initialize our container
myrows = []

# Path to csv file exported from Drupal
# TODO: Move basepath to a configuration file?
# basepath = ''
# Replace '' with fully-qualified path to folder containing file when running Python 2 or 3 in pyCharm
basepath = '/Users/rjaffe/Documents/RDM/RDM_Metrics/MetricsData/'
# Use this basepath when working in iPython notebook on Rick's virtual box BCE instance
# basepath = '/home/oski/Desktop/Shared/sf_VBox-BCE_sf_Documents/'
# Replace sys.argv[1] with 'RDMConsulting_Ricks_view_FY2015-Q2_2016-02-01T16-28-11.csv'
# when running Python 2 or 3 in pyCharm
# filename = sys.argv[1]
filename = 'RDMConsulting_Ricks_view_FY2015-Q2_2016-02-06T12-50-39.csv'
path = basepath + filename
# print(path)  # Check location of file

# Read data into a list of lists, clean as required, and count various metrics
with open(path) as csvfile:
    for row in csv.reader(csvfile, delimiter=","):
        assert isinstance(row, object)
        myrow = row
        # print(myrow)  # What does the row look like?
        # Add all the individual rows into a list of rows
        myrows.append(myrow)
        # print(myrows) # What does the data look like?
        # print(len(myrows)) # How many rows before removing header row and 'FYI only' rows?

    # ***** CLEAN THE DATA *****
    # Remove header row
    myrows = remove_headers(myrows)
    # print(len(myrows))  # Check that the header row has been removed

    # Split datetime field (element [1]) into startdate, enddate; append to row as elements [8] and [9], respectively
    # Can be used to filter engagements by date, to calculate the length of consultations, etc.
    myrows = parse_date(myrows)

    # Remove rows in which "Is this question answered?" is blank -- i.e., 'FYI only' engagements
    myrows = remove_fyi_rows(myrows)

    # Attribute individual referrals to the proper group
    myrows = group_referrals(myrows)

    # Referrals in, Referrals out, Clean Department, Organizational partner and Patron status "columns":
    # replace empty values with appropriate label
    # TODO: Move labels to a configuration file?
    labels = ['', 'None', 'Unknown department', 'Consultation(s) without a partner', 'Unknown']
    for n, label in zip(dictable_cols, labels):
        myrows = clean_cols(myrows, n, label)

    # Change name to signify the completion of cleaning
    cleanrows = myrows
    # print(cleanrows) # Check that all the clean-up has been done successfully.

    # ***** COUNT THE DATA *****
    # Each remaining row (list) represents a consulting engagement
    quarterly_consultations = (len(cleanrows))
    print('\nIn FY2015-Q2, RDM Consulting provided %d consultations.' % quarterly_consultations)

    # Count how many engagements are resolved successfully
    answered = resolved_count(cleanrows)
    print('We reached a successful resolution in %d of those engagements.' % answered)

    # Gather and count (subtotal) the values for referrals in, referrals out, departments,
    # organizational partners and patron status (only those five "columns" for now).
    # Save each as a dictionary, then combine into a list of dicts.
    saved_dicts = []  # This will be the list of dicts
    for n in dictable_cols:
        gather_and_count = dict_from_cols(cleanrows, n)
        saved_dicts.append(gather_and_count)

    # Store as separate dictionaries for further processing
    d_refsin, d_refsout, d_depts, d_partners, d_patrons = saved_dicts

    # ***** OUTPUT (SORT, PRINT) THE DATA *****
    # Prepare iterable for sorting, printing
    dicts = [d_refsin, d_refsout, d_depts, d_partners, d_patrons]

    # Sort each dict by value, descending, then by key ascending (i.e., alphabetical), per lambda below
    # Thank you to http://stackoverflow.com/a/15371752 for the sort algorithm
    list_of_sorted = []  # This will be the list of sorted (key, value) pairs from each dictionary
    for d in dicts:
        sort = [(key, value) for (key, value) in sorted(d.items(), key=lambda x: (-x[1], str.lower(x[0])))]
        list_of_sorted.append(sort)

    # Store as separate lists for further processing
    sorted_refsin, sorted_refsout, sorted_depts, sorted_partners, sorted_patrons = list_of_sorted

    # Prepare iterable of sorted values for printing
    sorted_lists = [sorted_refsin, sorted_refsout, sorted_depts, sorted_partners, sorted_patrons]

    # Print each dictionary under the appropriate heading
    # TODO: Move headings to a configuration file?
    headings = ['Referrals In', 'Referrals Out', 'Departments served (number of engagements)',
                'Organizational partners (number of shared engagements)', 'Patron status (number of patrons)']
    # Uncomment the next two lines to print each dictionary, unsorted
    #for dict, heading in zip(dicts, headings):
    #   print_dict(dict, heading)

    # Uncomment the two lines after this comment to print each dictionary sorted by value, in descending order,
    # then by key, in ascending order (i.e., alphabetically)
    for list, heading in zip(sorted_lists, headings):
        print_sorted(list, heading)
