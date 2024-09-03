## Social-Media-ELT-Pipeline

This is currently in progress and I wrote the timeline, but not the dates since I'm still figuring out my schedule and time it takes to compelete the tasks. I hope for this project to be a more practical pipeline that follows logic and reasoning the regular Data Engineers use.

### Pipeline Purpose: What is the primary goal of your pipeline? Is it for strategy development, risk management, backtesting, or a combination of these?

This pipeline is based on extracting information from social media in real time to get a idea of trending topics, get sentiment of certain topics, and detect spam from these platforms. The main goal of this is to make a system which updates data in real time for use in querying.

Python is used for everything just to test everything out. If using real time Java should be used since it has better performance and latency compared to Python.

### Data Sources: What kind of data are you using (e.g., market data, fundamental data, alternative data)? Are your data sources reliable and consistent?

Currently to simplify pipelines and focus more on checking if this system works as expected, I will use reddit data using the PRAW API to fetch data. This is reliable and consistent, but due to rate limits that I currently have, cause an issue with not making this fully real time right now. 

### Data Cleaning and Processing: How are you handling data cleaning, preprocessing, and feature engineering? Are there any potential data quality issues or biases?

Currently data quality issues might exist due to taking any data that is put on reddit and scraped through the api. To check quality would mean to go more in depth in spam detection algorithms and other algorithms to check quality, but is not the main focus of this project.

Other data used for indexing is tracking the subreddit or keywords in posts,comments etc to index later on properly. This is also a new feature.

Data quality can cause bias. The other issue is what subreddits I scrape. Leaving out subreddits can cause bias, however this project is mainly to get the pipeline made, so I will focus less on this.

The data itself will also have a timestamp on when it was added to the Hbase. This is different from kafka logging because the data will constantly be updated. Kafka can log its updates, but each comment might come in Hbase at a different time. 

### Model Development: What types of models are you using (e.g., statistical models, machine learning algorithms)? How are you evaluating model performance and selecting the best candidates?

The main part of this pipeline is to ensure real time updates and availability of these updates to use. As data comes in constantly, we are introduced to new text data in these posts. To see real-time analysis more, I thought it would be good to use sentiment analysis algorithms and add a field to the text data as a feature in the file to show how fast it's being updated and how  fast transformations are happening.


Backtesting and Validation: What backtesting methodology are you using? How are you addressing look-ahead bias and survivorship bias? 

Logging: Logging is checked to latency and makes sure errors don’t occur that much. Logs in scripts have error checking to make sure this works.

Apache Nifi: Used to track the whole pipelines as a whole instead of logging which has more modularity.

Risk Management: What risk factors are you considering? How are you measuring and managing risk?

Errors in changes in API or scripts(beautifulsoup scraping): This has occurred to me before where a website can change some format in newer data. and the whole script can stop working because of this. This is the reason why APIs and scripts must have modularity and error checks. Logging also tracks this fast and notifies users that this has occurred to make sure scripts are updated.

API Limits: This is runned in batches to make sure that I have API limits met. If you have real-time through paying for access, you should still have error implementation in logging implemented. 

### Technology Stack: What tools and technologies are you using for data ingestion, processing, model development, and deployment?
### The overall technologies in this pipeline is:


Apache HBase: Apache HBase is good for read/write in real time which makes it good for social media data. For reddit data, it is good in updating post files for more comments, replies and other metadata. It’s also very good with scaling, managing large datasets, and interacting with the Hadoop ecosystem. 


Apache Spark Streaming: This is used for the pipeline in order to apply ML to the data and write back to the Hbase file. This will take raw data, find relevant data, and then apply ML I am also taking in data from this which has worse latency compared to Flink since Flink is better used. This is only because API I have has rate limits already and already introduces latency. If you add other sources or api with streaming capabilities like twitter, flink is better used.

Apache Kafka: This is used for taking in data and logging in incoming data, transformations, feature engineering, and updates.

Apache Hive: This is used because you typically want to analyze over a certain period of time. After that you should store somewhere else. This is used for historical analysis. Older data might still have updates however so it's best not to store it in a data lake or HDFS where edits can’t be made. Data lakes are made for appending or keeping raw data and not one with updates. Infrequent updates can work, but in this data it’s hard to tell. Hive consumes less resources than HBase making it a good place to use less resources and also keep updates from happening. You can use this for historical analysis that mainly does not need much real-time analysis and can take delay in latency. Something to keep in mind is that algorithms or queries that use this for historical analysis must have a filtering for timeframes to avoid lookahead biases by using data that is updated in previous analysis. 

Apache Solr: This is built on top of HBase to have text query search on HBase and incoming data that comes in. It is also good with indexing and more flexible making it good for searching within HBase to make up for HBase CRUD operations. The thing is Solr is more complicated and requires more programming to make sure indexes are optimized for performance. It’s also that you can’t get much real-time when text searching, but can get near-real-time if you keep short intervals that solr uses to take in data in batch and index. This is best used in cases when you can tolerate some latency in this as this is large data. Solr takes in data in batches so we can’t avoid this limitation.

Apache NiFi: This is used for monitoring the pipelines and checking dependencies and script monitoring. This is good for real time so this is why it’s used.

Elasticsearch: This is used for log monitoring. You can do this in Solr too, but because this is better in real time compared to Solr, Its better in logging in real time when you have to track errors and get to the reason why something happened fast. 

Solr vs Elasticsearch: If using elasticsearch you have to duplicate data if storing in HBase and elasticsearch while Solr builds on top of HBase and HDFS in general. Elasticsearch is better in real time and indexing. It is also easier to use compared to Solr. Solr does in batch which is not optimized for real time since you can achieve near real time. Elasticsearch has autoindexing while Solr needs optimizations and more manual configurations. Elasticsearch is not optimized for constant write/updates which HBase is for which is why I'm only using elastic search for log data which is mainly appended while reddit data and other sources can update very fast. HBase also scales better.

Amazon S3: This is good for Append only data and not updates. Since Logs don’t update, we will regularly roll out previous logs so elasticsearch can have the most recent data and relevant queries. Since other data is still being updated, other data isn’t stored unless you have other data that is not updated much. Log data should be compressed

Compression: I am getting raw data from API and will compress it in an ORC or Parquet format to be read optimized to make sure ML and other transformations run quickly. Same goes with queries.

Other Databases: I can use MongoDB to store this data too, but HBase is more optimized for read/write in real time since MongoDB takes in semi-structured and unstructured data. Since we also have an idea on the data, we can use HBase better since it scales better in very large data sizes that can possibly be used for analysis.

Synchronization: If using other databases, its hard to synchronize, that is why Hadoop is mainly used. Synchronization will also be checked between Hive and HBase. If other databases are used, this does need to be implemented.

Consistency: HBase is good consistency and when introducing other databases, you have to make sure its consistent. Other databases might be more optimized for availability which can also cause issues when synchronizing data between different databases. This is also why I used HBase

Kappa Architecture: There is a different process in batch processing with Hive which is historical data updated and different interval while real time is in HBase and processed at much faster intervals. This is then synchronized. This is Kappa architecture and much more complex to manage. Depending on use case, this can be good or bad since Hadoop requires more manual configuration compared to other easy to use databases like MongoDB or Elasticsearch.

CAP Theorem: This is mainly Partition since big data is used and needs to be processed fast. HBase and Hive both have consistency so this is also used mainly if consistent data is needed. 

Transformations and Parallel Processing: Transformations are made in separate scripts and given modularity because you can parallelize to transform and add features to make this faster if needed. I don’t parallelize but this is an option.

Indexing: Solr is good with indexing, but does not auto create indexes. Since Reddit is more structured with API it might be better to have scripts to make indexes dynamically or based on subreddits to query effectively. 

Batch/Streaming: Hive is good for updates but not real time. In cases with batch processing, data warehouses like Hive are good with this. Historical data is viewed less and should be updated less frequently and in batches. Hive is more for recent data that needs constant data analysis and accurate data in real time. This uses a more real time script. This is important to make sure you save costs when running scripts.

ETL/ELT: I use an ELT because the raw data loaded in from reddit or other platforms can be used for other purposes. You might have other cases than querying text data that need to be ran or analyzed so loading first and transforming(has some latency) is better. ELT is good in cases where dependencies need to be checked. This is better in cases like Hive where schemas are predefined and need to be checked before loading it in.


### Scalability: How well does your pipeline scale to handle large datasets and frequent updates?

This scales very well because of HBase,Hive, and HDFS and data lakes being very good with scaling. They use horizontal scaling so adding more nodes is needed if you get more data.

### Automation: Have you considered automating any parts of the pipeline to improve efficiency and reduce manual errors?

Most of this is automated using scripts with logging and nifi used to track errors


### Documentation: How well is your pipeline documented, including code, data sources, and methodologies?

This is current documentation and plan with code being made and documented later. This is very important considering how complex this pipeline is.

### Current Plan:

Download all required technologies.

Make Scripts to get incoming Data with kafka to check logging, data upload, and error checking

Make Script to transition old log data to s3

Make Scripts for Data Transformations(preprocessing) through kafka 

Make Scripts for ML related feature engineering through Spark Streaming

Make a Solr indexing script for data in HBase

Make Solr Query scripts and test them

Use Apache Nifi to track pipeline

Make Script to transition old social media data to Hive.

Make Hive Query Scripts



### Future considerations:

Better scripts in Java(speed)

More Api to add more data

More Solr Queries

More ML/Transformations in data for analysis.

Performance Testing

Subreddit data ingestion(rate limit not considered)

