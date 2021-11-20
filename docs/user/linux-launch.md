This page present sequence of actions to run bot.

***

###Settings

**To configure bot:**

Before starting the bot launch go to the directory and set up a configuration file that includes tokens for 
the bot and tables, as well as additional options for them and chats.

To do it go to the sources directory and write **settings.ini** in sources by 
[**setting.ini.example**](https://github.com/rserdyukov/proctoring-bot/tree/main/sources/setting.ini.example). 
The proctoring bot's root directory might look like this:

```
proctoring-bot
└─ sources/
   ├─ settings.ini.example
   ├─ settings.ini                     //configured settings.ini.example
   └─ tokens/
      ├─ auth_token.json
      ├─ works_token.json
      └─ tests_token.json
```

The directory [**source/tokens**](https://github.com/rserdyukov/proctoring-bot/tree/main/sources/tokens) 
contains Google spreadsheets tokens.

The config file might look like this:

```
[Bot]
token=bot_token                        //proctoring bot token

[Chat]
timeout=0                              //auth expectation timeout value

[Spreadsheet]                          //spreadsheet ids and tokens
auth_id=auth_sp_id
auth_token=tokens/auth_token.json

works_id=works_sp_id
works_token=tokens/works_token.json

tests_id=tests_sp_id
tests_token=tokens/tests_token.json
```

*Options are used at the level of the bot program implementation.*

***

###Launch

**To run bot on Linux:**

```shell
cd scripts
./run_bot.sh
```

**To run bot on any operating system:**

```shell
pip3 install -r scripts/requirements.txt
cd sources
python3 main.py
```

***