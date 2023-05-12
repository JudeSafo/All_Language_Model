[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/569/badge)](https://bestpractices.coreinfrastructure.org/projects/569)<br>

# ESG Report Database
We have set up a `MongoDB` database for storing and accessing *ESG Report* data for the 100+ companies we are tracking. Mongodb is a 3rd party client affiliated with our `AWS` cloud account.  
Here are the instructions on how to access it for the first time, including information on _credentials_, _basic queries_, and the _data schema_. You should have received an email from `@mongodb.com` providing you with user credentials. Please follow the steps below to get started:
![image](https://user-images.githubusercontent.com/9307673/232570287-09f75b52-1725-414d-8a2b-e0751f319570.png)

### Background

There are 126 companies and 748 esg reports total in our database.<br>
Each company folder contains:
1. **PDFs**: Anywhere from 1 to 9 _ESG reports_ per company in 'pdf' format (e.g. 'Environmental Report', 'CSR Report', "Impact Report")
2. **Plaintext**: A `plaintext` file for each `pdf` file that can be read into the 
3. **Topics**: For each report grab from a predefined list of topics most relevant for our analysis
4. **Parser**: Using the topics, slice the report into the sections pertaining to each topic.
### Install a MongoDB client:

You will need a MongoDB client to connect to our database. You can either use the _MongoDB shell_ (https://www.mongodb.com/try/download/shell) or a GUI like MongoDB Compass (https://www.mongodb.com/try/download/compass). If you prefer direct access via _command line_ (On Mac) simply navigate to terminal, enter `brew install mongosh` and follow prompts.

### Access credentials:

You should get these credentials from your email invitation to your `<your_name>@ecocrumb.app` email<br>
(For now I've provided my own credentials below)

```
Username: jude
Password: pcm2ZrCtL3NJgImC
```
Please keep this information secure and do not share it with unauthorized individuals.<br>
**Note:** (If your connection times out try adding your 'IP address' to the list of know IP's)

### Connection details: 
![image](https://user-images.githubusercontent.com/9307673/232186331-6181fd7a-5738-4a4c-9587-3e292085a979.png)

To connect to our database, use the following connection string for your MongoDB client:

```ruby
mongodb+srv://[username]:[password]@esgcluster.cqfz8.mongodb.net/esgCompanyData?retryWrites=true&w=majority
```
Replace [username], [password] with the appropriate values.

## Basic queries:

Once connected, you can run some basic queries to explore our data:

### List all companies in the database:

```sql
show collections
```
which should return  
```bash
Atlas atlas-d7qm9l-shard-0 [primary] esgCompanyData> show collections
Acme_Smoked_Fish_Corp
Acushnet_Holdings
ADM
Ag_Processing_Inc
Agropur
Albertsons
Altria_Group
American_Crystal_Sugar_Company
American_Seafoods
Andersons
Archer_Daniels_Midland
ASR_Group
...
```
### List all esg reports
To list the esg reports within a given company you can run the following query to list the report names within a specific company:
```sql
db.collection_name.find({}, { "document_name": 1, _id: 0 }).pretty();
```
This query will return the esg report names in the specified company without displaying the _id field.

For example, if you want to list the esg report names in a company called "ADM", run the following command:

```sql
db.ADM.find({}, { "document_name": 1, _id: 0 }).pretty();
```
you should expect the following
![image](https://user-images.githubusercontent.com/9307673/232187440-d15d8af2-dcf9-4db2-8203-b9fb88891995.png)

To query and return a specific company and esg report in our database, you can use the `find()` method with a filter. To query "ADM" and retrieve document titled "OUR_SUSTAINABILITY_JOURNEY_topics_features" run the following query:
```sql
db.ADM.find({ "document_name": "OUR_SUSTAINABILITY_JOURNEY_topics_features" });

```
which returns
```
Atlas atlas-d7qm9l-shard-0 [primary] esgCompanyData>
...
'Value of Sustainable Innovation ': [
      'range sustainable',
      '2015 sustainable soy',
      'drive value industrial',
      'produce sustainable rapeseed',
      'gmo quality sustainable',
      'value growing responsibly',
      'assurance throughout value',
      'council sustainable',
      'global value chain',
      'throughout value chain',
      'adopt sustainable',
      'promoting sustainable',
      'trade sustainable',
      'innovation efficiency',
      'value differences'
    ],
    document_name: 'OUR_SUSTAINABILITY_JOURNEY_topics_features'
  }
]
```
### List the relevant `topics` across all documents for a given company
```sql
db.ADM.find({ "document_name": { $regex: /_topics_features$/ } });
```
for which you should expect

```mongodb
Atlas atlas-d7qm9l-shard-0 [primary] esgCompanyData> db.ADM.find({ "document_name": { $regex: /_topics_features$/ } });
      ...
      'waste value added',
      'practices sustainable',
      'sustainable agricultural',
      'overview technology innovation',
      'undergone create value'
    ],
    document_name: 'Transforming_the_way_we_do_business_topics_features'
  }
```
...

### Find esg report containing the key "Tax Transparency" in the company "ADM":
```bash
db.ADM.find({ "Tax Transparency": { $exists: true } }, { "Tax Transparency": 1, _id: 0 });
```
### Aggregate values for the key "Tax Transparency" in the "collection_name" company and include the esg report name:

```sql
db.ADM.aggregate([
  {
    $group: {
      _id: null,
      tax_transparency: {
        $addToSet: {
          value: "$Tax Transparency",
          document_name: "$document_name"
        }
      }
    }
  }
]);
```

## Data schema:

Our data is stored in a JSON-like format called BSON. Each document (report) in a collection (company) may have different fields (keys) and their respective values. Here's an example of the document structure in our database:

```bash
{
  "_id": ObjectId("..."),
  "document_name": "example_document",
  "Tax Transparency": [...],
  "Resource Use and Circularity": [...],
  ...
}
```
The "_id" field is automatically generated by MongoDB for each document, and the "document_name" field identifies the original JSON file's name. Other fields represent the keys and their respective values from the JSON data.

## Conclusion
If you have any questions or need assistance with accessing our MongoDB database, please don't hesitate to reach out to [jude@ecocrumb.com](jude@ecocrumb.com). Let's make the most out of our data!

*Note*: You can also view these documents via our aws [s3 bucket](https://s3.console.aws.amazon.com/s3/buckets/esgreportswebcrawl?region=us-east-2&prefix=esgreports/reports/&showversions=false) here
