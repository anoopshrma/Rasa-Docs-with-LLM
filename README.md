# Rasa-Docs-with-LLM
Connecting Rasa Docs using LlamaIndex to LLM for creating a bot that can answer user queries based on the Rasa Documentation.

# Need for this project/ Usecase for Rasa
Rasa is a great platform for building chatbots but I found two issues on the Platform which were
- Users asking basic and similar questions again and again on the rasa forum which reduces the chance for looking at the good and new issues.
- On the official Rasa documentations we have to search for the exact thing we are looking for which sometimes can be hard. As sometimes user is not quite sure what he is looking for.
## Solution
To tackle both the issues, We can deploy a Rasa bot which will be up to date with the latest docs on forum as well as on the official Documentation. 
- User can ask their query to rasa bot if they want to setup rasa or create a bot using any connector or deployment related directly to our bot and get answer quickly on the forum. Thus saving time for Rasa moderator like me to answer real issues.
- On the official Docs, The bot can help user to guide for what they are actually looking for and provide details such as URL where they can find more about their query.

# Info
- This project is using OpenAI services. You will need to have a OpenAI dkey with you while running this.
- The demo is displayed using `Chainlit` which is the exact copy of the main code present in `main.py`.
- Rasa URLs have been added in `constants.py` file.
- You'll get the response along with the URL from which the response is coming from and sources from which the response has been framed. A sample is shown below.
  ![image](https://github.com/anoopshrma/Rasa-Docs-with-LLM/assets/26565263/202d97e8-6587-4f08-bd9a-b3e50c01aa5f)
- Currently I have added the indexes, So it will not create new indexes. If you wish to add more urls and test on them. You'll have to remove the Storage folder and add urls in `constants.py` and restart the server.

# Install the required dependencies
```
pip install requirements.txt
```

#  Run the project
```
uvicorn main:app
```
For checking out the swagger go to `BASE_URL/docs`. It will look like this.
  ![image](https://github.com/anoopshrma/Rasa-Docs-with-LLM/assets/26565263/f2285782-e928-42c4-bc90-51c90845ad8e)


# Demo
For Demo, I have used Chainlit for providing better UI to show the implementation. I have added the chainlit code as well. You can find it under `chainlit_app.py`.

