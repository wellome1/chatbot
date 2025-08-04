from pluginBase import Plugin

class WelcomeSequence(Plugin):
    def __init__(self,
                 pluginName:str,
                 pluginDesc:str,
                 pluginTags:list[str],
                 triggerWords:list[str],
                 api:str,
                 function:callable=None,
                 overwrite:bool=False,
                 startBoot:bool=True,
    ):
        if function is None: function = self.welcomeSequence
        super().__init__(
            pluginName=pluginName,
            pluginDesc=pluginDesc,
            pluginTags=pluginTags,
            triggerWords=triggerWords,
            api=api,
            function=function,
            overwrite=overwrite,
            startBoot=startBoot
        )

    def welcomeSequence(self):
        quotesActive = False
        weatherActive = False

        for pluginKey, plugin in Plugin.pluginList.items():
            if plugin.pluginName == "QuotesPlugin" and not quotesActive:
                plugin.generateQuote("1")
                quotesActive = True
            if plugin.pluginName == "WeatherPlugin" and not weatherActive:
                plugin.getWeather(query=["australia", "sydney"])
                weatherActive = True

        if not quotesActive and not weatherActive:
            raise ValueError(f"Timing is wrong. Fix something up.")

        print("="*40)