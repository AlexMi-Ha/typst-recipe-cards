import json
import os
import argparse

class Recipe:
    def __init__(self, title:str, category:str, grouping:str, servings:int, prep_time:str, cook_time:str, ingredients: list[str], steps: list[str]):
        self.title = title
        self.category = category
        self.grouping = grouping
        self.servings = servings
        self.prep_time = prep_time
        self.cook_time = cook_time
        self.ingredients = ingredients
        self.steps = steps

    def to_json(self):
        this = self.__dict__
        this.pop('category')
        this['ingredients'] = '\n'.join(self.ingredients)
        this['steps'] = '\n'.join(self.steps)
        return this

class RecipeParser:

    def __init__(self, path):
        self.path = path

        self.properties = {}
        self.ingredients = []
        self.steps = []

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

        return Recipe(
            self.properties['title'],
            self.properties['category'],
            self.properties['grouping'],
            int(self.properties['servings']),
            self.properties['prep_time'],
            self.properties['cook_time'],
            self.ingredients,
            self.steps
        )

    def __parseProperties(self):
        while not self.__lineEquals('---'):
            if self.__lineEquals('tags:'):
                self.properties['tags'] = []
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

def parseRecipes(recipeFiles: list[str]) -> list[Recipe]:
    parsedRecipes = []
    for recipe in recipeFiles:
        parser = RecipeParser(recipe)
        parsedRecipes.append(parser.parse())
    return parsedRecipes

def groupByCategory(recipes: list[Recipe]) -> dict[str, list[Recipe]]:
    categories: dict[str, list[Recipe]] = {}
    for recipe in recipes:
        if recipe.category not in categories:
            categories[recipe.category] = []
        categories[recipe.category].append(recipe)
    return categories

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
    print(f'Exporting json files to {outPath}...')
    exportCategories(categories, outPath)