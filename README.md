# rdm_metrics
Scripts for cleaning, counting, displaying, etc. Research Data Management program metrics

After May 4, 2016, please use the Python script, RDM_metrics_genericized.py. It takes two arguments: 

• The first argument points at a .csv file exported from the RDM Drupal site (contact Rick or Jamie for details)
• The second provides the text that describes the period that the report covers.

To run, download or clone the script to your local machine, and (in your terminal or shell, etc.) navigate to the folder that contains the script. Locate the path to the .csv file and enter:

     python RDM_metrics_genericized.py {csv file name} {report period descriptor}

For example:
     python RDM_metrics_genericized.py /path/to/file/RDMConsulting_Ricks_view_FY2015-16_Q3_2016-05-04T17-15-48.csv FY2015-16_Q3

(no line break)

This will run the script on the file RDMConsulting_Ricks_view_FY2015-16_Q3_2016-05-04T17-15-48.csv. The ouptut will include a line that reads:

     In FY2015-16_Q3, RDM Consulting provided {x} consultations.
     We reached a successful resolution in {y} of those engagements.

(The text 'FY2015-16_Q3' comes directly from the second argument supplied.)

Contact Rick or Jamie for information on how to download the CSV file.




