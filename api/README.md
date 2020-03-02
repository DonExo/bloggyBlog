# bloggyBlog

### API definitions

After you have successfully set-up and run the local server, visit the following end-points for different actions:


    localhost:8000/api/users/<PK>/ -> Retrieves a single user and his articles
    
    localhost:8000/api/topics/ -> Retrieves a list of all topics. Also an endpoint for Admin user to submit new Topic.
    localhost:8000/api/topics/<PK>/ -> Retrieves a topic and all the articles in it.
    
    localhost:8000/api/articles/ -> Different options are available for this end-point:
        * GET -> retrieves all articles
        * GET (with search query [?search=term] -> retrieves only articles that have the "term" in title or text
        * POST -> Creates a new article. User must be logged-in
    localhost:8000/api/articles/<PK>/ -> Retrieves a single article. Also an end-point for PUT/PATCH/DELETE requests. User needs to be logged in and author of the article

    localhost:8000/token/ -> Endpoint for retrieving user's token by providing username and password.
    localhost:8000/token/refresh -> Endpoint for refreshing the access token, by providing the refresh token

This API reference can of-course look much better if built with Swagger or similar,
but for the sake of a MVP product this will suffice its needs.