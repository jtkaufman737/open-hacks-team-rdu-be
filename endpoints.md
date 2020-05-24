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

Can technically be empty 

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
   codes: [] ... // State abbreviation array 
 } 
``` 

## /subscribe/alerts 

#### PATCH
```
{ 
   textEnabled: ... 
   emailEnabled: ... 
 } 
``` 

## /current/<state_code>

#### GET
```
{
    "state_code": ..., // 2 character state code
    "state_name": ..., // full textual state name
    "positive_tests": ..., // number of positive tests as of current date
    "total_tested": ..., // number of people tested ""
    "recovered": ..., // number of people recovered ""
    "deaths": ... // number of deaths ""
}
```

## /current/us

#### GET
```
{
    "positive_tests": ..., // number of positive tests as of current date
    "total_tested": ..., // number of people tested ""
    "recovered": ..., // number of people recovered ""
    "deaths": ... // number of deaths ""
}
```

## /current/states

#### GET
```
[  // returns array of state data objects
    {
        "state_code": ..., // 2 character state code
        "state_name": ..., // full textual state name
        "positive_tests": ..., // number of positive tests as of current date
        "total_tested": ..., // number of people tested ""
        "recovered": ..., // number of people recovered ""
        "deaths": ... // number of deaths ""
    }
]
```

## /user

#### GET 

```
{
    "password": "pbkdf2:sha256:150000$UEdUCHcA$1b65a0482c2f7c7373562003d63f1290276620e780e91fb54126e7570e7d8dcc",
    "phone": "9195924799",
    "subscriptions": [
        "AZ",
        "HI",
        "NJ"
      ],
      "username": "abc123"
},
```
