## IDEA 
- Roomate tracking app using facebook (or Twitter or Insta or Tiktok depending on API availability) data to identify connections 
- Self tagging preferences - female roommate desired etc, and users can define tags. Unlimited tags and then we could match 
based on % of identical tags 
- Graph theory based on the social media data to extrapolate people with network connections 

## TOOLS 
- React frontend 
- Material UI for CSS 
- Sketch for images, or designers 
- Slack for keeping track of what we are working on 
- GCP for hosting 
- Axios 
- Hooks/Functional 
- Tentatively Mongo/Atlas for db 

## TASK BREAKDOWN (general) 
- Generate frontend with create react app
- Install Material 
- Agree on data models 
- Talk through the endpoints 
- Roberto can be point on React 
- I will float and work on whatever 
- Katy could help on frontend stuff based on what's left 

## MVP FUNCTIONALITY 
- User would have the ability to sign up/log in to the app 
- Home page could be a world heat map, and then below that cut out states 
- Ability to get text or email updates or both 
- We need recurring tasks to kick off the emails 
- Plotly heatmap - frontend and backend 
- Side menu with your subscriptions listed 

## BACKEND - ENDPOINTS 
- Sign up (POST)
- Login (POST) 
- Logout 
- /Location 
- /Subscribe post new user-location subscription add/delete etc 

## FRONTEND - COMPONENTS & PAGES 
- Sign up/login - Include blurb, add tags, sign into facebook 
- Home/Dashboard page - favoriting be an option from the card, same for email  
- About the product - Could be home page or the login page
- Side Nav 

## COLLECTIONS 
- Users 
  - name 
  - email 
  - password
  - array of state identifiers 
- State 
  - name 
  - ID 
  
