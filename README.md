
### Adaptive Learning

"Adaptive Learning" is a web application that

 a) recommends the best type of learning material to the user based on the data they submit about themselves and

 b) provides visualizations that show
      - preferred way of asking help based on different selectable user attributes
      - personal evaluation of effectiveness of learning platforms based on different selectable user attributes
      - distribution of user (in percent) based on different selectable user attributes

This project was submitted for the Learning Analytics course at the University of Duisburg-Essen.


### Dataset Description

 * data from own Google Survey with 22 Questions and 70+ participants (anonymized)
 * the results were stored in an SQL database 


### Implementation Technologies

 * Frontend
  + Website
    + Dash
    + 
    + 
  + Visualization
    + Plotly
 * Backend
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

 * Clustering
    + Algorithm: KMeans
    + Needed Libraries: sklearn, pandas
 * Recommendation
    + Algorithm:
    + Needed Libraries: caserec, 

### Web structure preparation (index.py)

"index.py" is the main file for our backend server using "Dash" python framework. The server starts by rendering the Home Page on http://localhost:5000/.


### Visualization

All visualizations were built using Plotly


### Deployment

You can deploy our application locally by following these steps:

 1. Install python, plotly, dash,
 2. 


### Run Server

 - Write "python index.py" in the terminal
 - Access http://127.0.0.1:8050/ on your browser










