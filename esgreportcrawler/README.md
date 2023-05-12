# ESG Report Crawler

Purpose of this code is to crawl `ESG reports` publicly available online and populate a a database. 

We leverage `Google Dorks` and the text based browser `lynx` to allow us to sidestep some of the bot detecting techniques. By adding a `sleep` time of 180seconds between queries we hope to avoid triggering bot detection. We sample from a list of 149 companies provided in the _companies.csv_ file. A sample _dork_ for our ESG data looks as follows:

```
site:Foods,venturafoods.com^M ext:pdf OR ext:pptx OR ext:ppt intitle:ESG OR intitle:CSR OR intitle:Sustainability OR intitle:"Impact Report" OR intitle:"responsibility report" OR intitle:(Sustainability reporting|Corporate responsibility reporting|Environmental reporting|Social reporting|Governance reporting|Responsible investing|Ethical investing|Green investing|ESG disclosure|ESG performanc      e|ESG metrics|ESG ratings|ESG analysis|ESG integration|ESG criteria)
```
<br>
Temporary location for ESG reports currently are saved to [google drive](https://drive.google.com/drive/folders/1kMDQ8xlPyx4_-JsBc-3DE0OrBDxVOYOc?usp=share_link). Final list of esg reports will be saved to [s3 bucket](https://s3.console.aws.amazon.com/s3/buckets/esgreportswebcrawl?region=us-east-2&prefix=esgreports/reports/&showversions=false)
<br>
To run

1. Navigate to terminal
2. run ` git clone git@github.com:ecocrumb/esgreportcrawler.git && cd esgreportcrawler`
3. from dir run `./esgcrawler3.sh`
4. Verify log file `query.log` for normal behavior. 
5. Inspect `reports/` dir for output of crawl

*Note*: First iteration at this crawler. Early observations
- Google Dorks cap at 32 tokens. Further refinement needed
- 443 errors 
