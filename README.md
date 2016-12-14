# Squeaky-Wheel    
Automatically run speed tests and tweet @ your ISP if they are garbage.  
### Overview:  
Python Script that utilizes selenium web driver to scrape speed test results and  
tweet them at your ISP if they are below a given value.  
###### This script compiles and logs:  
* Download Speed in Mbps  
* Upload Speed in Mbps  
* Latency in msec  
* Jitter in msec  

#### [MLab (Measurement Lab)](http://www.measurementlab.net/) is used for the speedtest.  
##### It's the same test that Google is using in its new native speedtest feature:  

![Google Test](https://s24.postimg.org/vdhuc51p1/image.png)  

The MLab's test is located @ http://www.measurementlab.net/tools/ndt/ ,  
but the data is scraped from http://www.measurementlab.net/p/ndt-ws.html  
because the test is served up through an iframe.  

The [Tweepy](http://www.tweepy.org/) Library is used to access the twitter API.  
You will need your own API keys and access tokens from https://dev.twitter.com/.   

#### Sample Output:   
![Sample Tweet](https://s23.postimg.org/hv52aukjv/image.png)  

### Setup:  
##### Dependencies:  
`Selenium`  
`geckodriver`  
`Tweepy`  

##### Config:  
Config options can be set in **config.json**:  

###### Bandwidth  
Set "download" to the download speed you are supposed to get (in Mbps).  
Set "upload" to the upload speed you are supposed to get (in Mbps).  
###### Twitter
Put in your Twitter API keys and Access tokens in the "twitter" section.  
###### Margin  
The margin sets how much leeway there is for normal fluxuation.  
Example: a margin of ".5" triggers an exception and tweet if speeds dip  
below 50% of promised speeds (".6" == 60%, etc).  
**Must be between 0 and 1**.
###### ISP:  
Set "isp" to your ISP's twitter handle.  

| ISP | Twitter Handle |  
| --- | --- |   
| Comcast | @comcast |  
| Comcast Support | @comcastcares |  
| Spectrum / Time Warner |  @GetSpectrum |  
| Verizon Fios | @verizonfios |  
| Verizon Support | @VerizonSupport |  
| AT&T | @ATT |  
| AT&T Support | @ATTCares |  
| CenturyLink | @CenturyLink |  
| CenturyLink Support | @CenturyLinkHelp |  
| Cox Communications | @CoxComm |  
| Cox Support | @CoxCommHelp |  
| Frontier | @FrontierCorp |  
###### Log:  
Change the name / location of the .log file. Default location is local directory  
###### Selenium Driver
Change the driver type to one of either 'chrome' or 'firefox'.  Leaving
 empty or not set will use Firefox.  If Firefox is not installed in the
 expected location, set the driver binary to the full path to the
 Firefox executable.  Ex `C:\Program Files (x86)\Mozilla Firefox\Firefox.exe`

 You must have installed the proper driver. See the [downloads section here](http://www.seleniumhq.org/download/)
## Usage:  
`python3 ~/squeaky-wheel.py`  

Set it as a cron job to run every x minutes/ hours:  
`0,30 * * * * python3 ~/squeaky-wheel.py`  

## Support:  
Drop me a line - mrbenpappas@gmail.com  
Or visit my [site](http://mrbenpappas.com)  
## License:  
##### The MIT License (MIT)  
