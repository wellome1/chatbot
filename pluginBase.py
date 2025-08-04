import re

class Plugin:
    """
    pluginList: Here just so I can keep track of what plugins exist and are implemented on file launch.

    # def __init__...: Just making sure stuff gets done. Explanation:
    self.pluginName = pluginName; self.pluginDesc... - Just to make sure the instance has callable stuff.

    ## Why "self.triggerWords" and "self.loweredTriggers"?
    Just because, "self.triggerWords" is to make sure it looks better when I'm listing everything. "self.loweredTriggers" is what the code itself uses. It stops me from remaking that exact thing every time I check tags.

    ## self.function
    Pretty much:
    It'll be the function passed to function through IF one is given. If none is given, the code defaults it to the boolean None. When self.function gets assigned a value in the code, it'll be the function if it's something other than bool(None). If it is bool(None), it'll be the "functionNotImplemented" command, which just raises an error.
    Am I expecting it to happen often? Yes. Absolutely.

    ## self.register(overwrite)
    "overwrite" is almost always going to be False. If I want to change something, it'll be in the code, not mid-session. I might add that functionality, but it's more of a "Maybe I'll do it" than "This is planned". The "register" command does the following:
    1. Checks if self.pluginName is in Plugin.pluginList. Stops me from overwriting all the time.
    2. If it is, checks if overwrite is False. If it is, it raises a ValueError. I don't want me code constantly reinitialising plugins.
    3. If it isn't (of if overwrite isn't False), it'll check that self.pluginName isn't in Plugin.pluginList. This is more of a precaution, I doubt it's necessary. If it is in Plugin.pluginList, it'll overwrite it if overwrite=True.
    4. If somehow, it gets to the "else", then it just causes an error, which forces me to question just HOW it got to this point.

    # def __str__(self):
    This is pretty simple. It makes a variable called "pluginTags", which just makes the tags readable.

    Then, it gives the output of f"{self.pluginName}: {self.pluginDesc}\npluginTags:\n{pluginTags}\n\n". In depth:
    f"" - The f-string. My favourite thing, allows for inline variable by using the {}.
    {self.pluginName}: {self.pluginDesc} - This will be something like "Greetings: Gives greetings"
    \n - New line! Makes it more readable.
    pluginTags:\n - States "pluginTags" in the code, then puts a new line.
    {pluginTags} - The thing we made before, showing the now-readable tags.
    \n\n - I'm expecting this to be used in mass with other plugins. It needs a bit of a break, no?

    # def functionNotImplemented(self):
    Literally just returns an error. That's all it's there for.

    # def handleCheck(self, tokens):
    It's one line, but does a lot in one line.
    "any()" - Returns a boolean depending on if what's inside returns as true. It's like doing a loop and checking if it ever becomes true.
    "token.lower() in self.loweredTags for token in tokens" - Now this is an actual loop. This just loops it so it'll always check. It's pretty much doing: Q: "What's the weather?", then doing:
    is "what's" in self.loweredTags? No, okay, next token.
    is "the" in self.loweredTags? No, okay, next token.
    is "weather" in self.loweredTags? Yes, okay, return "True".

    It stops the checking as SOON as it gets a True and returns False otherwise. I think. I didn't code Python, I dunno.

    # def handle(self)
    First, it checks "self.function" and makes sure it exists (it always should, it's just a precaution). Then, it runs self.function.

    If, somehow through an intervention by God, self.function doesn't exist, it returns the NotImplementedError, making me question how the hell you did that.

    # def register(self, overwrite=False)
    I went through it before in the def __init__ section.
    ***
    # To any fellow Python developers reading this, no, I won't stop using camelCase. I've used it too much to stop. I have a problem. Is there a camelCase Anonymous group I can join?
    """
    pluginList = {}

    def __init__(self,
                 pluginName:str,
                 pluginDesc:str,
                 pluginTags:list[str],
                 triggerWords:list[str],
                 api,
                 function=None,
                 overwrite=False,
                 startBoot = None
        ):

        self.pluginName = pluginName
        self.pluginDesc = pluginDesc
        self.pluginTags = pluginTags
        self.triggerWords = triggerWords
        self.loweredTriggers = {trigger.lower() for trigger in triggerWords}
        self.api = api
        self.function = function if function is not None else self.functionNotImplemented

        self.startBoot = startBoot if startBoot is not None else False

        self.register(overwrite)

    def __str__(self):
        pluginTags = "".join(f"{pluginTag}\n" for pluginTag in self.pluginTags)
        triggers = "".join(f"{trigger}\n" for trigger in self.triggerWords)

        return f"{self.pluginName}: {self.pluginDesc}\npluginTags:\n{pluginTags}\ntriggers:{triggers}\n\n"

    def functionNotImplemented(self, query=None, *args, **kwargs):
        print(f"Not implemented. Args: {args}, kwargs: {kwargs}. Query: {query}.")
        raise NotImplementedError("This method is not implemented. Using default 'Plugin' class, fix the error.")

    def handleCheck(self, query):
        tokens = re.findall(r'\b\w+\b', query.lower())
        return sum(token.lower() in self.loweredTriggers for token in tokens)

    def handle(self, query=None, queryHandle=False):
        if self.function:
            if queryHandle and query is not None:
                return self.function(query=query)
            else: return self.function()
        else:
            raise NotImplementedError("This is a weird bug. How did you manage this ???")

    def register(self, overwrite=False):
        if self.pluginName in self.pluginList and not overwrite:
            raise ValueError("This plugin is already registered.")
        elif self.pluginName not in self.pluginList or overwrite:
            self.pluginList[self.pluginName] = self
        else:
            raise ValueError("How... How did you manage THIS???")

    def queryParse(self, query):
        queryList = []

        if isinstance(query, list):
            parts = query
        else:
            parts = re.split(r'[,\s]+', query.lower())

        for part in parts:
            if part.isdigit():
                queryList.append(part)
                continue
            tokens = re.findall(r'\b\w+\b', part)
            if tokens:
                queryList.extend(tokens)

        return queryList