# Price-Miner
**CURRENT HOST**: 
[https://price-miner.herokuapp.com](https://price-miner.herokuapp.com/)

This is a web crawler from e-commerces that i made for Price Management class of my Marketing Graduation and want to turn on my possible TCC for price analysis of e-commerces

It is a public api to retrieve data from e-commerces asynchronously. You send a first url to retrieve data from and the number os items you want to extract. The 
backend handles everything else automatically.

## Motivation
Most of the analysis  and studies made for studying prices on e-commerces are qualitative and not quantitative. This is for retrieving a lot of data so
researchers can have a better understading of the prices on e-commerces and how is it managed and decided based on quantitative data.

### Why not scrapy?
Scrapy is a webcrawler framework written in python that is fast and reliable for crawling websites. The problem is that it doesn't work well on some
javascript based websites like some of the biggest e-commerces out there. So the idea here is to make it easy and possible to crawl e-commerces that 
have javascript generated content.

## Initialization
You need to run it inside of the docker-compose, sorry, just run
   
    $ docker-compose up --build

The program will be available on `localhost` port `5000`.

This program uses the **seleniumhub** available on port `4444`, **redis** to handle messages available on port `6379` and it also have a **postgres** 
that will probably be used in the future (or not).

## Working with the API

All the API uses just one url: `\mine`

### POST
For `POST` requests send a **JSON** with the following parameters

+ **url** (*String*): Initial url from e-commerce to extract data from.
+ **max_number** (*Integer*): max number of items to extract from e-commerce. Max: 85
+ **similar_products_container_tag** (*String*): The container for similar products (div, ul, etc.).
+ **similar_products_container_class** (*String*): The class of the container for similar products.
+ **data** (*List[dict]*): The container to get products price (div, ul, etc.).
    + **name** (*String*): The key that will hold the result
    + **container_tag** (*String*): The tag of the content you want to retrieve
    + **container_class** (*String*): The class of the content you want to retrieve
    + **to_get** (*String*): tells white type of content to retrieve, if **text** is passed, it retrieves the 
    textContent of the tag. Defaults to: `text￿￿`
+ *OPTIONAL* **blacklist** (*List[String]*): Tells what string the title cannot contain. Ex.: If you don't
                                    want to retrieve notebooks you would send a list `['notebook']`
                                    if you also don't want monitors also it would be `['notebook', 'monitor']`
+ *OPTIONAL* **whitelist** (*List[String]*): Tells what string the title can contain. Ex.: If you only
                                    want to retrieve notebooks you would send a list `['notebook']`
                                    if you want monitors also it would be `['notebook', 'monitor']`
+ *OPTIONAL* **sleep_time** (*Integer*): Max time to sleep until retrieve data. Default: 10, Max: 60
+ *OPTIONAL* **main_url** (*String*): Since some websites just contains the path and not the complete url, this is to
complete the path with the main url of the website.

#### Response
It can return a Celery task id used to get the results from this call, or a message saying that a celery task is already running.

Since it's a really small server, we need to limit the tasks running in the background.


Example:
```json
{
	"url": "https://www.magazineluiza.com.br/notebook-hp-240-g5-14-polegadas-i3-6006u-4gb-500gb-dvdrw-win-10-pro/p/7280842/in/note/",
	"max_number": 2,
	"similar_products_container_tag": "div",
	"similar_products_container_class": "slick-track",
	"data": [{
	  "name": "price",
	  "container_tag": "div",
	  "container_class": "price-template",
	  "to_get": "text"
    }],
	"sleep_time": 20
}
```

### GET

For `GET` send a request with the following parameter:
 
+ **job_id** (*String*): The id of celery task

#### Response
**If Job is running:**
return the task state

**If Job is completed:**
return JSON with task id and task result

Example:

```
$ curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET  http://localhost:5000/mine?job_id=95a88c3c-684e-49d4-a3bd-551245c49944
```

returns 
```json
{
    "content": {
        "content": [
            {
                "data": {
                    "price": "   por R$ 595,90      em 10x de R$ 59,59 sem juros "
                },
                "title": "Smartphone Samsung Galaxy J4 Core Tela infinita de 6 Câmera Frontal de 5MP Android Go 8.1- Preto - Galaxy J4 Core - Magazine Luiza"
            },
            {
                "data": {
                    "price": "   por R$ 598,74      em 10x de R$ 59,87 sem juros "
                },
                "title": "Smartphone Multilaser Ms60Z 2Gb Ram Tela 6 Pol. Ips Hd 16Gb Android 8.1 Câmera 13Mp+13Mp Com Sensor Digital Preto + Cartão Memória 32Gb - NB741 - Smartphone - Magazine Luiza"
            },
            {
                "data": {
                    "price": "   por R$ 669,00      em 10x de R$ 66,90 sem juros "
                },
                "title": "Smartphone Meizu M6 Dourado, Tela 5,2”, 3GB Ram, 32GB, Câmara 13MP/8MP, Dual Sim - Smartphone - Magazine Luiza"
            }
        ],
        "error": "",
        "last_url": "https://api-ads.percycle.com/click/?hash=gSCXUT3OOVKVqLNshqamxvgJ6e8UChYepRPPpaqmZ%2BCnRNMHK4RpbN9RyD9if1ItUM8h%2FR%2FtabAc4TJZiyHboht3WwAjp0H%2BvswRad3QQxF7JP4CTFeJlYjgYxtBRvKOrlznkE1vwfGgkKazOUJhOdD3RQtQ1I1QTYnnck6DtXUHkrGhp26PNc0ErjugJKzBGX%2BxizRO%2BOboeEiSo7aSNyplLNdBsIctrjtOR9lUUXUhjxiEDcfB%2B4Cp2k%2BhIHyPXe4AXTSObkYfl6xKaYvY7bNpV%2FOk2qxmTAkJkJ2yk4CV686rxLYAxfwFarHdhmHXZwmkLZk5x51wZHcgxvrfvmKvslAA4lOXPThDyh%2Bi4YXu5LezSevgo1xaLgS%2B0tMV7%2Fk%2B4UK0SeRtOsVSLIxwRHeHB%2FcGbynWHnurAVFcxGMy7WgS4cla1b88EPo0oEvEkLrUplD7IPPJzLVhE5DRto3mBvAg7SlC0jKJJEAnguMljSJam5y%2F53YITXDKHk0tRlOYkQovej%2Fgz3sR7U7aLIdocfxmhb4jylqIcRPSSshR%2F1t6tNFLmWejmg8hpFWIbb5DWsxRuXBw37nXrvqDp9TDy%2B9CzcgiUdGsTE3gVXtuTUyIWXQk9CZRwZsQe09Kzv6f33BQ0UUcbWfxLYxWvHfYMHNeWRsrJ7kccp8Y%2B5y8Z7Fhlps%2BMhUth7z5XTqNoTwNhnIMj5lvW3DdfpGqBNEorm2Zk%2Fn1NUdhjOg4WGfoeBYr7ZR8zZu9JqwLMkaYJajgCgQjsikFXxVh7igX6w%3D%3D"
    },
    "status": "SUCCESS",
    "task_id": "cbb6abb3-234e-4f86-98aa-850574d7ddd3"
}
```

## Deploying
First deploy selenium docker on selenium folder, then after making sure it is working deploy this application.

IMPORTANT: Make sure you change the production SELENIUM_WEBDRIVER_HOST configuration

## Known Issues
+ Add a small test case
+ For being selenium based it is not performatic, it would be nice to change that.
+ Missing serializer for post request, it's created really badly
+ Missing nginx configuration
+ Doesn't reload when a change is made on docker-compose so it needs to be rebuilt everytime
+ A nice and user friendly front-end for the common user

## Contribute
Feel free to send issues, all PR will be verified.

