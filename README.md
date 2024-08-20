# Social media api
Api for social media service
___
### Requirements:
 - User Registration and Authentication:
 - Users should be able to register with their email and password to create an account.
 - Users should be able to login with their credentials and receive a token for authentication.
 - Users should be able to logout and invalidate their token.
### User Profile:
 - Users should be able to create and update their profile, including profile picture, bio, and other details.
 - Users should be able to retrieve their own profile and view profiles of other users.
 - Users should be able to search for users by username or other criteria.
### Follow/Unfollow:
 - Users should be able to follow and unfollow other users.
 - Users should be able to view the list of users they are following and the list of users following them.
### Post Creation and Retrieval:
 - Users should be able to create new posts with text content and optional media attachments (e.g., images). (Adding images is optional task)
 - Users should be able to retrieve their own posts and posts of users they are following.
 - Users should be able to retrieve posts by hashtags or other criteria.
### Likes and Comments:
 - Users should be able to like and unlike posts. Users should be able to view the list of posts they have liked. 
 - Users should be able to add comments to posts and view comments on posts.
### Schedule Post creation using Celery:
 - Add possibility to schedule Post creation (you can select the time to create the Post before creating of it).
___
#### API Permissions:
 - Only authenticated users should be able to perform actions such as creating posts, liking posts, and following/unfollowing users.
 - Users should only be able to update and delete their own posts and comments.
 - Users should only be able to update and delete their own profile.
#### API Documentation:
 - The API should be well-documented with clear instructions on how to use each endpoint.
 - The documentation should include sample API requests and responses for different endpoints.
#### Technical Requirements:
 - Use Django and Django REST framework to build the API.
 - Use token-based authentication for user authentication.
 - Use appropriate serializers for data validation and representation.
 - Use appropriate views and viewsets for handling CRUD operations on models.
 - Use appropriate URL routing for different API endpoints.
 - Use appropriate permissions and authentication classes to implement API permissions.
 - Follow best practices for RESTful API design and documentation.
___
1. `git clone https://github.com/AllaKuksa/social-media-api.git`
2. `python -m venv venv`
3. `source venv/bin/activate`
4. `pip install -r requirements.txt`
5. Set the following environment variables:
   SECRET_KEY=<your secret key> in .env file
6. `python manage.py makemigrations`
7. `python manage.py migrate`
8.  `python manage.py runserver`

## Getting access

 - `create user  /api/user/register/`
 - `get access token  /api/user/token/`
 - `logout  /api/user/logout/`

## Post creation using Celery with broker Redis

 - `docker run -d -p 6379:6379 redis`
 - `celery -A social_media_api worker --loglevel=INFO`

## Run Flower
 - `celery --broker=amqp://guest:guest@localhost:5672// flower`

## API Swagger
 - `/api/schema/swagger-ui/`
