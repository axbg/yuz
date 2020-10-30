# yuz
#### A python-based web service & web app that allows portraits extraction from a photo

##### Deployment
* Docker
  * ```docker run -d -p prefered_port:8080 --name yuz axbg/yuz```
* Manually
  * Install >python3.7
  * Optional: create and activate a virtual environment
  * navigate to /yuz
  * run *"pip install -r requirements.txt"*
  * Optional: change the database from sqlite3 [to your preffered provider](https://docs.djangoproject.com/en/3.0/topics/db/multi-db/)
  * run *"python manage.py migrate"*
  * run *"python manage.py runserver"*
  * go and extract some faces

##### Using the REST interface
* Send a POST request on */register* with Content-Type *'application/json'* and body:
    {
    	"username":"your_username",
    	"password":"your_password",
    	"email": "your@email.com"
    }
    
* Send a POST request on */login* with Content-Type *'application/json'* and body:
{
	"username":"your_username",
	"password":"your_password"
}
* The response will contain the access token that you'll need to append in the Authorization header as *'Bearer token'*
* To extract faces from a photo, send a POST request on *'/extract'* providing the target image either encoded in base64 or directly as a file in the request body under the name 'original'
* The result will contain all the resulting extractions as base64 encoded images
* If you want to remove the current access token, send a POST request on *'/logout'* including the same Authorization header as above

##### Using the Web interface
* After launching the app, navigate to "/"

* Drag 'n' drop your image in the specified zone
* After the results have been computed, you can repeat the process by dropping another image
