## /login 

#### GET 

If authenticated: 
```
{ 
  status: 200, 
  message: 'Logged in'
}
``` 

If not authenticated: 
``` 
{ 
   status: 401, 
   message: 'Not logged in' 
}
```

#### POST 

```
{ 
  username: ..., 
  password: ... 
} 
```

If rejected: 

``` 
{ 
   status: 401, 
   message: 'Invalid credentials'
} 
```

## /signup 

#### POST 

```
{ 
   username: ... ,
   password: ... ,
   email:    ... ,
   phone:    ... ,
   textEnabled: true/false,
   emailEnabled: true/false
} 
```

^ Note, maybe those could be checkboxes...these will be translated into the notifications array 

## /logout 

#### POST 

```
{ username: ... } 
```
