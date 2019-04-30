# Scooby-Doo!
This is a web crawler from e-commerces that i made for Price Management class of my Marketing Graduation and want to turn on my possible TCC for price analysis of e-commerces

This is a public api to retrieve data from e-commerces asynchronously. You send a first url to retrieve data from and the number os items you want to extract. The 
backend handles the rest automatically.

## Initialization
You need to run it inside of the docker-compose, sorry, just run
   
    $ docker-compose up --build

The program will be available on `localhost` port `5000`.

This program uses the **selenium-hub** available on port `4444`, **redis** to handle messages available on port `6379` and it also have a **postgres** that will probably be used in 
the future (or not).

## Working with the API

All the API uses just one url: `\mine`

### POST
For `POST` requests send a **JSON** with the following parameters

+ **url** (*String*): Initial url from e-commerce to extract data from.
+ **max_number** (*Integer*): max number of items to extract from e-commerce. Max: 85
+ **similar_products_container_tag** (*String*): The container for similar products (div, ul, etc.).
+ **similar_products_container_class** (String): The class of the container for similar products.
+ **price_container_tag** (*String*): The container to get products price (div, ul, etc.).
+ **price_container_class** (*String*): The class of the container to get products price.
+ *OPTIONAL* **item_types** (*List[String]*): Tells what string the title can contain. Ex.: If you only
                                    want to retrieve notebooks you would send a list ['notebook']
                                    if you want monitors also would be ['notebook', 'monitor']
+ *OPTIONAL* **sleep_time** (*Integer*): Max time to sleep until retrieve data. Default: 5, Max: 60
+ *OPTIONAL* **main_url** (*String*): The main url of the website.

It returns a Celery task id used to get the results from this call

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
    
**If Job is running:**
return the task state

**If Job is completed:**
return JSON with task id and task result

Example:

```http://localhost:5000/mine?job_id=95a88c3c-684e-49d4-a3bd-551245c49944```


## Contribute
Feel free to send issues, all PR will be verified.

