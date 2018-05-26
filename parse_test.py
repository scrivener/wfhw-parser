#!/usr/bin/env python3

import parse
import pprint

def test_cleanLine():
    result = parse.cleanLine('Cost: 5m, 1wp; Mins: War 5, Essence 3 Type: Simple')
    assert result == [
        'Cost: 5m, 1wp;',
        'Mins: War 5, Essence 3',
        'Type: Simple'
    ]
    
    result = parse.cleanLine('Keywords: Signature (Wood) Duration: Until stratagem is completed Prerequisite Charms: None')
    assert result == [
        'Keywords: Signature (Wood)',
        'Duration: Until stratagem is completed',
        'Prerequisite Charms: None'
    ]

    result = parse.cleanLine('Keywords: Air, Uniform')
    assert result == [
        'Keywords: Air, Uniform'
    ]
    
    result = parse.cleanLine('Sighting along the flow of living Essence, the Dragon-Blood unleashes a flawless shot. She may')
    assert result == ['Sighting along the flow of living Essence, the Dragon-Blood unleashes a flawless shot. She may']

    result = parse.cleanLine('Cost: 3m; Mins: Socialize 2, Essence 1 ')
    assert result == [
        'Cost: 3m;',
        'Mins: Socialize 2, Essence 1'
    ]

    result = parse.cleanLine('Cost: 6m; Mins: Socialize 3, Essence 2 ')
    assert result == [
        'Cost: 6m;',
        'Mins: Socialize 3, Essence 2'
    ]

def test_consistency():
    charms = parse.parseFile('charms.txt')
    names = [charm['name'] for charm in charms]

    assert len(charms) == len(names)
    assert len(set(names)) == len(names)

    def pok(prereq):
        if prereq == 'None':
            return True
        if prereq == 'Any four Occult Charms':
            return True
        if prereq == 'Ox-Body Technique (x5)':
            return True
        else:
            return prereq in names

    for charm in charms:
        if ' or ' in charm['prerequisites']:
            prereqs = charm['prerequisites'].split(' or ')
        else:
            prereqs = charm['prerequisites'].split(',')
        prereqs = [p.strip() for p in prereqs]
        for p in prereqs:
            assert pok(p)


