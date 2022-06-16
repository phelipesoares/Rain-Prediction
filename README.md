# Project Goals
This repository has a end-to-end Data Science project, about climate predictions. It's a particular project that I'm working just myself, to improve my engineering and data analysis-science skills. The main goal is to create a pipeline that make predictions and save those in a database near real time.

# Project Description
In resume, this project is split into this parts:
  - Env: Google Cloud Plataform
  - Data Source: API (Rapid API)
  - Tools: Python, Cloud Functions, Cloud Storage, BigQuery

![image](https://user-images.githubusercontent.com/69798348/115745736-1939a080-a36a-11eb-81f1-cbc88bcb3789.png)

# Documentation

# API:
This API bring the climate info about some region passed in the parameters. For example, if you pass "London", then you receive London Climate info, as Temp, Wind direction, kpm wind, sky condition, etc. The API refresh this info every 15 minutes, thus you have 4 registers per hour about the region you want.

# Starting the project:

At the beggining, we don't have any information about any region climate, so we need to collect and store the data in some database. To solve it, we create a VM Instance in Google Cloud Platform, where we gonna run our scripts and a database in Query, where we gonna store the data. Thus, at this moment, every 15 minutes my scripts runs, collect the data from API, transform and insert into BigQuery table. At some point, we gonna have thousands of registers then we be able to create our predictions models.

# Where we are and what we're doing:
  # 22/04/2021
  This is the first day of collecting data from the API. We're collecting data from a city in Brazil, Carapicuiba, every 15 minute and storing into a BigQuery Table.
  
  # Next days:
  1) Include another cities, as Barueri, Carapicuiba and Sao Paulo, because their next to each other.
  2) Include a automation that sends a signal if the script doesn't finish the job, so we can know if the table has been updated.
  3) Wait for at least 50.000 records, then we can create prediction models with this dataset.

# 12/07/2021
We create a dashboard to see api working in real time and while we are filling our database I'm learning docker and luigi concepts to create our pipeline to put the algorithm in production once it's done.

Dashboard link - https://datastudio.google.com/s/p268nZ5P8DM (Ps: This dash has a default date filter, it always bring the last 14 days. It can be changed by clicking on filter box)

# Thanks!
I hope we can update this repository soon!
