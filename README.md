Read pluginBase.py's comments if you want to know the basics of how to make your own plugins.
***
But, a nice little summary:
1. Know what you're trying to do.
2. Make a basic class.
3. Put the arguments into intents.json (main.py will automatically import it and make a class, don't worry).
4. Write what you want your plugin to do inside handle().
***
If you want to have multiple commands in a single plugin, you can use the "query" argument, which will be automatically passed through if you put it there, to do a match-case to figure out what command to do.

Example:
```python
match query:
    case "generate": ...
    case "check": ...
```
You get the point.

I’ve not done this yet, because I’m not bothered.
But it’s a way to make your plugin bigger and easier to read than what I did in /plugins/quotes/quotes.py — generateQuote().

Have fun.
There’s a few issues that’ll start appearing once you get to ~50 plugins, but I have no intentions of getting there (yet), so you can fix it yourself.
***

Can it run on its own? Yeah.

But can it do much on its own? Not really. It can only pick quotes you give it and say hi.
That’s where boredom comes in — you can theoretically make any plugin you want.
It’s just putting it into practice, debugging it, making sure the trigger words don't overlap too much, etc etc.

-A high school student who was bored one weekend.