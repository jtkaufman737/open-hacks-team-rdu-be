# coronAlert back end api 

This application was borne out of the idea that it is challenging for those of us with loved ones spread around the globe to keep track of coronavirus cases. We wanted something to allow us to get the numbers on cases, recoveries, and fatalities in one place.

The application has the ability for a user to create customizable alerts, so that in addition to a US wide map they can track the specific statistics in states where their loved ones live.

Our backend API utilizes Flask, Mongo, and the Twilio API to give users personalized alerts for states that their loved ones live in so they can stay up to date on the lateset news. 

Here's an example text: 

![image]('Image from iOS (3).jpg' "Twilio alert")

# To run the app locally 

- select git clone, clone this repo locally
- `cd open-hacks-team-rdu-be` 
- If you wish, you can activate a virtual environment before installing dependencies 
- `pip -r install requirements.txt` 
- Reach out to the team and we can provide the .env files necessary to make this app run - it is bad security to commit them to a repo 
and until the last minute we thought we would have time to deploy this for you live, but hit an unexpected last minute technical 
snag in our deployment and running locally was the next best option we could come up with. We can pass the env files to you or demo 
from one of our computers. We're sorry for the technical difficulty but really hope this doesn't interfere with our opportunity to be 
judged 
- run `flask run` and the frontend will be able to interact with the API 

# Future Improvements 

To keep the app relevant, we intend to:

    Add vaccination information when one becomes available
    Add other countries! The APIs exist, we just didn't have time to build logic for them all in this hackathon

