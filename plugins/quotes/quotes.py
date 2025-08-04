from pluginBase import Plugin; from random import choice
import json; import os


class QuotesPlugin(Plugin):
    def __init__(self,
                 pluginName: str,
                 pluginDesc: str,
                 pluginTags: list[str],
                 triggerWords: list[str],
                 api=None,
                 function=None,
                 overwrite: bool = False
                 ):
        if function is None: function = self.generateQuote
        super().__init__(
            pluginName=pluginName,
            pluginDesc=pluginDesc,
            pluginTags=pluginTags,
            triggerWords=triggerWords,
            api=api,
            function=function,
            overwrite=overwrite
        )

        characterStartFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'characterStart.json')
        with open(characterStartFile, 'r', encoding="UTF-8") as f:
            self.characterStart = json.load(f)

        self.quotes = {}
        for key, value in self.characterStart.items():
            filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'characters', value[1])
            with open(filepath, "r", encoding="utf-8") as f:
                self.quotes[key] = json.load(f)

    def generateQuote(self, query):
        amount = 1
        character = None
        tags = None

        parts = self.queryParse(query)

        if parts[0] == "check":
            amountFound = {}
            for tag in parts[1:]:
                for character in self.quotes:
                    if tag not in amountFound:
                        amountFound[tag] = {}
                    amountFound[tag][character] = 0
                    for key, value in self.quotes[character].items():
                        if tag in value["tags"]:
                            amountFound[tag][character] = amountFound[tag][character] + 1

                for character, amount in amountFound[tag].items():
                    print(f"{self.characterStart[character]} has {amount} quotes with tag {tag}.")
            return
        if parts[0] == "analysis":
            if len(parts) >= 2 and parts[1] in self.characterStart:
                character = parts[1]
            elif len(parts) >= 2 and parts[1] not in self.characterStart:
                tags = parts[1:]

            if len(parts) >= 3 and parts[2] in self.characterStart:
                tags = parts[2:]

            chosenChar = character or choice(list(self.quotes.keys()))
            quotePool = list(self.quotes[chosenChar].keys())

            if tags:
                filteredQuotes = []
                for key, value in self.quotes[chosenChar].items():
                    if any(tag in value["tags"] for tag in tags):
                        filteredQuotes.append(key)

                if not filteredQuotes:
                    print(f"Filtered quotes for {chosenChar} (using tags {tags}) is empty.")
                    return

                quotePool = filteredQuotes

            chosenQuote = choice(quotePool)
            analysis = self.quotes[chosenChar][chosenQuote]['analysis']
            tags = self.quotes[chosenChar][chosenQuote]['tags']

            print(f"{self.characterStart[chosenChar]} says:\n\"{chosenQuote}\"\nAnalysis: {analysis}")
            print("Tags:")
            for tag in tags: print(f"- {tag}")
            return

        if parts[0].isdigit():
            amount = int(parts[0])

        if len(parts) >= 2 and parts[1] in self.characterStart:
            character = parts[1]
        elif len(parts) >= 2 and parts[1] not in self.characterStart:
            tags = parts[1:]

        if len(parts) >= 3 and parts[2] in self.characterStart:
            tags = parts[2:]

        for _ in range(amount):
            if character:
                quotePool = list(self.quotes[character].keys())

                if tags:
                    filteredQuotes = []
                    for key, value in self.quotes[character].items():
                        if any(tag in value["tags"] for tag in tags):
                            filteredQuotes.append(key)

                    if not filteredQuotes:
                        print(f"Filtered quotes for {character} (using tags {tags}) is empty.")
                        return

                    quotePool = filteredQuotes

                print(f"{self.characterStart[character]} says:\n\"{choice(quotePool)}\"")

            else:
                chosenChar = character or choice(list(self.quotes.keys()))
                quotePool = list(self.quotes[chosenChar].keys())

                if tags:
                    filteredQuotes = []
                    for key, value in self.quotes[chosenChar].items():
                        if any(tag in value["tags"] for tag in tags):
                            filteredQuotes.append(key)

                    if not filteredQuotes:
                        print(f"Filtered quotes for {chosenChar} (using tags {tags}) is empty.")
                        return

                    quotePool = filteredQuotes

                print(f"{self.characterStart[chosenChar]} says:\n\"{choice(quotePool)}\"")
