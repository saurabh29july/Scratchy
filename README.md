## Scratchy

**A simple cisco spark chatbot.**

Scratchy is a simple chat bot that from out-of-box corpus just knows how to say hello!

@scratchy #help

    Hi! I'm Scratchy, your scratchpad for cheatsheets, notes etc etc.

    @scratchy Hi - Talk to me!
    
    #help - See this again!
    #note <tag(s)> | <note>  - Note it down with , seperated tag(s)
    #del <tag> - Delete notes with tag
    #list - List all or #list <tag> notes

_**What Scratchy does?**_
*   Integrates with Cisco Spark
*   Provides a blank corpus of hello/hi which can be used to build one's own scratchpad.
*   Json based corpus file makes Scratchy restart safe & also use corpus for different purposes.
*   No AI/ML for now.

_**Run Scratchy**_
>Clone this repository

>pip install requirements.txt

>Add Cisco Spark Bot Details in scratchy.py for email, accessToken & roomId

>python scratchy.py

To use this bot or more details on integration visit my blog http://saurabh29july.blog/building-a-simple-cisco-spark-chatbot.
