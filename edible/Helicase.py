################################
## PROJECT EDIBLE             ##
##                            ##
##Version: 1.0                ##
##Developers: Michael Albert  ##
##Release Date: 3/18/2014     ##
################################

import urllib, re, time, os, random

modifiers = {}

prepositions = {'of', 'to', 'with', 'in', 'and'}

exceptions = {}

disclude = {'xxx'}

ingredients = dict()
recipelist = dict()

#####################################
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

    filename = ""+str(name)
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
##            else:
##                ishouldremovethis = True
##                break
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
            self.name = "A Good Recipe."
            self.ingreds = self.chefBot(quality = [qlow,qhigh], size = thesize)

    def addMe(self):

        for sublist in self.ingreds:
            for item in sublist:
                if item in ingredients:
                    ingredients[item].addRecipe(self.name)
                else:
                    ingredients[item] = ingredient(item, self.name)
            
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
                mods = 0
                parts = set()
                length = len(cbn)
                if cbn[0] in prepositions or cbn[-1] in prepositions:
                    go = False
                for item in namestring[itemnum1:itemnum2+1]:
                    if item in parts:
                        go = False
                    parts.add(item)
                    if item in modifiers:
                        mods += 1
                    name += item + ' '
                if mods == length and name[:-1] not in exceptions:
                    go = False
                if go:    
                    ingreds.append(name[:-1])

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
                    string += item2 + '\n'
            else:
                string += item1 + '\n'
        string += '##########'

        return string

class ingredient(object):

    __slots__ = ('name','recipes','matches','data')

    def __init__(self, name, recipe = None):

        self.data = None
        self.matches = dict()
        self.recipes = []
        self.name = name
        if recipe:
            self.recipes.append(recipe)

    def addRecipe(self, recipe):

        self.recipes.append(recipe)

    def addMatch(self, match):

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

def savedData():
    
    #directory = raw_input("Enter the initial directory: ")
    directory = ""
    allin = os.listdir(str(directory))

    #time.clock()

    for piece in allin:
        matchlist = parseMatchData(piece)
        if matchlist:
            ingredients[piece[:-4]].setMatchSet(matchlist)

def newData():
    
    sample = int(raw_input("Enter the sample size you would like: "))

    #directory = raw_input("Enter the initial directory: ")
    directory = ""
    allin = os.listdir(str(directory))

    #time.clock()

    counter = 0

    for piece in allin:

        counter += 1
        recipeName = int(piece[:-4])
        recipe(recipeName, fileList(directory+"\\"+piece))

        if sample == counter:
            break

def main():

    load = raw_input("Type 'load' to load previous data or enter to continue\n").lower()

    os.system('CLS')

    if load == 'load':
        savedData()
    else:
        newData()
        save = raw_input("Type 'save' to save data or enter to continue\n").lower()
        if save == 'save':
            for ingred in ingredients:
                ingredients[ingred].toFile("")
       
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


