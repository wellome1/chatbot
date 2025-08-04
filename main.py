import json; import os
from typing import Optional; from dataclasses import dataclass
from pluginBase import Plugin; import importlib

@dataclass
class PluginScore:
    score: int = 0
    plugin: Optional[Plugin] | None = None


intentsFile = os.path.join('./intents.json')

with open(intentsFile, "r") as f:
    intents = json.load(f)

for pluginKey, plugin in intents.items():
    moduleName = f"plugins.{plugin['filename']}.{plugin['filename']}"
    module = importlib.import_module(moduleName)

    className = getattr(module, plugin['pluginName'])

    instance = className(**plugin['arguments'])

while True:
    query = input("> ")
    savedQuery = None
    if query == "exit":
        break

    if "|" in query:
        querySections = query.split("|")
        savedQuery = querySections[1]
        query = querySections[0]

    pluginHandleCapability = {}
    for pluginKey, plugin in Plugin.pluginList.items():
        handleCapability = plugin.handleCheck(query)
        if handleCapability > 0:
            pluginHandleCapability[plugin] = handleCapability

    maxPossibleVal = len(query.split())
    maxVal = PluginScore()
    for plugin, score in pluginHandleCapability.items():
        if score > maxVal.score:
            maxVal.score = score
            maxVal.plugin = plugin
            if score == maxPossibleVal:
                break

    if isinstance(maxVal.plugin, Plugin):
        if savedQuery is not None:
            maxVal.plugin.handle(query=savedQuery, queryHandle=True)
        else:
            maxVal.plugin.handle()
    else:
        raise ValueError(f"There is no plugin for query: {query}")
