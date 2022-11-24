# FastAPI-App_backend
This is a social media posting app where people can share their thoughts, ideas and many more CRUD Operations.

## OVERVIEW:
Go to https://posts-app-backend.onrender.com/ for backend overview.
Keep in mind that this is just backend part of the application .
Thus, you will need to run it on OpenAPI or Postman.

## Working of the Application:
A person needs to signup to access this applications. Once they signup, a JSON web token is created. This token helps in authentication of the user is done by JWT.
Now, if the person is authorized to perform operations i.e., add new post, delete and other CRUD Operations. 

## Installation 
##### 1.Clone the repo
        gh repo clone divyansh3690/FastAPI-App_backend
        
##### 2. Install the requirements
         pip install -r req.txt
         
##### 3. Run the following command on terminal
         uvicorn main:app --reload


Now, as mentioned above there are two ways to run the application:
1. By uvicorn server that will be live on http://127.0.0.1:8000 or the mentioned url in terminal after you run 3rd command in terminal.
2. By online hosting i.e done by render here at https://posts-app-backend.onrender.com/.

## API Endpints:
#### 1. users

###### i.)  Adding new users (POST operation)
            /authentication/newuser
###### ii.) Login (POST operation)
            /authentication/token
######   NOTE- This request will retun a token for authentication of the user.
######         Always use these commands after the specified url.

#### 2. Home page / Publishing 
        
#####   i.)  Show all posts (GET operation)
            /posts/
#####   ii.) Show all posts of a speciafied user (GET operation)            
            /posts/byuser            
###### NOTE- Using, POSTMAN is the recommended as you will need to pass token of the specified user for authorization.
#####   iii.) Add new post  (POST operation)            
            /posts/           
###### NOTE- Using, POSTMAN is the recommended as you will need to pass token of the specified user for authorization.            
#####   iv.)  Edit a published post (PUT operation)            
            /posts/{post_id}
###### NOTE- Using, POSTMAN is the recommended as you will need to pass token of the specified user for authorization.            
#####   v.)   Delete a published post (DELETE operation)            
            /posts/{post_id}
###### NOTE- Using, POSTMAN is the recommended as you will need to pass token of the specified user for authorization.
