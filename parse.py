#!/usr/bin/env python3

from pprint import pprint
import re

SKILLS = [
    'Archery', 'Athletics', 'Awareness', 'Brawl', 'Bureaucracy', 
    'Craft', 'Dodge', 'Integrity', 'Investigation', 'Larceny', 
    'Linguistics', 'Lore', 'Medicine', 'Melee', 'Occult', 
    'Performance', 'Presence', 'Resistance', 'Ride', 'Sail', 
    'Socialize', 'Stealth', 'Survival', 'Thrown', 'War',

    'Sorcery'
]

def main():
    with open('charms.txt', 'r') as f:
        lines = f.readlines()
    lines = cleanLines(lines)

    currentCharm = None
    currentSkill = None
    charms = []
    for i,line in enumerate(lines):
        if line.strip() in SKILLS:
            print('NEW SKILL BEGINS: %s' % line)
            currentSkill = line
        if line.startswith('Cost:'):
            if currentCharm:
                currentCharm['description'] = ' '.join(currentCharm['description'])
                charms.append(currentCharm)
                pprint(currentCharm)
            currentCharm = {'description': []}
            currentCharm['name'] = lines[i-1]  
            currentCharm['cost'] = parseCost(line)
            currentCharm['skill'] = currentSkill
        elif line.startswith('Mins:'):
            currentCharm['mins'] = parseMins(line)
        elif line.startswith('Type:'):
            currentCharm['type'] = parseType(line)
        elif line.startswith('Keywords:'):
            currentCharm['keywords'] = parseKeywords(line)
        elif line.startswith('Prerequisite Charms:'):
            currentCharm['prerequisites'] = parsePrerequisites(line)
        else:
            if currentCharm:
                currentCharm['description'].append(line)


    skills = set()
    for charm in charms:
        for word in charm['mins'].split():
            if len(word) > 2 and word != 'Essence':
                skills.add(word)

    # print('found %d skills' % len(skills))
    # print(sorted(list(skills)))
    # assert sorted(list(skills)) == SKILLS



def cleanLines(lines):
    lines = [line.strip() for line in lines]

    newLines = [cleanLine(line) for line in lines]

    return [line for sublist in newLines for line in sublist]

def cleanLine(line):
    tokens = ['PrerequisiteCharms:', 'Type:', 'Cost:', 'Mins:', 'Keywords:', 'Duration:']
    if 'Prerequisite Charms' in line:
        line = line.replace('Prerequisite Charms:', 'PrerequisiteCharms:')

    if all([token not in line for token in tokens]):
        return [line]

    words = line.split()
    newLines = []
    line = None
    for i,word in enumerate(words):
        if word in tokens:
            if line:
                newLines.append(' '.join(line))
            line = [word]
        else:
            line.append(word)
    newLines.append(' '.join(line))
    newLines = [line.replace('PrerequisiteCharms:', 'Prerequisite Charms:') for line in newLines]
    return newLines


def parseCost(line):
    return line.split('Cost:')[1].strip().replace(';', '')

def parseMins(line):
    return line.split('Mins:')[-1].strip()
#return re.search('Mins:\s+(.*)\s+(Type:)?', line).group(1)

def parseType(line):
    return line.split('Type:')[-1].strip()

def parseKeywords(line):
    return line.split('Keywords:')[-1].strip()

def parsePrerequisites(line):
    return line.split('Prerequisite Charms:')[-1].strip()
#return re.search('Mins:\s+(.*)\s+(Type:)?', line).group(1)

# print(cleanLine('Cost: 5m, 1wp; Mins: War 5, Essence 3 Type: Simple'))
# print(cleanLine('Keywords: Signature (Wood) Duration: Until stratagem is completed Prerequisite Charms: None'))

main()
