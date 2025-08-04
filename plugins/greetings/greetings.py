from pluginBase import Plugin
from random import choice

class GreetingPlugin(Plugin):
    def __init__(self,
                 pluginName:str,
                 pluginDesc:str,
                 pluginTags:list[str],
                 triggerWords:list[str],
                 greetings:list[str],
                 api:str,
                 function=None,
                 overwrite:bool=False
        ):
        if function is None: function = self.greetUser
        super().__init__(
            pluginName=pluginName,
            pluginDesc=pluginDesc,
            pluginTags=pluginTags,
            triggerWords=triggerWords,
            api=api,
            function=function,
            overwrite=overwrite
        )

        self.greetings = greetings

    def __str__(self):
        pluginTags = "".join(f"{pluginTag}\n" for pluginTag in self.pluginTags)
        greetings = "".join(f"{greeting}\n" for greeting in self.greetings)
        triggers = "".join(f"{trigger}\n" for trigger in self.triggerWords)

        return f"{self.pluginName}: {self.pluginDesc}\nGreetings:{greetings}\npluginTags:\n{pluginTags}\ntriggers:{triggers}\n\n"

    def greetUser(self):
        return choice(self.greetings)