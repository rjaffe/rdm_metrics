# rdm_metrics
Scripts for cleaning, counting, displaying, etc. Research Data Management program metrics

*>>> NOW IN 'BETA': Script with selectable report begin- and end-dates. See below for details.*


RUNNING THE SCRIPT

After May 4, 2016, please use the Python script RDM_metrics_genericized.py and the configuration file config_v2.py. The script operates on a .csv file exported from the RDM Drupal knowledge Base. Contact Rick or Jamie for information on how to download the CSV file.

The Python script takes two arguments: 

• The first argument points to the .csv file, stored locally on your computer
• The second provides the text that describes the period that the report covers.

To run: download or clone the script and the configuration file to the same folder on your local machine, and (in your terminal or shell, etc.) navigate to the folder that contains them. Locate the path to the .csv file and enter:

     python RDM_metrics_genericized.py {csv filepath and name} {report period descriptor}

For example:

     python RDM_metrics_genericized.py /path/to/file/RDMConsulting_Ricks_view_FY2015-16_Q3_2016-05-04T17-15-48.csv FY2015-16_Q3

This will run the script on the file RDMConsulting_Ricks_view_FY2015-16_Q3_2016-05-04T17-15-48.csv. The ouptut will include a line that reads:

     In FY2015-16_Q3, RDM Consulting provided {x} consultations.
     We reached a successful resolution in {y} of those engagements.

(The text 'FY2015-16_Q3' comes directly from the second argument supplied.)

CONFIGURATION UPDATES

Values for Referrals In and Referrals Out group a number of individuals into categories: RDM Consulting, Berkeley Research Computing, The Library, D-Lab, etc. The file config_v2.py contains a dictionary that associates individual names with each organization. For example:

    'css': ['Campus Shared Services - IT', ['Brett Larsen', 'Daniel Bass', 'Johnathon Kogelman', 'CSS-IT']],

The lefthand-most value (e.g., 'css') is the key for that dictionary entry. The value for each key is a nested list. The first item in the list (e.g., 'Campus Shared Services - IT') is the text that displays in the output; the second item is a list containing names associated with each organization. These could be individuals or terms used during data entry to refer to the unit (e.g., 'Brett Larsen', 'Daniel Bass', 'Johnathon Kogelman', 'CSS-IT').

We need to update the lists that comprise the dictionary as new people refer cases to us or we refer cases to people for the first time. The file config_v2.py is version-controlled in GitHub at:

    https://github.com/rjaffe/rdm_metrics.

All changes should be submitted as pull-requests to that repository.

PLEASE pay attention to syntax - quotes, commas, and especially trailing commas! - when updating the configuration.


===

SELECTABLE REPORT DATES  *NOW IN BETA*

To set arbitrary report begin- and end-dates, use the Python script RDM_metrics_selectable_period.py and the configuration file config_v2.py. The script operates on a .csv file exported from the RDM Drupal knowledge Base that contains data on every consultation in the data base. (The earliest engagement began September 23, 2015.) Contact Rick or Jamie for information on how to download the CSV file.

The Python script requires four arguments: 

• The first argument points to the .csv file, stored locally on your computer
• The second provides the text that describes the period that the report covers. Double-quote text that contains spaces, e.g. "April - June 2016".
• The third is the report begin-date in the format YYYY-MM-DD
• The final argument is the report end-date in the format YYYY-MM-DD

To run: download or clone the script and the configuration file to the same folder on your local machine, and (in your terminal or shell, etc.) navigate to the folder that contains them. Locate the path to the .csv file and enter:

     python RDM_metrics_selectable_period.py {csv filepath and name} {report period descriptor} {report begin-date} {report end-date}

For example:

     python RDM_metrics_selectable_period.py /path/to/file/RDMConsulting_metrics-export_2016-09-24T13-45-51.csv FY2015-16_Q4 2016-04-01 2016-06-30

For a more human-readible description,  you could substitute "April - June 2016" above. Don't forget to double-quote text that includes spaces! 

This will run the script on the file RDMConsulting_metrics-export_2016-09-24T13-45-51.csv. The ouptut will include a line that reads:

     In FY2015-16_Q4, RDM Consulting provided {x} consultations.
     We reached a successful resolution in {y} of those engagements.

(The text 'FY2015-16_Q4' comes directly from the second argument supplied.)

Only those consulting engagements beginning between April 1, 2016 and June 30, 2016 will be tabulated.