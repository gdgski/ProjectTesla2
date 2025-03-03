# Tesla Group Work
Welcome to our statistical analysis of Tesla's stock prices for the last 10 years. The project can be divided into the following categories: 
1. Initial cleaning of CSV file:  
   2. Assessed how many NaN values were present, after determining that less than 5% of all rows consisted of NaN values we decided to remove these values as the overall dataset would still maintain its validity. 
3. Loaded cleaned CSV file into MySQL and MongoDB databases:
   4. For MySQL our code reads each line in the cleaned CSV file and inserts each row into the database
   5. For MongoDB we developped a code that would read each line in the cleaned CSV file and stored each line of data as a dictionary which was then to a list containing the entirety of the data. The list was then inserted using an insert_many in order to optimise performance.
6. Conducted data analysis using pandas and matplotlib:
   7. Utilizing Pandas to initially create a dataframe of the first 700 rows in the cleaned CSV file, we added various metrics to our analysis including average daily trading volume (ADTV) and standard deviation of average dailty trading volume (ADTVSTD). Both of these metrics were manipulated to take into consideration different timeframes. All results were plotted into their respective graphs in order to make trend analysis more evident. 
8. Creation of Web App in HTML:
   9. Due to our lack of proficiency in HTML we leveraged various AI in order to facilitate the creation of the website. The website's homepage consists of various Tesla models. We also incorporated the possiblity to visualize the cleaned CSV data, giving the user the ability to specify for which date they would like to visualize. We added two pages showing the graphs that were developed in Phase 3. 
      