Project-Casting-Agency
-----

## Introduction
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

![image](https://github.com/KhoiVuKha/Project-Casting-Agency/assets/15206083/12ef12f0-8827-4beb-a7e7-f3d214e5d7da)


## Overview
This Project-Casting-Agency takes responsible for:

* creating new actors, movies.
* searching for actors and movies.
* learning more about a specific movie or actor.

## Tech Stack (Dependencies)

### 1. Backend Dependencies
Our tech stack will include the following:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-Migrate** for creating and running schema migrations
You can download and install the dependencies mentioned above using `pip` as:
```
pip install virtualenv
pip install SQLAlchemy
pip install postgres
pip install Flask
pip install Flask-Migrate
```
> **Note** - If we do not mention the specific version of a package, then the default latest stable package will be installed. 

### 2. Frontend Dependencies
You must have the **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend. Bootstrap can only be installed by Node Package Manager (NPM). Therefore, if not already, download and install the [Node.js](https://nodejs.org/en/download/). Windows users must run the executable as an Administrator, and restart the computer after installation. After successfully installing the Node, verify the installation as shown below.
```
node -v
npm -v
```
Install [Bootstrap 3](https://getbootstrap.com/docs/3.3/getting-started/) for the website's frontend:
```
npm init -y
npm install bootstrap@3
```


## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. Includes your SQLAlchemy models.
                    "python app.py" to run after installing dependencies
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── forms.py *** Your forms
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```

Overall:
* Models are located in the `MODELS` section of `models.py`.
* Controllers are also located in `app.py`.
* Authentications are located in `auth/auth.py`.
* The web frontend is located in `templates/`, which builds static assets deployed to the web server at `static/`.
* Web forms for creating data are located in `form.py`


Highlight folders:
* `templates/pages` -- Defines the pages that are rendered to the site. These templates render views based on data passed into the template’s view, in the controllers defined in `app.py`. These pages successfully represent the data to the user, and are already defined for you.
* `templates/layouts` -- Defines the layout that a page can be contained in to define footer and header code for a given page.
* `templates/forms` -- Defines the forms used to create new movies, and actors.
* `app.py` -- Defines routes that match the user’s URL, and controllers which handle data and renders views to the user. This is the main file you will be working on to connect to and manipulate the database and render views with data to the user, based on the URL.
* Models in `models.py` -- Defines the data models that set up the database tables.
* Authentications in `auth/auth.py` -- Defines some methods to get authentication header, get and decode JWT token and check permissions.

## Development Setup
1. **Clone the project**
```
git clone git@github.com:KhoiVuKha/Project-Casting-Agency.git
cd Project-Casting-Agency
```

2. **Initialize and activate a virtualenv using:**
```
python3 -m venv env
source env/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
source env/Scripts/activate
```

3. **Install the dependencies:**
```
pip install -r requirements.txt
```

4. **Set up environment:**
Note that the main database was deployed in render server.
```
chmod +x setup.sh
source setup.sh
```

5. **Run unit test**
Note: Before run unit test, please do some steps in `section 8` to get the JWT token for `Excutive Producer` user and modify the old token (variable `JWT`) in `setup.sh` file
```
dropdb casting_agency_test # (optional) Drop if it exists
createdb casting_agency_test 
psql -U postgres -d casting_agency_test < casting_agency_test.sql
python3 test_app.py
```

6. **Run API test (RBAC)**
Note: Before run API test, please do some steps in `section 8` to get the JWT tokens for `Casting Assistant`, `Casting Director`, `Excutive Producer`, save these tokens in order to import to Postman in the future.
We may need using some Incognito tabs of browser to prevent caching or we may need to clear cache for another login.
```
dropdb casting_agency_test # (optional) Drop if it exists
createdb casting_agency_test 
psql -U postgres -d casting_agency_test < casting_agency_test.sql
python3 app.py
```

Open Postman and import json config: `project-casting-agency.postman_collection.json` modify these old JWT tokens with these new token that you've just saved and run all test of `project-casting-agency` with following configs:
- Run manually
- Interations: 1
- Delay: 0
Then press `Run project-casting-agency` to run all test.

7. **Run the development server locally:**
```
python3 app.py
```

8. **Verify on the Browser**<br>
Please press Login in Navigation Bar and login as following roles (User name and password provided in setup.sh file):
  - Casting Assistant
    - Can view actors and movies
  - Casting Director
    - All permissions a Casting Assistant has and…
    - Add or delete an actor from the database
    - Modify actors or movies
  - Executive Producer
    - All permissions a Casting Director has and…
    - Add or delete a movie from the database
Then get appropriate JWT token in the address bar of browser.

- For Development (Run app locally):
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000)

- For users (Run app deployed in render server): https://casting-agency-specifications.onrender.com/.

## Troubleshooting:
- If you encounter any dependency errors, please ensure that you are using Python 3.9 or lower.
- If you are still facing the dependency errors, follow the given commands:
  - `using pip install --upgrade flask-moment`
  - `Using pip install Werkzeug==2.0.0`
  - `Using pip uninstall Flask and then pip install flask==2.0.3`

## Deployment to Render Cloud Platform
Follow [this instruction]() to deploy Flask App to Render Cloud.

## API Reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
- Authentication: auth0.

### Error Handling
Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "error": 404,
    "message": "Not Found"
}
```

Currently, the API will return two error types when requests fail:
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 405: Method not allowed
- 422: Unprocessable
- 500: Internal server error


### Endpoints

#### GET '/actors'
- General: Fetch all actors
  - Fetches all actor's information
  - Request parameters: None
  - Returns: list of actors and success status.
- Sample of request: ```curl http://127.0.0.1:5000/actors -H 'Content-Type: application/json' -H 'Authorization: Bearer <JWT_TOKEN>'```
- Sample of response:
```
{
  "actors": [
    {
      "age": "69", 
      "gender": "{Male}", 
      "id": 2, 
      "image_link": "https://c4.wallpaperflare.com/wallpaper/518/546/557/jackie-chan-affair-men-actor-wallpaper-preview.jpg", 
      "name": "Jackie Chan"
    }, 
    {
      "age": "61", 
      "gender": "{Male}", 
      "id": 3, 
      "image_link": "https://www.goldderby.com/wp-content/uploads/2022/05/top-gun-maverick.jpg", 
      "name": "Tom Cruise"
    }, 
    {
      "age": "47", 
      "gender": "{Female}", 
      "id": 12, 
      "image_link": "https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcQjMLlgBjjXiBcXkBfj8ioAVD9JRbLbvFChl24qgBZMd-uLMhNZMEqA-lC_CxnJS1S1f8haDnRBBehf-l4", 
      "name": "Angelina Jolie"
    }, 
    {
      "age": "59", 
      "gender": "{Male}", 
      "id": 13, 
      "image_link": "https://www.thewikifeed.com/wp-content/uploads/2021/11/brad-pitt-1.jpg", 
      "name": "Brad Pitt"
    }
  ], 
  "success": true
}
```

#### POST '/actors/search'
- General: Search for actor by actor's name.
  - Sends a post request in order to search for actor by search term (actor's name)
  - Request parameters: search_term.
  - Returns: (list of) actor(s) that related to search term, total number of actors match, success status.
- Sample of request: 
```curl http://127.0.0.1:5000/actors/search -X POST -H 'Content-Type: application/json' -H 'Authorization: Bearer <JWT_TOKEN>' -d '{"search_term": "chan"}'```
- Sample of response: when search_term = "chan"
```
{
  "actors": [
    {
      "age": "69", 
      "gender": "{Male}", 
      "id": 2, 
      "image_link": "https://c4.wallpaperflare.com/wallpaper/518/546/557/jackie-chan-affair-men-actor-wallpaper-preview.jpg", 
      "name": "Jackie Chan"
    }
  ], 
  "success": true, 
  "total": 1
}
```

#### GET '/actors/id'
- General: Fetch actor by id
  - Fetches actor by id
  - Request parameters: None
  - Returns: actor's information and success status.
- Sample of request: ```curl http://127.0.0.1:5000/actors/2 -H 'Content-Type: application/json' -H 'Authorization: Bearer <JWT_TOKEN>'```
- Sample of response:
```
{
  "actor": [
    {
      "age": "69", 
      "gender": "{Male}", 
      "id": 2, 
      "image_link": "https://c4.wallpaperflare.com/wallpaper/518/546/557/jackie-chan-affair-men-actor-wallpaper-preview.jpg", 
      "name": "Jackie Chan"
    }
  ], 
  "success": true
}
```

#### POST '/actors/create'
- General: Add a new actor's information record.
  - Send a post request to add a new actor's information record.
  - Request parameters: Actors's name, age, gender, image.
  - Returns: The new movie, success status, total actors.
- Sample of request: ```curl -X POST -H 'Content-Type: application/json' -H 'Authorization: Bearer <JWT_TOKEN>' -d '{"name":"Tom Holland", "age":"27", "gender":"Male", "image_link":"None"}' http://127.0.0.1:5000/actors/create```
- Sample of response:
```
{
  "actor": [
    {
      "age": "27", 
      "gender": "Male", 
      "id": 15, 
      "image_link": "None", 
      "name": "Tom Holland"
    }
  ], 
  "success": true
}
```

#### DELETE '/actors/${id}'
- General: Delete actor by id.
  - Deletes a specified actor using the id of the actor
  - Request parameters: `actor_id` - integer
  - Returns: the id of the deleted actor, success value.
- Sample of request to delete actor with id = 16:
```curl -H '{"Content-Type: application/json"}' -H 'Authorization: Bearer <JWT_TOKEN>' -X DELETE http://127.0.0.1:5000/actors/16```
- Sample of response:
```
{
  "actor_id": "16", 
  "success": true
}
```

#### POST '/actors/${id}/edit'
- General: Update actor by id.
  - Update some information of an actor based on a payload
  - Request parameters: `actor_id` - integer and actor's info.
  - Returns: current actor, success value.
- Sample of request to modify actor with id = 2:
```curl -X POST -H 'Content-Type: application/json' -H 'Authorization: Bearer <JWT_TOKEN>' -d '{"name":"Jackie Chan", "age":"70", "gender":"Male", "image_link":"https://c4.wallpaperflare.com/wallpaper/518/546/557/jackie-chan-affair-men-actor-wallpaper-preview.jpg"}' http://127.0.0.1:5000/actors/2/edit```

```
{
  "actor": [
    {
      "age": "70", 
      "gender": "Male", 
      "id": 2, 
      "image_link": "https://c4.wallpaperflare.com/wallpaper/518/546/557/jackie-chan-affair-men-actor-wallpaper-preview.jpg", 
      "name": "Jackie Chan"
    }
  ], 
  "success": true
}
```

#### GET '/movies'
- General: Fetch all movies
  - Fetches all movie's information
  - Request parameters: None
  - Returns: list of actors and success status.
- Sample of request: ```curl http://127.0.0.1:5000/movies -H 'Content-Type: application/json' -H 'Authorization: Bearer <JWT_TOKEN>'```
- Sample of response:
```
{
  "movies": [
    {
      "id": 1, 
      "image_link": "https://prod-ripcut-delivery.disney-plus.net/v1/variant/disney/863E75A035911DBA10F8D7EE1E433A12A1BF4915670B66597AC31C585A291942/scale?width=1200&aspectRatio=1.78&format=jpeg", 
      "release_date": "28/12/2019", 
      "title": "Avengers: Endgame"
    }, 
    {
      "id": 2, 
      "image_link": "https://www.intofilm.org/intofilm-production/7019/scaledcropped/970x546/resources/7019/kung-fu-panda-2-ep-dreamworks-animation.jpg", 
      "release_date": "28/12/2008", 
      "title": "Kung Fu Panda"
    }, 
    {
      "id": 3, 
      "image_link": "https://m.media-amazon.com/images/I/814FWjSQFfL._RI_.jpg", 
      "release_date": "31/10/2010", 
      "title": "The Walking Dead"
    }
  ], 
  "success": true
}
```

#### POST '/movies/search'
- General: Search for movie by movie's name.
  - Sends a post request in order to search for movie by search term (movie's name)
  - Request parameters: search_term.
  - Returns: (list of) movie(s) that related to search term, total number of movies match, success status.
- Sample of request: 
```curl http://127.0.0.1:5000/movies/search -X POST -H 'Content-Type: application/json' -H 'Authorization: Bearer <JWT_TOKEN>' -d '{"search_term": "kung fu"}'```
- Sample of response: when search_term = "chan"
```
{
  "movies": [
    {
      "id": 2, 
      "image_link": "https://www.intofilm.org/intofilm-production/7019/scaledcropped/970x546/resources/7019/kung-fu-panda-2-ep-dreamworks-animation.jpg", 
      "release_date": "28/12/2008", 
      "title": "Kung Fu Panda"
    }
  ], 
  "success": true, 
  "total": 1
}
```

#### GET '/movies/id'
- General: Fetch movie by id
  - Fetches movie by id
  - Request parameters: None
  - Returns: movie's information and success status.
- Sample of request: ```curl http://127.0.0.1:5000/movies/1 -H 'Content-Type: application/json' -H 'Authorization: Bearer <JWT_TOKEN>'```
- Sample of response:
```
{
  "movie": [
    {
      "id": 1, 
      "image_link": "https://prod-ripcut-delivery.disney-plus.net/v1/variant/disney/863E75A035911DBA10F8D7EE1E433A12A1BF4915670B66597AC31C585A291942/scale?width=1200&aspectRatio=1.78&format=jpeg", 
      "release_date": "28/12/2019", 
      "title": "Avengers: Endgame"
    }
  ], 
  "success": true
}
```

#### POST '/movies/create'
- General: Add a new movie's information record.
  - Send a post request to add a new movie's information record.
  - Request parameters: Movie's title, release_date, image_link.
  - Returns: The new movie, success status, total movies.
- Sample of request: ```curl -X POST -H 'Content-Type: application/json' -H 'Authorization: Bearer <JWT_TOKEN>' -d '{"title":"Movie abc", "release_date":"31/05/2023", "gender":"Male", "image_link":"None"}' http://127.0.0.1:5000/movies/create```
- Sample of response:
```
{
  "movie": [
    {
      "id": 6, 
      "image_link": "None", 
      "release_date": "31/05/2023", 
      "title": "Movie abc"
    }
  ], 
  "success": true, 
  "total": 5
}
```

#### DELETE '/movies/${id}'
- General: Delete movie by id.
  - Deletes a specified movie using the id of the movie
  - Request parameters: `movie_id` - integer
  - Returns: the id of the deleted movie, success value.
- Sample of request to delete actor with id = 5:
```curl -H '{"Content-Type: application/json"}' -H 'Authorization: Bearer <JWT_TOKEN>' -X DELETE http://127.0.0.1:5000/movies/5```
- Sample of response:
```
{
  "movie_id": "5", 
  "success": true
}
```

#### POST '/movies/${id}/edit'
- General: Update movie by id.
  - Update some information of a movie based on a payload
  - Request parameters: `movie_id` - integer and movie's info.
  - Returns: current movie, success value.
- Sample of request to modify movie with id = 2:
```curl -X POST -H 'Content-Type: application/json' -d '{"title":"Kung Fu Panda 1", "release_date":"28/12/2009", "image_link":"https://www.intofilm.org/intofilm-production/7019/scaledcropped/970x546/resources/7019/kung-fu-panda-2-ep-dreamworks-animation.jpg"}' http://127.0.0.1:5000/movies/2/edit -H 'Authorization: Bearer <JWT_TOKEN>'```

```
{
  "movie": [
    {
      "id": 2, 
      "image_link": "https://www.intofilm.org/intofilm-production/7019/scaledcropped/970x546/resources/7019/kung-fu-panda-2-ep-dreamworks-animation.jpg", 
      "release_date": "28/12/2009", 
      "title": "Kung Fu Panda 1"
    }
  ], 
  "success": true
}
```
