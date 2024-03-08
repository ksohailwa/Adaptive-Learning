
### Adaptive Learning
<img src="assets/ibm_logo.png" width="100">


"Adaptive Learning" is a web application that

 a) recommends the best type of learning material to the user based on the data they submit about themselves and

 b) provides visualizations that show
      - preferred way of asking help based on different selectable user attributes
      - personal evaluation of effectiveness of learning platforms based on different selectable user attributes
      - distribution of user (in percent) based on different selectable user attributes

This project was submitted by the Data Detectives group for the Learning Analytics course at the <a href="https://www.uni-due.de/en/index.php">University of Duisburg-Essen</a>.



### Dataset Description

 * data from own Google Survey with 22 Questions and 70+ participants (anonymized)
 * the results were stored in an SQL database

You can access and participate in the survey by clicking this <a href="https://docs.google.com/forms/d/e/1FAIpQLSd31k__bA9LBGXkNk2o7dfdR6-4crZceVpVKv3jm3JAhQ7L6Q/viewform">link</a> 

### Implementation Technologies

**Frontend**
  + Website
    + Dash
  + Visualization
    + Plotly

**Backend**
  + Web Server
    + Python
    + Dash
    + Plotly
  + Machine Learning
    + Scikit Learn
  + Recommender System
    + Case Recommender
  + Database
    + Azure SQL Database Server

### App Structure

 * //wait for professors's answer if we need to change it or not//

### Machine Learning

 * Clustering Existing Users
    + Algorithm: KMeans
    + Needed Libraries: sklearn, pandas
 * Classifying New User
    + Algorithm: KMeans
    + Needed Libraries: sklearn, pandas 
 * Recommendation
    + Algorithm: ItemKNN
    + Needed Libraries: caserec, pandas


  

### Web structure preparation (index.py)

"index.py" is the main file for our backend server using "Dash" python framework. The server starts by rendering the Home Page on http://127.0.0.1:8050/.


### Visualization

All visualizations were built using <a href="https://plotly.com/">Plotly</a>.


### Deployment

To be able to deploy our application you need to install the following requirements:

 * python==3.8
 * pandas==2.1.3
 * plotly==5.18.0
 * dash==2.14.2
 * dash-mantine-components==0.10.2
 * dash-iconify==0.1.2
 * SQLAlchemy==2.0.25
 * dash-html-components==2.0.0
 * dash-bootstrap-components==1.5.0
 * dash-core-components==2.0.0
 * scikit-learn==1.3.2
 * caserecommender==1.1.1


There are 2 ways to install the dependencies with the specific versions we used in implementing this web application:

 1. Using pip package manager command
```ruby
pip install -r requirements.txt
```

 2. Using conda environment.yml file



### Run Server

 - Write "python index.py" in the terminal
 - Access http://127.0.0.1:8050/ on your browser










