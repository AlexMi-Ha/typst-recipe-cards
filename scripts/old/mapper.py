import json
import os
import argparse
import re

LINK_PATTERN = re.compile("\[\[([^\[\]]+)\]\]")

class Recipe:
    def __init__(self, title:str, tags: list[str], category:str, grouping:str, prep_time:str, cook_time:str, servings:int, source_url:str, last_modified:str, ingredients: list[str], steps: list[str], hints: list[str]):
        self.title = title
        self.tags = tags
        self.category = category
        self.grouping = grouping
        self.prep_time = prep_time
        self.cook_time = cook_time
        self.servings = servings
        self.source_url = source_url
        self.last_modified = last_modified
        self.ingredients = ingredients
        self.steps = steps
        self.hints = hints

    def setKey(self, categoryId:str, groupingId:str):
        self.key = f'{categoryId.capitalize()}-{groupingId.capitalize()}-{self.title[0].upper()}'

    def replaceLinks(self):
        def handleLinkMatch(match: re.Match[str]):
            assert(len(match.groups()) == 1)
            fileName = match.groups()[0].strip()
            linkedRecipe = RECIPE_FILE_NAME_TO_RECIPE_MAPPER[fileName]
            return f"{linkedRecipe.title} (ref. {linkedRecipe.key})"

        for i in range(len(self.ingredients)):
            if not self.__stringHasLink(self.ingredients[i]):
                continue
            self.ingredients[i] = LINK_PATTERN.sub(handleLinkMatch, self.ingredients[i])
        for i in range(len(self.steps)):
            if not self.__stringHasLink(self.steps[i]):
                continue
            self.steps[i] = LINK_PATTERN.sub(handleLinkMatch, self.steps[i])
        for i in range(len(self.hints)):
            if not self.__stringHasLink(self.hints[i]):
                continue
            self.hints[i] = LINK_PATTERN.sub(handleLinkMatch, self.hints[i])

    def containsLinks(self):
        return self.__collectionHasLink(self.ingredients) or self.__collectionHasLink(self.steps) or self.__collectionHasLink(self.hints)

    def __collectionHasLink(self, list: list[str]):
        for item in list:
            if self.__stringHasLink(item):
                return True
        return False
    
    def __stringHasLink(self, line: str):
        return bool(LINK_PATTERN.search(line))

    def to_json(self):
        return self.__dict__

class RecipeParser:

    def __init__(self, path):
        self.path = path

        self.properties = {}
        self.properties['tags'] = []
        self.ingredients = []
        self.steps = []
        self.hints = []

        self.linePointer = 0

        with open(path, "r") as file:
            self.lines = file.readlines()

    def __getCurrentLine(self):
        val = self.lines[self.linePointer].strip()
        while len(val) == 0 and not self.__eof():
            self.__next()
            val = self.lines[self.linePointer].strip()
        return val

    def __lineEquals(self, equals: str):
        return self.__getCurrentLine() == equals.strip()
    
    def __lineStartsWith(self, startsWith: str):
        return self.__getCurrentLine().startswith(startsWith)        

    def __next(self):
        if(self.__eof()):
            raise Exception(f"Cannot move line pointer. Reached EOF in {self.path}!")
        self.linePointer +=1

    def __eof(self):
        return self.linePointer >= len(self.lines) - 1

    def parse(self) -> Recipe:
        assert(self.__lineEquals('---'))
        self.__next()
        self.__parseProperties()
        self.__assertRequiredProperties()

        assert(self.__lineStartsWith('# ')) # title
        self.__next()
        assert(self.__lineEquals('## Zutaten'))
        self.__parseIngredients()

        assert(self.__lineEquals('## Schritte'))
        self.__parseSteps()

        assert(self.__lineEquals('## Hinweise'))
        self.__parseHints()

        return Recipe(
            self.properties['title'],
            self.properties['tags'],
            self.properties['category'],
            self.properties['grouping'],
            self.properties['prep_time'],
            self.properties['cook_time'],
            int(self.properties['servings']),
            self.properties.get('source_url', ''),
            self.properties.get('last_modified', ''),
            self.ingredients,
            self.steps,
            self.hints
        )

    def __parseProperties(self):
        while not self.__lineEquals('---'):
            if self.__lineStartsWith('tags:'):
                pass
            elif self.__lineStartsWith('-'):
                self.properties['tags'].append(self.__getCurrentLine()[2:])
            else:
                lineComponents = self.__getCurrentLine().split(':', 1)
                if len(lineComponents) != 2:
                    print(f"Error in {self.path}. Could not read line {self.__getCurrentLine()}")
                    continue
                self.properties[lineComponents[0]] = lineComponents[1].strip().strip('"')
            self.__next()

        assert(self.__lineEquals('---'))
        self.__next()

    def __assertRequiredProperties(self):
        assert('title' in self.properties)
        assert('category' in self.properties)
        assert('grouping' in self.properties)
        assert('servings' in self.properties)
        assert('prep_time' in self.properties)
        assert('cook_time' in self.properties)

    def __parseIngredients(self):
        assert(self.__lineEquals('## Zutaten'))
        self.__next()
        while self.__lineStartsWith('-') or self.__lineStartsWith('###'):
            line = self.__getCurrentLine()
            if self.__lineStartsWith('### '):
                line = '===' + line[3:]
            self.ingredients.append(line)
            self.__next()

        assert(self.__lineStartsWith('## '))
    
    def __parseSteps(self):
        assert(self.__lineEquals('## Schritte'))
        self.__next()
        currentStep = 1
        while not self.__lineStartsWith('## '):
            if self.__lineStartsWith(str(currentStep) + '.'):
                line = self.__getCurrentLine()
                line = '+' + line[2:]
                self.steps.append(line)
                currentStep += 1
            else:
                if len(self.steps) == 0:
                    self.steps.append('')
                self.steps[len(self.steps) - 1] += '\n' + self.__getCurrentLine()
            
            self.__next()
        
        assert(self.__lineStartsWith('## '))

    def __parseHints(self):
        assert(self.__lineEquals('## Hinweise'))
        self.__next()

        while not self.__lineStartsWith('## ') and not self.__eof():
            self.hints.append(self.__getCurrentLine())
            self.__next()

def searchRecipes(parentDir: str) -> list[str]:
    marker = '<!-- MARKER FOR MAPPER SCRIPT -->'
    foundFiles = []
    for root, _, files in os.walk(parentDir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.read().splitlines()
                        if lines and lines[-1].strip() == marker:
                            foundFiles.append(filepath)
                except Exception as e:
                    print(f"Could not read {filepath}: {e}")
    
    return foundFiles

BUFFER_OF_RECIPES_WITH_LINKS = []
RECIPE_FILE_NAME_TO_RECIPE_MAPPER = {}

def parseRecipes(recipeFiles: list[str]) -> list[Recipe]:
    parsedRecipes = []
    for recipeFile in recipeFiles:
        parser = RecipeParser(recipeFile)
        recipe = parser.parse()
        parsedRecipes.append(recipe)
        recipeFileName = os.path.splitext(os.path.basename(recipeFile))[0]
        RECIPE_FILE_NAME_TO_RECIPE_MAPPER[recipeFileName] = recipe
        if(recipe.containsLinks()):
            BUFFER_OF_RECIPES_WITH_LINKS.append(recipe)
    return parsedRecipes

def groupByCategory(recipes: list[Recipe]) -> dict[str, list[Recipe]]:
    categories: dict[str, list[Recipe]] = {}
    for recipe in recipes:
        if recipe.category not in categories:
            categories[recipe.category] = []
        categories[recipe.category].append(recipe)

    for category in categories:
        recipes = categories[category]
        recipes.sort(key=lambda r: (r.grouping, r.title))

    return categories

def calculateIds(recipesByCategory: dict[str, list[Recipe]]):
    categoryIdMapper = getUniqueIdsFromSet(recipesByCategory.keys())

    for category in recipesByCategory:
        distinctGroupings = []
        for recipe in recipesByCategory[category]:
            if recipe.grouping not in distinctGroupings:
                distinctGroupings.append(recipe.grouping)
        
        groupingIdMapper = getUniqueIdsFromSet(distinctGroupings)

        for recipe in recipesByCategory[category]:
            recipe.setKey(categoryIdMapper[recipe.category], groupingIdMapper[recipe.grouping])


def getUniqueIdsFromSet(setOfFullNames: list[str]):
    idMapper = {}
    for item in setOfFullNames:
        idSplitPointer = 1
        while item[:idSplitPointer] in idMapper:
            oldId = item[:idSplitPointer]
            idSplitPointer += 1
            oldItem = idMapper[oldId]
            if idSplitPointer > len(oldItem):
                raise Exception(f"Cannot get unique identifiers from set. Conflict between '{oldItem}' and '{item}'")
            
            newId = oldItem[:idSplitPointer]
            idMapper.pop(oldId)
            idMapper[newId] = oldItem
        
        if idSplitPointer > len(item):
            raise Exception(f"Cannot get unique identifiers from set. Conflict at '{item}'")
        
        idMapper[item[:idSplitPointer]] = item
    
    return dict((v, k) for k, v in idMapper.items())

def processObsidianLinks():
    for recipe in BUFFER_OF_RECIPES_WITH_LINKS:
        recipe.replaceLinks()

def exportCategories(categories: dict[str, list[Recipe]], outPath: str):
    for category in categories:
        recipes = categories[category]
        filename = os.path.join(outPath, category + '.json')
        print(f'Writing {category} to {filename}')
        jsonContent = json.dumps([f.to_json() for f in recipes], indent=2)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(jsonContent)

def parseArgs():
    parser = argparse.ArgumentParser(description="Mapper script")
    parser.add_argument("-i", "--input", required=True, help="Parent path where the recipe markdown files are located")
    parser.add_argument("-o", "--output", required=True, help="Output path for recipe json files")

    return parser.parse_args()
    
if __name__ == '__main__':
    args = parseArgs()
    inPath = args.input
    outPath = args.output

    print('Welcome to the Obsidian to Typst Recipe converter!')
    print('Searching for recipes...')
    recipeFiles = searchRecipes(inPath)
    print(f'Found {len(recipeFiles)} recipe files!')
    for recipe in recipeFiles:
        print(f'\t{os.path.basename(recipe)}')
    
    print('Parsing the recipes...')
    recipeModels = parseRecipes(recipeFiles)
    categories = groupByCategory(recipeModels)
    print(f'Parsed and grouped by {len(categories.keys())} categories!')
    print('Generating IDs...')
    calculateIds(categories)
    processObsidianLinks()
    print(f'Exporting json files to {outPath}...')
    exportCategories(categories, outPath)