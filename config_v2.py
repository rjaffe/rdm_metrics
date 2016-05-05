# Positional elements (columns) with the following indices -- and only those elements, at present --
# will be gathered and counted using a dictionary
dictable_cols = [4, 5, 6, 7, 8, 9]

# let the data do the heavy lifting...everything is in this dict!
refs = {
    'lib': ['The Library', ['Harrison Dekker', 'Jamie Wittenberg', 'Susan Edwards', 'Steve Mendoza', 'Steven Mendoza',
                            'Margaret Phillips', 'data-consult list (Library)', 'Brian Quigley']],
    'css': ['Campus Shared Services - IT', ['Brett Larsen', 'Daniel Bass']],
    'dlab': ['D-Lab', ['D-Lab Consulting List', 'D-Lab', 'Jon Stiles', 'Zawadi Rucks Ahidiana']],
    'scf': ['Statistical Computing Facility', ['Chris Paciorek', 'Ryan Lovett']],
    'brc': ['Berkeley Research Computing',
            ['Patrick Schmitz', 'Aron Roberts', 'Aaron Culich', 'Jason Christopher', 'Kelly Rowland',
             'BRC Cloud Consulting']],
    'dh': ['Digital Humanities @ Berkeley', ['Quinn Dombrowski', 'Camille Villa', 'Digital Humanities']],
    'rdm': ['RDM Consulting', ['researchdata@berkeley.edu', 'Rick Jaffe', 'Chris Hoffman']],
    'cdl': ['California Digital Library', ['Joan Starr', 'Stephanie Simms']],
    'ist': ['Information Services & Technology - API', ['Jennifer Bellenger', 'Jon Broshious', 'Ian Crew', 'Jon Hays']],
    'micronet': ['Micronet', ['micronet', 'Micronet', 'micronet list', 'Micronet list']]
}

labels = ['', 'None', 'Unknown department', 'Consultation(s) without a partner', 'Unknown', '']

headings = ['Referrals In', 'Referrals Out', 'Departments served (number of engagements)',
            'Organizational partners (number of shared engagements)', 'Patron status (number of patrons)', 'Consultation complexity']
