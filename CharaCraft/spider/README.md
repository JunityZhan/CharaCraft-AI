## Examples
When the target website is static, you can use the following command to crawl the website:
```bash
python run_spider.py --urls https://example.com/ --depths 0
```
Write urls after --urls, and write depths after --depths. The number of urls and depths should be the same. The above command will crawl the website and save the crawled data in the data folder. The data folder will be created automatically if it does not exist.

You may also assign multiple urls and depths to crawl multiple websites at the same time:
```bash
python run_spider.py --urls https://example.com/ https://www.wikipedia.org/ --depths 0 0 # You must assign depths with the same number of urls
```

When the target website is dynamic, you can assign --dynamic to crawl the website:
```bash
python run_spider.py --urls https://example.com/ --depths 0 --dynamic
```