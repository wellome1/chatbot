from pluginBase import Plugin
import requests

class WeatherPlugin(Plugin):
    def __init__(
            self,
            pluginName:str,
            pluginDesc:str,
            pluginTags:list[str],
            triggerWords:list[str],
            api:str,
            function:callable=None,
            overwrite:bool=False,
    ):
        if function is None: function = self.getWeather
        super().__init__(
            pluginName=pluginName,
            pluginDesc=pluginDesc,
            pluginTags=pluginTags,
            triggerWords=triggerWords,
            api=api,
            function=function,
            overwrite=overwrite
        )

    def getWeather(self, query=None):
        if query: queryParts = self.queryParse(query)
        else: queryParts = ["japan","tokyo"]

        partJoined = "+".join(queryParts[1:])
        queryPartsCopy = [queryParts[0], partJoined]

        # Assume queryParts[0] is the city. Ignore the rest. Trust in the user.
        response = requests.get(f"{self.api}{queryPartsCopy[0]}/{queryPartsCopy[1]}?format=3")
        print(response.text.strip())