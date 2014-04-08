#############################
# Author: Michael Albert    #
#           alberm4@rpi.edu #
# Release Date: 04/08/14    #
# Name: Helicase            #
# Version: Alpha 2          #
#   added "vetted" system   #
#############################

import urllib, re, time, os, random

prepositions = {'of', 'to', 'with', 'in', 'and'}
disclude = {'xxx'}
vowels = {'a','e','i','o','u'}
ingredients = dict()
recipelist = dict()
vetted = set()

#User directory info
usersaves = ""
recipedir = ""

#####################################
def makeSingular(ingredient):
    '''Returns the singular form of the input word'''
    
    if len(ingredient) < 3:
        return ingredient
    if len(ingredient) > 3:
        if ingredient[-3:] == 'ies':
            return ingredient[:-3]+'y'
        if ingredient[-2:] == 'es':
            if (ingredient[-3] in vowels and ingredient[-3] != 'u') or (ingredient[-4:-2] == 'sh'):
                return ingredient[:-2]
            if ingredient[-3] not in vowels and ingredient[-4] in vowels:
                return ingredient[:-1]
    if ingredient[-1] == 's' and ingredient[-2] != 's':
        return ingredient[:-1]
    return ingredient
    
def mapsTo(value):  
    '''Returns the wellness of the ingredient pair'''

    if value >= 50:
        return 100
    else:
        return int((value/50)*100)
    
def delete(regex, string):
    '''Delete all instances of the characters in the regex from string
        return -> the stripped string'''

    string = re.compile('[%s]' % re.escape(regex)).sub('',string)
    
    return string

def ridOf(string, regex):
    '''Discards words in string* greater than length*
        return -> the string with discarded words'''

    if string:
        string = re.compile(regex).sub(" ", string)

    return string

def stripPunctuation(string):
    '''Strips some non alphanumeric characters from a string
       return -> the stripped string'''

    return delete("\/\*\\\'\"\?\:\.\;\_\[\]\|\%", string)

def splitCombinatories(string):
    '''Splits a string at and's and or's
        return -> the split string'''

    if string:
        string = re.compile(" and | or | \& ").sub("\n", string)

    return string

def delete(regex, string):
    '''Delete all instances of the characters in the regex from string
        return -> the stripped string'''

    string = re.compile('[%s]' % re.escape(regex)).sub('',string)
    
    return string

def fileList(filename):
    '''Takes a recipe file and extracts valid lines
       return -> the lines of the recipe'''

    thefile = open(filename, 'r')
    get = True
    lines = []
    
    while get:
        get = False
        line = thefile.readline()
        if line != '':
            line = stripPunctuation(line)
            line = ridOf(line.lower(), "(( jar(s)* )|( gallon(s)* )|( bottle(s)* )|( dash(es)* )|( pinch(es)* )|( sheet(s)* )|( loa(f)*(ves)* )|( box(es)* )|( stalk(s)* )|( clove(s)* )|(-)|( stick(s)* )|( pod(s)* )|( (c)*(m)*(s)* )|( (centi)*(milli)*meter(s)* )|( f(ee)*(oo)*t )|( (centi)*(milli)*liter(s)* )|( (c)*(m)*l(s)* )|( a )|(\d)|( pint(s)* )|( quart(s)* )|( package )|( sized )|( size )|( g(s)* )|( kg(s)* )|( bunch(es)* )|( container(s)* )|( head(s)* )|( inch(es)* )|( slice(s)* )|( package(s)* )|( can(s)* )|( cup(s)* )|( tbs )|( tsp(s)* )|( teaspoon(s)* )|( tablespoon(s)* )|(\((.*)\))|( ounce(s)* )|( lb(s)* )|( pound(s)* )|(small)|(medium)|(large))(of)*")
            line = ridOf(line, ",(.*)")
            line = splitCombinatories(line).split('\n')
            for linesplit in line:
                lines.append(linesplit)
            get = True
    thefile.close()

    return lines

def parseMatchData(name):
    '''Gets information from a saved recipe file and deletes unnecessary files
       return -> the file information'''

    filename = usersaves+str(name)
    thefile = open(filename, 'r')
    get = True
    lines = []
    ingredients[name[:-4]] = ingredient(name[:-4])
    ishouldremovethis = False
    
    while get:
        get = False
        line = thefile.readline()
        if line != '':
            line = line.split("|")
            lines.append([line[0], int(line[1])])
            get = True

    thefile.close()
    if ishouldremovethis:
        os.remove(filename)
        del ingredients[name[:-4]]
        return None
    
    return lines

def solve(recipe, quality, size, allowed):

    if size == 0:
        return recipe

    while len(allowed) > 0:
        test = 'xxx'
        while test in disclude:
            test = random.sample(allowed, 1)
            test = test[0]
            allowed.discard(test)
        answer = solve(recipe+[test], quality, size - 1, allowed.intersection(ingredients[test].getInRange(quality[0], quality[1])))
        if answer != None:
            return answer
        
    return None

def fixSpacing(string):
    dc = False
    string = string.split()
    if string[0] == 'no':
        string.pop(0)
        dc = True
    newstring = ''
    for word in string:
        newstring += word + ' '
    newstring = newstring[:-1]
    if dc:
        disclude.add(newstring)
        return None
    return newstring
    
######################################
class recipe(object):

    __slots__ = ('name', 'ingreds', 'basis')

    def __init__(self, name, ingredlist, basis = None, thesize = 3, qlow = 60, qhigh = 100):

        if not basis:
            recipelist[name] = self
            self.ingreds = []
            self.name = name
            for ingredstring in ingredlist:
                self.genNames(ingredstring.lower())
            self.addMe()
            self.makeMatches()
        else:
            self.basis = basis
            self.name = "ChefBot's Suggestion"
            self.ingreds = self.chefBot(quality = [qlow,qhigh], size = thesize)

    def addMe(self):

        for sublist in self.ingreds:
            for item in sublist:
                singular = makeSingular(item)
                if item in ingredients:
                    ingredients[item].addRecipe(self.name)
                elif singular in ingredients:
                    ingredients[item] = ingredients[singular]
                    ingredients[singular].addName(item)
                    ingredients[singular].setPlural(item)
                else:
                    ingredients[singular] = ingredient(item, self.name)
                    ingredients[item] = ingredients[singular]
                    ingredients[item].addName(singular)
            
    def genNames(self, namestring):
        
        namestring = namestring.split()
        
        if len(namestring) > 4:
            namestring = namestring[:4]
        elif len(namestring) == 0:
            return
        
        ingreds = []

        for itemnum1 in range(len(namestring)):
            for itemnum2 in range(itemnum1, len(namestring)):
                cbn = namestring[itemnum1:itemnum2+1]
                go = True
                name = ''
                parts = set()
                length = len(cbn)
                if cbn[0] in prepositions or cbn[-1] in prepositions:
                    go = False
                for item in namestring[itemnum1:itemnum2+1]:
                    if item in parts:
                        go = False
                    parts.add(item)
                    name += item + ' '
                name = name[:-1]
                if name not in vetted:
                    go = False
                if go:    
                    ingreds.append(name)

        self.ingreds.append(ingreds)

    def makeMatches(self):

        for ingrednum1 in range(len(self.ingreds)-1):
            for ingrednum2 in range(ingrednum1+1, len(self.ingreds)):
                for ingred1 in self.ingreds[ingrednum1]:
                   for ingred2 in self.ingreds[ingrednum2]:
                        if ingred1 != ingred2:
                            ingredients[ingred1].addMatch(ingred2)

    def chefBot(self, quality = [60,100], size = 5):

        first = self.basis.pop(0)
        allowed = ingredients[first].getInRange(quality[0], quality[1])
        recipe = [first]
        for ingred in self.basis:
            recipe += [ingred]
            allowed = allowed.intersection(ingredients[ingred].getInRange(quality[0], quality[1]))
            size += -1
        return solve(recipe, quality, size-1, allowed)

    def __str__(self):

        string = self.name+'\n##########\n'
        for item1 in self.ingreds:
            if type(item1) == list:
                for item2 in item1:
                    string += str(ingredients[item2]) + '\n'
            else:
                string += str(ingredients[item1]) + '\n'
        string += '##########'

        return string

class ingredient(object):

    __slots__ = ('name', 'names', 'plural', 'recipes','matches','data')

    def __init__(self, name, recipe = None):

        self.data = None
        self.matches = dict()
        self.recipes = []
        self.name = name
        self.plural = name
        self.names = [name]
        if recipe:
            self.recipes.append(recipe)

    def addName(self, name):

        self.names.append(name)
        if len(self.names) == 3:
            self.names = sorted(self.names)[1:]

    def setPlural(self, name):

        self.plural = name

    def addRecipe(self, recipe):

        self.recipes.append(recipe)

    def addMatch(self, match):

        match = ingredients[match].name

        if match in self.matches:
            self.matches[match] += 1
        else:
            self.matches[match] = 1
            
        ingredients[match].reciprocateMe(self.name)

    def setMatchSet(self, matchset):

        self.data = matchset
        self.matches = dict(matchset)

    def reciprocateMe(self, match):

        if match in self.matches:
            self.matches[match] += 1
        else:
            self.matches[match] = 1

    def orderMe(self):

        if not self.data:
            self.data = sorted(self.matches.items(), key = lambda x:x[1], reverse = True)

    def getMatches(self):

        self.orderMe()
        return self.data

    def toFile(self, directory = ''):

        self.orderMe()
        filename = directory+'//'+self.name+'.txt'
        daFile = open(filename, "w")
        daFile = open(filename, "a")
        for ingredo in self.data:
            daFile.write(str(ingredo[0])+"|"+str(ingredo[1])+"\n")
        daFile.close()

    def getInRange(self, lower, upper):

        self.orderMe()
        done = False
        length = len(self.data) - 1
        allowed = set()
        counter = 0
        while not done:
            value = mapsTo(self.data[counter][1])
            #print value
            if value <= upper and value >= lower:
                #possible.append(self.data[counter])
                allowed.add(self.data[counter][0])
            if (value < lower) or (counter == length):
                done = True
            counter += 1
        #theGet = random.choice(possible)[0]
        
        return allowed

    def __str__(self):

        return self.plural

def savedData():
    
    #directory = raw_input("Enter the initial directory: ")
    directory = usersaves
    allin = os.listdir(str(directory))

    sample = len(allin)

    #time.clock()
    
    counter = 0
    breakpoints = set()
    for brk in range(10):
        breakpoints.add(int((sample/10)*(brk+1)))

    os.system('CLS')
    print(" LOADING...")
    print("[          ]")
    
    for piece in allin:

        counter += 1
        if counter in breakpoints:
            os.system('CLS')
            print(" LOADING...")
            print('['+'|'*int(10*(float(counter)/float(sample)))+' '*(10-int(10*(float(counter)/float(sample))))+']')

        matchlist = parseMatchData(piece)
        if matchlist:
            ingredients[piece[:-4]].setMatchSet(matchlist)

    os.system('CLS')
    
def newData():
    
    sample = int(raw_input("Enter the sample size you would like: "))

    #directory = raw_input("Enter the initial directory: ")
    directory = recipedir
    allin = os.listdir(str(directory))

    #time.clock()

    counter = 0
    breakpoints = set()
    for brk in range(10):
        breakpoints.add(int((sample/10)*(brk+1)))

    os.system('CLS')
    print(" LOADING...")
    print("[          ]")
    for piece in allin:

        counter += 1
        if counter in breakpoints:
            os.system('CLS')
            print(" LOADING...")
            print('['+'|'*int(10*(float(counter)/float(sample)))+' '*(10-int(10*(float(counter)/float(sample))))+']')
        
        recipeName = int(piece[:-4])
        recipe(recipeName, fileList(directory+"\\"+piece))

        if sample == counter:
            break
    os.system('CLS')

def main():

    ### LOAD VETTED
    vetFile = open("vetted.txt", "r")
    vetList = vetFile.readline().split(";")
    for item in vetList:
        singular = makeSingular(item)
        if item not in vetted:
            vetted.add(item) 
        if singular not in vetted:
            vetted.add(singular)
            
    load = raw_input("Type 'load' to load previous data or enter to continue\n").lower()

    os.system('CLS')

    if load == 'load':
        savedData()
    else:
        newData()
        save = raw_input("Type 'save' to save data or enter to continue\n").lower()
        if save == 'save':
            for ingred in ingredients:
                ingredients[ingred].toFile(usersaves)
       
    search = raw_input("Which ingredients would you like to start with? ").lower().split(",")

    while search != "quit":

        found = True

        for item in range(len(search)):
            search[item] = fixSpacing(search[item])
            if search[item]:
                if search[item] not in ingredients:
                    found = False
        
        if found:
            size = int(raw_input("Enter the size of the recipe: "))
            low = int(raw_input("Enter the lowest allowed quality (0-100): "))
            high = int(raw_input("Enter the highest allowed quality (0-100): "))
            os.system('CLS')
            print recipe(None, None, basis = search, thesize = size, qlow = low, qhigh = high)
        else:
            print "Not found!"
            
        search = raw_input("Which ingredient would you like to see? ").lower().split(",")

main()


