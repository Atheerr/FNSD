Capstone Project
-----


### Casting Agency

The motivation of this project is to practice the skills learned during the Udacity FullStack NanoDegree program. 

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are

------------


### Casting Agency Specifications

###### Models:
- Movies with attributes title and release date
- Actors with attributes name, age and gender

###### Endpoints:
- GET /actors and /movies
- DELETE /actors/ and /movies/
- POST /actors and /movies and
- PATCH /actors/ and /movies/

###### Roles:
1. Casting Assistant
 - Can view actors and movies ` get:actors`  &  `get:movies`
 
2. Casting Director
	-  `All permissions` a Casting Assistant has and… 
	-  Add or delete an actor from the database ` delete:actors` & `post:actors`
	
	- Modify actors or movies `patch:movies` & `patch:actors`
3. Executive Producer
	- `All permissions` a Casting Director has and… 
	
	- Add or delete a movie from the database `post:movies` & ` delete:movies`

###### Tests:
- One test for success behavior of each endpoint
- One test for error behavior of each endpoint
- At least two tests of RBAC for each role


------------

###Working with the application locally
###### Installing Dependencies
- Python 3.7
- 	`pip install -r requirements.txt`

###### Running the server
On Linux : export

- `export FLASK_APP=app.py`
- `export FLASK_ENV=development`
- `flask run`

On Windows : set
- `set FLASK_APP=app.py`
- `set FLASK_ENV=development`
- `flask run`
###### Run Test:
- `python3.7 test_app.py`


------------

### Endpoints 
- The Host for the endpoints is: https://capstone-atheer.herokuapp.com/

- The flask app is being run locally http://127.0.0.1:5000/ 



- GET /actors
Sample request:

`curl -X GET http://127.0.0.1:5000/actors -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN"`

Sample response:

    {
      "actors": [
        {
          "age": 20, 
          "gender": "Female", 
          "id": 1, 
          "name": "atheer"
        }
      ], 
      "success": true
    }
	
- POST /actors
Sample request:

`curl -X POST http://127.0.0.1:5000/actors -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN"  -d '{"name" : "New_Actor_1", "age" : "30", "gender":"Male"}'`

Sample response: 

    {
      "created": 2, 
      "success": true
    }

- PATCH /actors/<int:actor_id>

Sample request: 

`curl -X PATCH http://127.0.0.1:5000/actors/1 -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" -d '{"name" : "Azooz Saad"}'`

Sample

    {
      "actor": {
        "age": 20, 
        "gender": "Female", 
        "id": 1, 
        "name": "Azooz Saad"
      }, 
      "success": true
    }

- DELETE /actors/<int:actor_id>

Sample request:

`curl -X DELETE http://127.0.0.1:5000/actors/1 -H "Authorization: Bearer ACCESS_TOKEN"`

Sample response:



    {
      "delete": 1, 
      "success": true
    }

- GET /movies

Sample request:

`curl -X GET http://127.0.0.1:5000/movies -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN"`

Sample response:

    
        {
          "movies": [
            {
              "id": 1, 
              "release_date": "Mon, 08 Mar 2021 00:00:00 GMT", 
              "title": "hloe word "
            }
          ], 
          "success": true
        }

- POST /movies

Sample request:

`curl -X POST http://127.0.0.1:5000/movies -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" -d '{"title" : "UPDATE_NAME", "release_date" : "12/6/2020"}'`

Sample response:  

    {
      "created": 2, 
      "success": true
    }
    - PATCH /movies
    {
      "movie": {
        "id": 1, 
        "release_date": "Sun, 06 Dec 2020 00:00:00 GMT", 
        "title": "UPDATE_NAME"
      }, 
      "success": true
    }
    

- DELETE /actors/<int:actor_id>

Sample request:

`curl -X DELETE http://127.0.0.1:5000/actors/1 -H "Authorization: Bearer ACCESS_TOKEN"`

Sample response:  

    {
      "delete": 1, 
      "success": true
    }

------------

### Authors
* Atheer

### Acknowledgments
* The team Udacity
