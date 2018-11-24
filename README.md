# JsonMerger
If you do regular backups of your data on Facebook (on JSON), you will find yourself with a lot of files ('message.json') with redundant messages. By doing so, you will be able to use it for your stats (link of the project).   

If you want to merge them *without duplicates*, this program is for you!  

To use it, you put your two JSON files as arguments, by typing the following command:  
`python jsonMerger.py foo bar`  
(where `foo` and `bar` are the JSON files you want to merge (e.g.: message1.json)).  

:warning: By running the command, a file called **message.json** will be created, where the program is. If it already exists, it will be overwritten!  

If you run the program without arguments, the default arguments are `message1.json` and `message2.json`.  
In other terms: `python jsonMerger.py` is equivalent to `python jsonMerger.py message1.json message2.json`.  

~~Hint: so far, you can merge only two files. Feel free to run this program in a loop where one of its arguments will be message.json.~~ 
Update: Now, you can merge as many files as you wish. For example, if you wish to merge five files from your monthly backups, you can type `python jsonMerger.py /home/pi/FacebookBackup/*/messages/inbox/yourFriend/message.json` (with a star) to select all the concerned files.  

Upcoming version: check number of messages to be sure there are no losses in certain cases.  
