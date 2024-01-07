# Data Description

## Tables

### Table 1: clientData


| Variable Name          | Description                     | Data type |
|------------------------|---------------------------------|-----------|
| first_name             | First name of the user                   |object|
| last_name              | Last name of the user                    |object|
| email                  | User e-mail for log-in |object                  |
| gender                 | Gender of the user |object                     |
| username               | Username |object                               |
| date_of_birth          | User's Date of Birth |object                  |
| nationality            | User's Nationality |object                    |
| city                   | User's District in Portugal |object            |
| travel_car             | Whether the user prefers to travel by car |bool |
| drinks_alcohol         | Whether the user drinks alcohol |bool          |
| dietary_restrictions   | Possible Dietary restrictions |object          |
| allergies              | Possible allergies |object                     |
| favourite_food         | User's favourite meal |object                  |
| dislike_food           | User's most unliked meal |object               |
| preferred_payment      | User's preferred payment type |object     |
| restaurant_style       | User's preferred restaurant style |object      |
| cuisine_type           | User's preferred cuisine type |object          |
| lunch_hour             | User's typical lunch time period       |      object    |
| dinner_hour            | User's typical dinner time period       |       object  |
| normal_price_range     | Average price in € the user is willing to pay | integer  |
| smoker_n               | Whether the user is a smoker or not |bool     |


_Description_: this .csv file is used to collect and store user preference data for the FlavourFlix platform. <br> It contains information about FlavourFlix's clients after completing their profile page in the app.


<br>

### Table 2: og_restaurant_data

|  Variable Name | Description       | Data Type |
|------------|------------|-------|
|  Unnamed: 0                     |  ID |  integer  |
| address               | Address of the restaurant | string  |
| averagePrice          | Average price of the restaurant | integer |
| chefName              | Name of the chef  | string   |
| cuisine               | Type of cuisine offered  |  string  |
| currency              | Currency used for pricing  |  string  |
| customerPhotos/X      |  URLs to customer photos | string   |
|description|Detailed description of the restaurant| object|
|hasLoyaltyProgram|Indicates if the restaurant has a loyalty program|bool|
|isBookable|Indicates if the restaurant accepts reservations|bool|
|latitude|Geographic latitude of the restaurant|float|
|location|Location of the restaurant|object|
|longitude|Geographic longitude of the restaurant|float|
|name|Nmae of the restaurant|object|
|offer|Special offers available at the restaurant|object|
|paymentAccepted/X |Types of payment accepted| object|
|phone|Contact phone number of the restaurant|float|
|photo | URL to primary photo of the restautant| object
| photos/X          |  	URLs to additional photos of the restaurant |  string  |
|radius|___Radius of service area or delivery (if applicable)___|int|
|ratingValue|Overall rating value of the restaurant|float|
|reviewCount|Number of reviews received|float|
|reviewList/_X_/foodRatingValue|Food rating value in a specific review|float64|
|reviewList/_X_/ratingValue|Overall rating value in a specific review|float64|
|reviewList/_X_/review|Text of the review|object|
|reviewList/_X_/reviewerName|Name of the reviewer|object|
|reviewList/_X_/serviceRatingValue|Service rating value in a specific review|float64|
|style|Style of the restaurant|object|
|tags/_X_|Tags associated with the restaurant|object|
|url|Link to the restaurant TheFork page|object|


_Description:_ this .csv file is related to restaurant data, focusing on various restaurants' characteristics, offerings, and customer interactions.


<br> 

### Table 3: preprocessed_restaurant_data

|  Variable Name | Description  | Data Type |
|------------|------------|-------|
|url|Link to the restaurant page|object|
|name|Name of the restaurant|object|
|address|Address of the restaurant|object|
|photo|Link to the photo of the restaurant|object|
|averagePrice| Average price of the restaurant|integer|
|chefName1|Name of the primery chef|object|
|chefName2|Name of the secondary chef (if applicable)|object|
|chefName3|Name of the third chef (if applicable)|object|
|cuisine|Type of cuisine offered|object|
|michelin|Indicates if the restaurant has a michelin star|integer|
|description|Detailed description of the restaurant|object|
|isBookable|Indicates if the restaurant accepts reservations|bool|
|maxPartySize|Maximum party size that can be accommodated|float|
|schedule|Schedule of the restaurant|object|
|promotions|Current promotions of the restaurant|object|
|phone|Contact phone number of the restaurant|object|
|photo.1|Primary photo of the restaurant|object|
|ratingValue|Average customer rating|float|
|reviewCount|Number of customer reviews|float|
|latitude|Geographic latitude of the restaurant|float|
|longitude|Geographic longitude of the restaurant|float|
|location|Location of the restaurant|object|
|city|City where the restaurant is located|object|
|ambienceRatingSummary|Average ambience rating|float|
|foodRatingSummary|Average food rating|float|
|serviceRatingSummary|Average service rating|float|
|paymentAcceptedSummary|Summary of accepted payment methods|object|
|outdoor_area|Indicates if there is an outdoor dining area|integer|
|current_occupation|Current occupation of the restaurant|integer|
|menu_pre_proc|Pre-processed menu information|object|
|menu_en|Menu details in English|object|
|menu_pt|Menu details in Portuguese|object|


_Description:_ this .csv file contains the preprocessed information from the 'og_restaurant_data.csv' and additional data.

<br>


### Table 4: menus_with_translations

|  Variable Name | Description  | Data Type |
|------------|------------|-------|
|input|URL link to the restaurant's page on TheFork|object|
|menu_pre_proc|Preprocesses menu information|object|
|menu_en|Translated version of the menu in English|object|
|menu_pt|Translated version of the menu in Portuguese|object|

_Description:_ this .csv file contains information about resraurant menus along with their translations.


### Table 5: feedback

| Product ID | Name       | Price |
|------------|------------|-------|
|Email|Email address of the feedback provider|object|
|Name|Name of the feedback provider|object|
|Date|Date when the feedback was provided|object|
|Subject|Subject of the feedback|object|
|Text|Text content of the feedback|object|

_Description:_ this .csv file comprises customer feedback information.

<br>

### Table 6: reservations

| Product ID | Name       | Price |
|------------|------------|-------|
|res_name	|Name of the restaurant where the reservation is made|object|
|guest_name	|Name of the guest making the reservation|object|
|	email	|Email address of the guest|object|
|	date	|Date of the reservation|object|
|	time	|Time of the reservation|object|
|num_people	|Number of people included in the reservation|integer
|special_requests	|Special requests made by the guest (if any)|object|

_Description:_ this .csv file contains the details of the reservations made.

<br>


### Table 7: blog_posts


|Variable Name|	Description	|Data Type
|------------|------------|-------|
|title	|Title of the blog post	|string
|author	|Author of the blog post	|string
|image|	URL link to the blog post's featured image	|string
|date|	Publication date of the blog post|	string
full_text	|Complete text content of the blog post	|string
|corpus|	Structured breakdown of the blog post's content into specific sections like greeting, platform description, personal experience, etc.|	object

_Description:_ this .json file comprises a collection of blog posts related to FlavourFlix.

<br> 

### Table 8: testimonials

| Product ID | Name       | Price |
|------------|------------|-------|
| Client First Name	|First name of the client providing the testimonial	|string
| Review Date	|Date when the testimonial was given	| string
|Rating value (out of ten)	|Customer's rating for FlavourFlix, out of ten	|integer
|Testimonial text	|Text of the customer's testimonial	| string
|Image	|Path to the image associated with the testimonial	| string

_Description:_ this .json file comprises a collection of customer testimonials for FlavourFlix.

<br> 

### Table 9: portuguese_locations

| Product ID | Name       | Price |
|------------|------------|-------|
| Unnamed: 0	|ID|	integer
|name	|Name of the restaurant	|object
|address	|Full address of the restaurant	|object
|location	|General location or city of the restaurant	|object
longitude	|Geographic longitude coordinate of the restaurant|	float64
latitude|	Geographic latitude coordinate of the restaurant	|float64
location2	|Additional location information |	object
location3	|Further location details	|object

_Description:_ this .csv file contains detailed information about various restaurants, primarily focused on their geographical locations.


<br>

## Text Data


### Text File 1: Company

- PDF file explaining the FlavourFlix company, project, background, mission, values and so on. Was used within the vector database of the ChatBot for document retrieval. Generated using ChatGPT and was prior corrected by the group.

### Text File 2: FlavourFlix FAQ

- PDF file with Frequently Asked Questions (FAQ's) and respective answers. Used within the vector database of the ChatBot for document retrieval. Generated using ChatGPT and was prior corrected by the group.

### Text File 3: Problem Identification and Resolution Protocol within the FlavourFlix website

- PDF file explaining possible problems a user may face when experimenting with FlavourFlix' products and ways of resolution. Used within the vector database of the ChatBot for document retrieval. Generated using ChatGPT and was prior corrected by the group.

### Text File 4: Product

- PDF file explaining the products FlavourFlix offers, such as the Analytics Dashboard, the virtual assistant Filomena and so on. Was used within the vector database of the ChatBot for document retrieval. Generated using ChatGPT and was prior corrected by the group.

### Text File 5: Traditional Portuguese Dishes

- PDF file describing the portuguese gastronomic culture, such as recipes, traditions and ingredients. Obtained by compiling and clening the information retrieved from documents on the internet about this matter. Was used within the vector database of the ChatBot for document retrieval.


## Images

### FlavourFlix Logo
![Alt text](ext_images\logo1.jpeg "FlavourFlix Logo")

### FlavourFlix Page Icon
Used on the page tabs.
![Alt text](ext_images\page_icon.png "FlavourFlix Page Icon")

### FlavourFlix Home Page Image
![Alt text](ext_images\pnas.1913308116fig01.jpeg "FlavourFlix Page Icon")

### Comfort Food Lover Illustration
Generated using Adobe Firefly <br>

![Alt text](ext_images\personalities\comfort_food_lover.png "Comfort Food Lover Illustration")

### Conscious Eater Illustration
Generated using Adobe Firefly <br>


![Alt text](ext_images\personalities\conscious_eater.png "Conscious Eater Illustration")

### Fine Dining Connoisseur Illustration
Generated using Adobe Firefly <br>


![Alt text](ext_images\personalities\fine_dining_connoisseur.png "Fine Dining Connoisseur Illustration")


### Low Cost Foodie Illustration
Generated using Adobe Firefly <br>


![Alt text](ext_images\personalities\low_cost_foodie.jpeg "Low Cost Foodie Illustration")

### The Adventurer Illustration
Generated using Adobe Firefly <br>


![Alt text](ext_images\personalities\the_adventurer.png "The Adventurer Illustration")


 
### Testimonial Picture 1 <br>

Generated using DALLE-e <br>

![Alt text](ext_images/testimonials_img/img_f1.jpg "Testimonial Picture 1")


 
### Testimonial Picture 2 <br>

Generated using DALLE-e <br>

![Alt text](ext_images/testimonials_img/img_f2.jpg "Testimonial Picture 2")


 
### Testimonial Picture 3 <br>

Generated using DALLE-e <br>

![Alt text](ext_images/testimonials_img/img_f3.jpg "Testimonial Picture 3")


 
### Testimonial Picture 4 <br>

Generated using DALLE-e <br>

![Alt text](ext_images/testimonials_img/img_f4.jpg "Testimonial Picture 4")


 
### Testimonial Picture 5 <br>

Generated using DALLE-e <br>

![Alt text](ext_images/testimonials_img/img_f5.jpg "Testimonial Picture 5")


 
### Testimonial Picture 6 <br>

Generated using DALLE-e <br>

![Alt text](ext_images/testimonials_img/img_f6.jpg "Testimonial Picture 6")


 
### Testimonial Picture 7 <br>

Generated using DALLE-e <br>

![Alt text](ext_images/testimonials_img/img_f7.jpg "Testimonial Picture 7")


 
### Testimonial Picture 8 <br>

Generated using DALLE-e <br>

![Alt text](ext_images/testimonials_img/img_f8.jpg "Testimonial Picture 8")


 
### Testimonial Picture 9 <br>

Generated using DALLE-e <br>

![Alt text](ext_images/testimonials_img/img_f80.jpg "Testimonial Picture 9")


 
### Testimonial Picture 10 <br>

Generated using DALLE-e <br>

![Alt text](ext_images/testimonials_img/img_f9.jpg "Testimonial Picture 10")


 
### Testimonial Picture 11 <br>

Generated using DALLE-e <br>

![Alt text](ext_images/testimonials_img/img_f91.jpg "Testimonial Picture 11")


 
### Testimonial Picture 12 <br>

Generated using DALLE-e <br>

![Alt text](ext_images/testimonials_img/img_f92.jpg "Testimonial Picture 12")


 
### Testimonial Picture 13 <br>

Generated using DALLE-e <br>

![Alt text](ext_images/testimonials_img/img_m1.jpg "Testimonial Picture 13")


 
### Testimonial Picture 14 <br>

Generated using DALLE-e <br>

![Alt text](ext_images/testimonials_img/img_m2.jpg "Testimonial Picture 14")


 
### Testimonial Picture 15 <br>

Generated using DALLE-e <br>

![Alt text](ext_images/testimonials_img/img_m3.jpg "Testimonial Picture 15")


 
### Testimonial Picture 16 <br>

Generated using DALLE-e <br>

![Alt text](ext_images/testimonials_img/img_m4.jpg "Testimonial Picture 16")


 
### Testimonial Picture 17 <br>

Generated using DALLE-e <br>

![Alt text](ext_images/testimonials_img/img_m5.jpg "Testimonial Picture 17")


 
### Testimonial Picture 18 <br>

Generated using DALLE-e <br>

![Alt text](ext_images/testimonials_img/img_m6.jpg "Testimonial Picture 18")


 
### Testimonial Picture 19 <br>

Generated using DALLE-e <br>

![Alt text](ext_images/testimonials_img/img_m7.jpg "Testimonial Picture 19")


 
### Testimonial Picture 20 <br>

Generated using DALLE-e <br>

![Alt text](ext_images/testimonials_img/img_m8.jpg "Testimonial Picture 20")


 
### Testimonial Picture 21 <br>

Generated using DALLE-e <br>

![Alt text](ext_images/testimonials_img/img_m9.jpg "Testimonial Picture 21")







