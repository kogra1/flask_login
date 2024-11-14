# Flask Test Application

Simple flask app with a log in/sign up page and a weather forecast page
## Login / Sign up page

Sign up page that saves a users username, password, and email to a mySQL database
Log in page looks for a user in the database using the username and confirms if the password matches
If log in is confirmed the user's info is saved in the session

## Weather page

 Using the National Weather Service's API, local coordinates are used to retreive weather data using a get method
 The data is then taken out of the JSON format and displayed the webpage
