# rdm_metrics
Scripts for cleaning, counting, displaying, etc. Research Data Management program metrics based on data compiled in the Google Sheet "Research IT Consulting Engagement Log."


RUNNING THE SCRIPT

After October 2017, please use the Jupyter Notebook RDM_metrics_FROM-RIT-Consulting-Engagement-Log.ipynb or the Python script RDM_metrics_FROM-RIT-Consulting-Engagement-Log.py. The Jupyter Notebook has a cell that contains the required five arguments and another that holds the dictionary configuration. The Python script takes five arguments on the command line and gets its dictionary configuration from the file config_v3.py. Both versions operate on a .csv file exported from the Google Sheet "Research IT Consulting Engagements Log." Contact Rick or Amy for information on how to download the CSV file.

NOTE that the two versions are not always in sync...most development gets done in one version (these days, typically, the Jupyter Notebook) and ported to the other.

The Python script takes five arguments: 

• The first argument provides the path to the .csv file, stored locally on your computer.

• The second provides the filename itself. 

• The third provides the text that describes the period that the report covers.

• The fourth provides the earliest consultation start date that the script will include.

• The fifth provides the latest consultation state date that the script will include.

In the Jupyter Notebook, these can be entered manually or read from a file using the %load cell magic. Loading from a file allows you to save the parameters for later review and reuse. We've stored our files in a folder called Metrics_args.

To run the Jupyter Notebook: download or clone the notebook to your local machine. Locate the .csv file and enter the required arguments in the appropriate cell. If you elect to store the arguments in a file, uncomment the line that begins '%load' and add the filename including the path, relative to the notebook. (The existing argument values will be overwritten.) 

To run the script: download or clone the script and the configuration file to the same folder on your local machine, and (in your terminal or shell, etc.) navigate to the folder that contains them. Locate the path to the .csv file and enter:

     python RDM_metrics_FROM-RIT-Consulting-Engagement-Log.py {csv filepath} {csv name} {report period descriptor, in double quotes} {report start date, in YYYY-MM-DD format} {report end date, in YYYY-MM-DD format}

For example:

     python RDM_metrics_FROM-RIT-Consulting-Engagement-Log.py path/to/file/Research-IT-Consulting-Engagements-Log_20171019_1544PDT.csv "the first quarter of FY 2017-2018 (July 1 through September 30, 2017)" 2017-07-01 2017-09-30
	 
This will run the script on the file Research-IT-Consulting-Engagements-Log_20171019_1544PDT.csv. The ouptut will include a line that reads:

     In the first quarter of FY 2017-2018 (July 1 through September 30, 2017), RDM Consulting provided {x} consultations.
     We reached a successful resolution in {y} of those engagements.

(The text 'the first quarter of FY 2017-2018 (July 1 through September 30, 2017)' comes directly from the third argument supplied.)

CONFIGURATION UPDATES

Values for Referrals In and Referrals Out group a number of individuals into categories: RDM Consulting, Berkeley Research Computing, The Library, D-Lab, etc. In the notebook, there is a cell that associates individual names with each organization. For example:

    'css': ['Campus Shared Services - IT', ['Brett Larsen', 'Daniel Bass', 'Johnathon Kogelman', 'CSS-IT']],

The lefthand-most value (e.g., 'css') is the key for that dictionary entry. The value for each key is a nested list. The first item in the list (e.g., 'Campus Shared Services - IT') is the text that displays in the output; the second item is a list containing names associated with each organization. These could be individuals or terms used during data entry to refer to the unit (e.g., 'Brett Larsen', 'Daniel Bass', 'Johnathon Kogelman', 'CSS-IT').

The script imports this dictionary from a file named config_v3.py.
 
We need to update the lists that comprise the dictionary as new people refer cases to us or we refer cases to people for the first time. The file config_v3.py is version-controlled in GitHub at:

    https://github.com/rjaffe/rdm_metrics.

All changes should be submitted as pull-requests to that repository.

PLEASE pay attention to syntax - quotes, commas, and especially trailing commas! - when updating the configuration.

Note that the configuration cell/file also includes display text for empty values in a number of fields and headings for the various categories in the output report. These shouldn't change very often.

===

