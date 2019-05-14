PRICE_MINER_HOST = "http://localhost:5000"

BODY_REQUEST = {
    "url": "https://www.magazineluiza.com.br/iphone-8-apple-64gb-dourado-4g-tela-47-retina-cam-12mp-selfie-7mp-ios-11/p/155542800/te/teip/",
    "max_number": 30,
    "similar_products_container_tag": "ul",
    "similar_products_container_class": "showcase showcase__five-product js-carousel-showcase-wvav slick-initialized slick-slider",
    "data": [{
      "name": "price",
      "container_tag": "div",
      "container_class": "price-template",
      "to_get": "text",
      "required": True
    }],
    "blacklist": [],
    "whitelist": ["smartphone", "samsung", "xiaomi", "android", "iphone", "apple"],
    "sleep_time": 20
}
