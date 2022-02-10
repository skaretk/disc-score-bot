# disc-score-bot

Scorebot for uDisc

Will store .csv files uploaded and responds to commands in order to view these in the discord channel!

Currently supported commands:



%scores
> Lists all scorecards and total scores

%scores list course
> List all courses stored

%scores list date
> Lists all dates for scorecards

%scores get course coursename
> Get all scorescards for the coursename

%scores get date 01.12.1990
> Search for all scorecards with given date

%scores get date 01.12.1990 01.01.1991
> Search for all scorecards between dates

%files
> Lists files stored in the channel


Get started:

Based on guide posted here: https://realpython.com/how-to-make-a-discord-bot-python/

1. Setup a new bot from the guide
2. Install python from python.org
3. Install nextcord (pip install -U nextcord)
4. Install python-dotenv (pip install python-dotenv)
5. Create a file called 'token.env' in the root folder and add the token generated from the guide referenced above.
