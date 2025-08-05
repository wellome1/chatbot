from pluginBase import Plugin
import json; import os

class LegalReviewPlugin(Plugin):
    def __init__(self,
                 pluginName:str,
                 pluginDesc:str,
                 pluginTags:list[str],
                 triggerWords:list[str],
                 api=None,
                 function:callable=None,
                 overwrite:bool=False,
                 startBoot:bool=False
                 ):
        if function is None: function = self.getResponse
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

        legalCases = os.path.join(os.path.dirname(__file__), "legalStudiesCases.json")

        with open(legalCases, "r", encoding="UTF-8") as f:
            self.legalStudies = json.load(f)


    def getResponse(self, query):
        pass

    def reviewCases(self, case):
        pass

    def getImpact(self, case):
        pass

    def getAnalysis(self, case):
        pass
