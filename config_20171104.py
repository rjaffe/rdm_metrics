# Positional elements (columns) with the following indices -- and only those elements, at present --
# will be gathered and counted using a dictionary
dictable_cols = [1, 4, 6, 11, 12, 13, 14]

# In this version, we bring the "dictable columns" into dictionaries called:
# • ccounter (consultants) 
# • dcounter (departments/ORUs)
# • pcounter (position)
# • cacounter (category)
# • scounter (source)
# • rcounter (referrals in and out) and 
# • cocounter (complexity).

# Next we do modifications -- rolling up departmental values to their school, college or organizational parent; 
# L&S is first rolled up to its divisions, then aggregated as a college -- and store in new dictionaries: 
# • pacounter for values rolled-up by parent
# • lscounter for Letters & Science divisions rolled up into a single total

#Initialize dictionaries that we'll use later
ccounter, dcounter, pcounter, cacounter, scounter, rcounter, cocounter, \
pacounter, lscounter = {},{},{},{},{},{},{},{},{}

# let the data do the heavy lifting...everything is in this dict!
ref_rollups = {
    'lib': ['The Library', ['Harrison Dekker', 'Jamie Wittenberg', 'Susan Edwards', 'Steve Mendoza', 'Steven Mendoza',
                            'Margaret Phillips', 'data-consult list (Library)', 'Brian Quigley', 'Library',
                            'Data Storage/Sharing and the Social Sciences Working Group', 'Erik Mitchell',
                            'Susan Powell', 'Anna Sackmann', 'David Eiffler', 'Yasmin Alnoamany', 'Stacy Reardon',
                            'Celia Emmelhainz', 'Hilary Schiraldi', 'Amy Neeser']],
    'css': ['Campus Shared Services - IT', ['Brett Larsen', 'Daniel Bass', 'Johnathon Kogelman',
                                            'Johnathon Kogelman (CSS-IT)', 'CSS-IT', 
                                            'Referred by Johnathon Kogelman (CSS-IT)', 
                                            'request to Rick from Daniel Bass',
                                            'email to Rick from Daniel Bass',
                                            'CSS_IT (Jon Valmores)']],
    'dlab': ['D-Lab', ['D-Lab Consulting List', 'D-Lab', 'Jon Stiles', 'Zawadi Rucks Ahidiana',
                       'Rick Jaffe (via D-Lab Consulting web page)', 'dlab-consultants@lists.b.e', 
                       'd-lab consultants list', 'referred to D-Lab/Jon Stiles', 'D-Lab consultants list',
                       'Rick at d-lab consulting Ticket #29430', 'D-Lab ticket#29433', 'Chris Hench (D-Lab)']],
    'scf': ['Statistical Computing Facility', ['Chris Paciorek', 'Ryan Lovett']],
    'brc': ['Berkeley Research Computing',
            ['Patrick Schmitz', 'Aron Roberts', 'Aaron Culich', 'Jason Christopher', 'Kelly Rowland', 'Gary Jung',
             'BRC Cloud Consulting', 'Jason Huff (Computational Genomics Resource Lab)',
             'Berkeley Research Computing - Cloud', 'Yong Qin', 'Deb McCaffrey', 'email to BRC', 
             'brc@berkeley.edu']],
    'dh': ['Digital Humanities @ Berkeley', ['Quinn Dombrowski', 'Camille Villa', 'Digital Humanities',
                                             'Claudia Natalia Von Vacano']],
    'rdm': ['RDM Consulting', ['researchdata@berkeley.edu', 'Rick Jaffe', 'Chris Hoffman', 'John B Lowe',
                               'BRC Survey 2016 (Response to follow-up from Jamie)', 'email to Rick Jaffe', 
                               'Follow-up', 'Rick', 'follow up', 'email to Rick and Jason', 
                               'researchdata@b.e. (after browsing web site)', 'researchdata@b.e.', 
                               'researchdata@b.e', 'email to Rick from Jessica', 'email to Rick from Carla',
                               'email to Rick from Laura', 'email to Rick from Phuong', 'email to Rick from Sarah',
                               'Anna Sackman (RDM)', 'Email to Rick']],
    'cdl': ['California Digital Library', ['Joan Starr', 'Stephanie Simms', 
                                           'Daniella Lowenberg (DASH), via Quinn Dombrowski']],
    'ist': ['Information Services & Technology - API', ['Jennifer Bellenger', 'Jon Broshious', 'Ian Crew', 'Jon Hays',
                                                        'bConnected', 'Michael Leefers', 'Alex Walton', 
                                                        'referred by Ian (bConnected)', 
                                                        'referred to Rick by Jennifer Bellenger (bConnected)',
                                                        'Forwarded by Beth Muramoto (GSE) to Ian Crew (bConnected), who forwarded it in turn to researchdata@berkeley.edu',
                                                        'bconnected']],
    'micronet': ['Micronet', ['micronet', 'Micronet', 'micronet list', 'Micronet list']],
    'iao': ['Industry Alliances Office', ['Nicole Hensley', 'Nicole Hensley (IAO/IPIRA)', 'Nicole Hensley (IAO)',
                                         'email to Chris and Rick from Eric Giegerich',
                                         'email from Nicole Hensley to Rick and Chris',
                                         'Email from Nicole Hensley to Chris and to Rick']],
    'ssw': ['School of Social Welfare', ['David Fullmer']],
    'bids': ['Berkeley Institute for Data Science', ['BIDS']],
    'brdo': ['Berkeley Research Development Office (VCRO)', ['Barbara Ustanko via Chris Hoffman']],
    'lsit': ['Letters & Science IT', ['Michael Quan (Letters & Science IT)']],
    'ais': ['Academic Innovation Studio', ['AIS drop-in (handled by Rick)']],
    'musinf': ['Museum Informatics', ['BIDS Faire CSpace Portals poster']],
    'rit': ['Research IT', ['research-it@berkeley.edu']]
}

org_rollups = {
    'cchem': ['College of Chemistry', ['Department of Chemistry']],
    'ced': ['College of Environmental Design', ['City and Regional Planning', 'Department of City & Regional Planning', 'Landscape Architecture & Environmental Planning']],
    'citris':['Center for Information Technology Research in the Interest of Society', ['Center for Information Technology Research in the Interest of Society (CITRIS)']],
    'cnr': ['College of Natural Resources', ['College of Natural Resources (CNR)', 'Department of Agricultural & Resource Economics (ARE)',
                                             'Department of Environmental Science, Policy & Management (ESPM)',
                                             'Department of Plant and Microbial Biology']],
    'coe': ['College of Engineering', ['College of Engineering (CoE)','Department of Bioengineering',
                                       'Department of Civil and Environmental Engineering',
                                       'Department of Mechanical Engineering (ME)',
                                       'Department of Nuclear Engineering',
                                       'Division of Electrical Engineering/EECS',
                                       'Institute for Environmental Science and Engineering']],
    'dh':  ['Digital Humanities at Berkeley', ['Digital Humanities at Berkeley', 'Digital Humanities at Berkeley (DH)', 'Digital Humanities @ Berkeley']],
    'eslib':['Ethnic Studies Library', ['Ethnic Studies Library']],
    'gbsmrc':['Golden Bear Sleep and Mood Research Clinic', ['Golden Bear Sleep and Mood Research Clinic']],
    'gse': ['Graduate School of Education', ['Graduate School of Education (GSE)']],
    'gsj': ['Graduate School of Journalism', ['School of Journalism']],
    'haas':['Haas School of Business', ['Haas School of Business']],
    'intl':['International programs', ['International Computer Science Institute (ICSI)']],
    'ist': ['Information Services & Technology', ['Information Services & Technology (IST)']],
    'law': ['Berkeley Law', ['School of Law', 'Boalt Hall School of Law', 'Jurisprudence and Social Policy', 'Legal Studies Program']],
    'lib': ['Library', ['Bancroft Library', 'Bancroft Library - Oral History Center', 'C.V. Starr East Asian Library', 'Ethnic Studies Library', 'Library']],
    'ls':  ['College of Letters & Science - College-wide', ['College of Letters and Science (L&S)', 'D-Lab', 'Undergraduate Interdisciplinary Studies']],
    'lsa': ['College of Letters & Science - Arts & Humanities', ['Department of Music', 'Department of Near Eastern Studies', 'Department of History of Art']],
    'lsb': ['College of Letters & Science - Biological Sciences', 
                                            ['Department of Integrative Biology', 
                                             'Department of Molecular & Cell Biology',
                                             'Department of Molecular & Cell Biology (MCB)']],
    'lsm': ['College of Letters & Science - Math & Physical Sciences', 
                                            ['Department of Earth and Planetary Science (EPS)', 
                                             'Department of Physics', 'Department of Statistics']],
    'lss': ['College of Letters & Science - Social Sciences', 
                                            ['Department of Anthropology',
                                             'Department of Economics', 'Department of Geography', 'Department of History', 
                                             'Department of Political Science','Department of Psychology',
                                             'Department of Sociology']],
    'nat': ['National programs', ['Robert Wood Johnson Berkeley (Scholars in Health Policy Research Program)', 'Department of Economics / Robert Wood Johnson Berkeley (Scholars in Health Policy Research Program)']],
    'noid':['Not specified', ['Unknown value', 'unidentified', 'Unassigned', 'Unknown department', 'Unknown status', 'Unspecified', 'Unknown division']],
    'other':['Other', ['UCLA - Humanities CIO']],
    'qb3': ['California Institute for Quantitative Biosciences (QB3)', ['CIRM/QB3 Shared Stem Cell Facility and High-Throughput Screening Facility']],
    'sph': ['School of Public Health', ['School of Public Health', 'Division of Biostatistics/Public Health', 
                                        'UC Berkeley-UCSF Joint Medical Program']], 
    'ssw': ['School of Social Welfare', ['School of Social Welfare']],
    'tchi':['Terner Center for Housing Innovation', ['Terner Center for Housing Innovation']],
    'vcaf':['Vice Chancellor for Administration and Finance', ['Procurement Services - Supply Chain Management']],
    'vcr': ['Vice Chancellor for Research Office', ['Berkeley Institute for Data Science (BIDS)', 
                                                    'Berkeley Seismological Lab',
                                                    'Center for Effective Global Action (CEGA)',
                                                    'Center for Studies in Higher Education',
                                                    'Center for Race and Gender', 'Center for Study of Race and Gender',
                                                    'Haas Institute for a Fair & Inclusive Society',
                                                    'Human Evolution Research Center',
                                                    'Industry Alliances Office (Vice Chancellor for Research)',
                                                    'Institute of European Studies',
                                                    'Institute of Human Development', 
                                                    'Institute for Research on Labor and Employment (IRLE)', 
                                                    '(California Policy Lab)',
                                                    'Institute for the Study of Societal Issues',
                                                    'Institute of Transportation Studies (ITS)',
                                                    'Institute of Transportation Studies (ITS) - PATH',
                                                    'Phoebe A. Hearst Museum of Anthropology', 'Hearst Museum of Anthropology',
                                                    'UC Botanical Garden',
                                                    'University of California Transportation Center']],
    'vcue':['Vice Chancellor for Undergraduate Education', ['Berkeley Resource Center for Online Education (BRCOE)', 'Research IT']],
}

ls_rollup = {
    'lsall': ['College of Letters & Science - All', ['College of Letters & Science - College-wide', 
             'College of Letters & Science - Arts & Humanities', 'College of Letters & Science - Biological Sciences', 
             'College of Letters & Science - Math & Physical Sciences', 
             'College of Letters & Science - Social Sciences']]
}

labels = ['Unassigned', 'Unknown department', 'Unknown status', '',  '', '', 'Unspecified', 'Unknown division',
          'Consultation(s) without a partner',]

orig_headings = ['Consultants, number of consults', 'Departments Served, number of engagements',
            'Patron Status, number of patrons', 'RDM Lifecycle Category', 'Referrals In', 'Referrals Out',
            'Consultation Complexity', 'Library Division, number of engagements',
            'Organizational Partners, number of shared engagements' ]
mod_headings = ['School, College or Office', 'School, College or Office, with L&S combined'] # for copied values
all_headings = ['Consultants, number of consults', 'Departments Served, number of engagements',
            'Patron Status, number of patrons', 'RDM Lifecycle Category', 'Referrals In', 'Referrals Out',
            'Consultation Complexity', 'School, College or Office', 'School, College or Office, with L&S combined', 
            'Library Division, number of engagements',
            'Organizational Partners, number of shared engagements']
# List of dictionaries with modified values
mod_dicts = [pacounter, lscounter]