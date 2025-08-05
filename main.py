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

for pluginKey, plugin in Plugin.pluginList.items():
    if plugin.startBoot:
        plugin.handle()

recallActive = False
recallPlugin = None

while True:
    query = input("> ")
    savedQuery = None

    if query == "exit":
        break

    if "|" in query:
        if query == "| exit":
            recallActive = False
            print("Recall is now off.")
            continue
        querySections = [section.strip() for section in query.split("|")]
        savedQuery = querySections[1:]
        query = querySections[0]

        if recallActive:
            query = [query] + savedQuery

    if not recallActive:
        if query.startswith("recall"):
            parts = query.split()
            if len(parts) >= 2:
                pluginToRecall = parts[1]
                if pluginToRecall in Plugin.pluginList:
                    recallPlugin = Plugin.pluginList[pluginToRecall]
                    recallActive = True
                    print(f"Recall is now on for plugin '{pluginToRecall}'.")
                    continue
                else:
                    print(f"Could not find plugin '{pluginToRecall}'.")
                    continue
            else:
                print("Please specify a plugin to recall.")
                continue

    if not recallActive:
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

    elif recallActive:
        if isinstance(recallPlugin, Plugin):
            if query is not None:
                recallPlugin.handle(query=query, queryHandle=True)
            else:
                recallPlugin.handle()