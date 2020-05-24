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

## /location 

#### GET 

~Important to include the `_id` field here because I think we should use that to populate the subscriptions array...~ Actually there is weirdness around that, guess we can just use code  

```
{ 
 code: ... // state abbreviation 
 name: ... // Full form name (for display purposes) 
}
```  

## /subscribe/locations

#### POST 

```
{ 
   username: ... 
   code: ... // State abbreviation 
 } 
``` 

#### PATCH 

Doing patch instead of delete so we can receive multiple pieces of data 

```
{ 
   username: ... 
   code: ... 
}
``` 

## /subscribe/alerts 

#### POST 
```
{ 
   username: ... 
   textEnabled: ...
   emailEnabled: ... 
 } 
``` 

#### PATCH
```
{ 
   username: ... 
   textEnabled: ... 
   emailEnabled: ... 
 } 
``` 
