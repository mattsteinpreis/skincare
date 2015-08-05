# Skincare for Steph

This is a simple web app which queries a database of skin care products
scraped from [drugstore.com](http://www.drugstore.com/beauty/skin-care/qxg180646-0).
This project is request from my girlfriend, who wanted to be able to search the products by ingredients, 
which are listed on the website but not available for searching.

The dataframe uses Python pandas, and the web app uses Flask is hosted on Heroku at [skincareforsteph.herokuapp.com](https://skincareforsteph.herokuapp.com).

Since I'm an HTML noob, the site is quite basic. Stay tuned for prettier updates!

Current features:
* select categories
* exclude ingredients
* sort by price or rating
* reset dataframe

Planned additions:
* lists of available categories and ingredients
* add links to product page
* make it pretty
* automatic (weekly?) scraping for up-to-date database
