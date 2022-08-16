# Made by Pedro Rioja

## The API documentation is in the following link:

https://salty-retreat-41066.herokuapp.com/api/docs


## In order to send posts requests to the API, the category needs to be one of the following:

- Pymes
- Casos de éxito
- Corporativos
- Emprendedores
- Xepelin
  
\* All categories are case insensitive


## The CURL command for sending POST requests is:

curl -X POST https://salty-retreat-41066.herokuapp.com/api/category_scrapper -d '{"category": "Pymes", "webhook": "WEBHOOK"}' -H 'Content-Type: application/json'
