## /login 

#### GET 

If authenticated returns status 200 

#### POST 

{ username: '', password: '' } 

## /signup 

#### POST 

{ 
   username: ...
   password: ... 
   email:    ... 
   phone:    ... 
   textEnabled: true/false
   emailEnabled: true/false
} 

^ Note, maybe those could be checkboxes...these will be translated into the notifications array 

## /logout 

#### POST 

{ username: '' } 
