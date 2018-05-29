#!/usr/bin/env python3

from pprint import pprint
import re
import networkx as nx

SKILLS = [
    'Archery', 'Athletics', 'Awareness', 'Brawl', 'Bureaucracy', 
    'Craft', 'Dodge', 'Integrity', 'Investigation', 'Larceny', 
    'Linguistics', 'Lore', 'Medicine', 'Melee', 'Occult', 
    'Performance', 'Presence', 'Resistance', 'Ride', 'Sail', 
    'Socialize', 'Stealth', 'Survival', 'Thrown', 'War',

    'Sorcery'
]

def main():
    charms = parseFile('charms.txt')
    pprint(charms)
    names = [charm['name'] for charm in charms]
    # print([name for name in names if name.startswith('Finding')])
    # pprint([charm for charm in charms if 'prerequisites' not in charm])
    

def parseFile(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    lines = cleanLines(lines)

    currentCharm = None
    currentSkill = None
    charms = []
    for i,line in enumerate(lines):
        if line.strip() in SKILLS:
            # print('NEW SKILL BEGINS: %s' % line)
            currentSkill = line
        elif len(lines) > i+1 and lines[i+1].startswith('Cost:'):
            if currentCharm:
                currentCharm['description'] = ' '.join(currentCharm['description'])
                charms.append(currentCharm)
            currentCharm = {'description': []}
            currentCharm['name'] = line
            currentCharm['skill'] = currentSkill
        elif line.startswith('Cost:'):
            print(line)
            currentCharm['cost'] = parseCost(line)
        elif line.startswith('Mins:'):
            currentCharm['mins'] = parseMins(line)
        elif line.startswith('Type:'):
            currentCharm['type'] = parseType(line)
        elif line.startswith('Keywords:'):
            currentCharm['keywords'] = parseKeywords(line)
        elif line.startswith('Duration:'):
            currentCharm['duration'] = parseDuration(line)
        elif line.startswith('Prerequisite Charms:'):
            currentCharm['prerequisites'] = parsePrerequisites(line)
        elif line.startswith('Prerequisite Charm:'):
            currentCharm['prerequisites'] = parsePrerequisites(line.replace('Prerequisite Charm', 'Prerequisite Charms'))
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

    return charms


def cleanLines(lines):
    lines = [line.strip() for line in lines]

    newLines = [cleanLine(line) for line in lines]

    return [line for sublist in newLines for line in sublist]

def cleanLine(line):
    # Typos
    if 'Observer Awareness Prana' in line:
        line = line.replace('Observer Awareness Prana', 'Observer Awareness Method')
    if "Observer-Awareness" in line:
        line = line.replace("Observer-Awareness", "Observer Awareness")
    if "Finding The Water's Depths" in line:
        line = line.replace("Finding The Water's Depths", "Finding the Water's Depths")
    if "Threshold-Warding" in line:
        line = line.replace("Threshold-Warding", "Threshold Warding")
    if "Breath of Inspiration" in line:
        line = line.replace("Breath of Inspiration", "Opening the Mind's Gates")
    if "Lightning Flash Meditation" in line:
        line = line.replace("Lightning Flash Meditation", "Lightning Flash Inspiration")
    if "Audience-Enthusing Performance" in line:
        line = line.replace("Audience-Enthusing Performance", "Audience-Enthusing Display")
    if "Heaven-Racing Leap" in line:
        line = line.replace("Heaven-Racing Leap", "Heaven-Gracing Leap")
    if "Cloud-Harnessing Method" in line:
        line = line.replace("Cloud-Harnessing Method", "Cloud-Harnessing Technique")
    if "Seize-the-Reins Approach" in line:
        line = line.replace("Seize-the-Reins Approach", "Seizing-the-Reins Approach")
    if "Vanishing Fogbank Escape" in line:
        line = line.replace("Vanishing Fogbank Escape", "Vanishing Fog-Bank Escape")
    if "Friend-to-All Nations Attitude" in line:
        line = line.replace("Friend-to-All Nations Attitude", "Friend-to-All-Nations Attitude")
    if "Mother of Beasts Mastery" in line:
        line = line.replace("Mother of Beasts Mastery", "Mother-of-Beasts Mastery")

    if line.strip() == 'Prerequisite Charms: Burning Dragon Mien, Unbearable Taunt Technique, Warm-Faced':
        return ['Prerequisite Charms: Burning Dragon Mien, Unbearable Taunt Technique, Warm-Faced Seduction Style']
    if line == 'Seduction Style':
        return []

    if line == '':
        return []
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

def parseDuration(line):
    return line.split('Duration:')[-1].strip()

def parsePrerequisites(line):
    return line.split('Prerequisite Charms:')[-1].strip()
#return re.search('Mins:\s+(.*)\s+(Type:)?', line).group(1)

# print(cleanLine('Cost: 5m, 1wp; Mins: War 5, Essence 3 Type: Simple'))
# print(cleanLine('Keywords: Signature (Wood) Duration: Until stratagem is completed Prerequisite Charms: None'))

    

main()
