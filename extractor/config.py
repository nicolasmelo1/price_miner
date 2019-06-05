PRICE_MINER_HOST = "http://localhost:5000"

BODY_REQUEST = {
    "url": "https://pt.aliexpress.com/item/32997336578.html?spm=a2g03.search0104.3.1.2b667a08O6IYTt&ws_ab_test=searchweb0_0%2Csearchweb201602_6_10065_10068_10547_319_10059_10884_317_10548_10887_10696_321_322_10084_453_10083_454_10103_10618_10307_537_536%2Csearchweb201603_53%2CppcSwitch_0&algo_expid=5b4e1fc7-13ec-42a8-b0d6-ac17052cecba-0&algo_pvid=5b4e1fc7-13ec-42a8-b0d6-ac17052cecba",
    "max_number": 5,
    "similar_products_container_tag": ["div"],
    "similar_products_container_class": ["bottom-recommendation"],
    "data": [{
        "name": "price",
        "container_tag": "div",
        "container_class": "product-price",
        "to_get": "text",
        "required": True
    }],
    "main_url": "",
    "blacklist": [],
    "sleep_time": 20
}