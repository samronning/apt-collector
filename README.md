# Welcome to Apartment Collector!

This is a utility that scrapes various apartment websites (apartments.com/zillow.com/etc..) to get
all of the listings and combine them into one place. The current version works for apartments.com
with plans for future sites.

It also includes search functionality for a postgres database of city names.

## Setting it up

The server requires a local postgres database to search for city names.
There is one table requirement listed below.

### **_us_cities_**

| Column     | Data Type        |       Example |
| ---------- | ---------------- | ------------: |
| city       | text             |    "Murrieta" |
| state_id   | text             |          "CA" |
| state_name | text             |  "California" |
| zips       | text             | "92563 92562" |
| population | integer          |        496046 |
| lat        | double precision |        33.572 |
| lng        | double precision |     -117.1909 |

### **redis**

A redis db is also required. This is used for caching the scraped data to prevent
too many requests to the scraped websites. The keys expire so the
data is always refreshed within the last hour.

### **example keys**

There are two key formats for the apartment data:

- location
- location-page
- Examples:
  - "New-York-NY"
  - "New-York-NY-1"

> Note: when a page isn't specified, it means all of the pages.

> Note: the pages are 1-indexed so the first page is 1. 0 is invalid.

## API

`GET /cities`

Takes a search string and matches it against either the name of the city, the name of the state, or the zip code.
It returns the top 5 list of cities in order of highest population.

Query Params:

- search - city name | state code | zip code
- examples:
  - "Newa"
  - "NJ"
  - "071"

Return example:

```json
[
  {
    "city": "Newark",
    "state_id": "NJ",
    "state_name": "New Jersey",
    "zips": "07103 07102 07105 07104 07107 07106 07108 07112 07114 07101 07175 07188 07191 07192 07193 07195 07198 07199",
    "population": 282011,
    "lat": 40.7245,
    "lng": -74.1725
  }
]
```

`GET /apartments/list`

Takes a page and location and returns the apartment listing page of all scraped sites. If no page is specified, returns all pages.
Stores any retrieved information in redis for 1hr and accesses that first if it exists to speed up retrieval.

Query Params:

- page - the page of the results to retrieve. one-indexed.
- location - string ex: "new-york-ny"

Return example:

```json
[
  {
    "title": "The Griswold",
    "price_min": 1795,
    "price_max": 3895,
    "address": "1117 Griswold St, Detroit, MI 48226",
    "bed_min": 1,
    "bed_max": 3,
    "img": "https://images1.apartments.com/i2/OtUXXBVcmqeisupsda9ysyP94C08tCTcI-OO5R6_t5Y/117/the-griswold-detroit-mi-building-photo.jpg"
  }
]
```

## Structures and Formats

**location**

A location is always in the format of cityname-statecode and any whitespace is replaced with "-" ex: "new-york-ny".
Location should be all lowercase.
