import csv
import json

cards = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

hands = [
  'AA',
  'AKs',
  'AQs',
  'AJs',
  'ATs',
  'A9s',
  'A8s',
  'A7s',
  'A6s',
  'A5s',
  'A4s',
  'A3s',
  'A2s',
  'AKo',
  'KK',
  'KQs',
  'KJs',
  'KTs',
  'K9s',
  'K8s',
  'K7s',
  'K6s',
  'K5s',
  'K4s',
  'K3s',
  'K2s',
  'AQo',
  'KQo',
  'QQ',
  'QJs',
  'QTs',
  'Q9s',
  'Q8s',
  'Q7s',
  'Q6s',
  'Q5s',
  'Q4s',
  'Q3s',
  'Q2s',
  'AJo',
  'KJo',
  'QJo',
  'JJ',
  'JTs',
  'J9s',
  'J8s',
  'J7s',
  'J6s',
  'J5s',
  'J4s',
  'J3s',
  'J2s',
  'ATo',
  'KTo',
  'QTo',
  'JTo',
  'TT',
  'T9s',
  'T8s',
  'T7s',
  'T6s',
  'T5s',
  'T4s',
  'T3s',
  'T2s',
  'A9o',
  'K9o',
  'Q9o',
  'J9o',
  'T9o',
  '99',
  '98s',
  '97s',
  '96s',
  '95s',
  '94s',
  '93s',
  '92s',
  'A8o',
  'K8o',
  'Q8o',
  'J8o',
  'T8o',
  '98o',
  '88',
  '87s',
  '86s',
  '85s',
  '84s',
  '83s',
  '82s',
  'A7o',
  'K7o',
  'Q7o',
  'J7o',
  'T7o',
  '97o',
  '87o',
  '77',
  '76s',
  '75s',
  '74s',
  '73s',
  '72s',
  'A6o',
  'K6o',
  'Q6o',
  'J6o',
  'T6o',
  '96o',
  '86o',
  '76o',
  '66',
  '65s',
  '64s',
  '63s',
  '62s',
  'A5o',
  'K5o',
  'Q5o',
  'J5o',
  'T5o',
  '95o',
  '85o',
  '75o',
  '65o',
  '55',
  '54s',
  '53s',
  '52s',
  'A4o',
  'K4o',
  'Q4o',
  'J4o',
  'T4o',
  '94o',
  '84o',
  '74o',
  '64o',
  '54o',
  '44',
  '43s',
  '42s',
  'A3o',
  'K3o',
  'Q3o',
  'J3o',
  'T3o',
  '93o',
  '83o',
  '73o',
  '63o',
  '53o',
  '43o',
  '33',
  '32s',
  'A2o',
  'K2o',
  'Q2o',
  'J2o',
  'T2o',
  '92o',
  '82o',
  '72o',
  '62o',
  '52o',
  '42o',
  '32o',
  '22',
];

positions = ['UTG', 'UTG+1', 'MP1', 'MP2', 'HJ', 'CO', 'BTN', 'SB']

ANTE = 'None'

def is_pair(token):
    return token[0] == token[1]

def gen_hands_matrix(hands):
    count = 0
    result = []
    aux = []
    for h in hands:
        aux.append(h)
        count+=1
        if count % 13 == 0:
            result.append(aux)
            aux = []
    return result
    
hands_matrix = gen_hands_matrix(hands)

def get_position_on_matrix(token):
    if '+' in token:
        clean_token = token[:-1]
    else:
        clean_token = token
    for i in range(13):
        for j in range(13):
            if hands_matrix[i][j] == clean_token:
                return i, j

print(get_position_on_matrix('J2o+'))

def token_to_range(token):
    hand_range = {}
    if '+' not in token:
        hand_range[token] = True
    else:
        x, y = get_position_on_matrix(token)
        if is_pair(token):
            for i in range(x+1):
                hand_range[ hands_matrix[i][i] ] = True

        if 'o' in token:
            for i in range(y+1, x+1):
                hand_range[ hands_matrix[i][y] ] = True

        if 's' in token:
            for j in range(x+1, y+1):
                hand_range[ hands_matrix[x][j] ] = True

    return hand_range

print(token_to_range('J2o+'))


def compact_range_to_dict(compact_range):
    result = {}
    if compact_range == '100.0%, Any two':
        any_two_range = {}
        for i in range(13):
            for j in range(13):
                any_two_range[ hands_matrix[i][j] ] = True
        return any_two_range
    for token in compact_range.split(' '):
        if ('%' in token):
            continue
        if 'x' in token:
            card = token[0]
            card_position = cards.index(card)
            for i in range(card_position + 1):
                offsuit_token = f"{cards[i]}2o+"
                suited_token = f"{cards[i]}2s+"
                offsuit_token_range = token_to_range(offsuit_token)
                suited_token_range = token_to_range(suited_token)
                result = result | offsuit_token_range
                result = result | suited_token_range
            continue

        token_range = token_to_range(token)
        result = result | token_range
    return result

print(compact_range_to_dict('TT+ Ax+ KTs+ QJs'))

full_dict = {}
def convert_lines(lines, ante: str):
    stack_size = 1
    for line in lines:
        position_index = 0
        for compact_range in line[1:]:
            position = positions[position_index]
            if position not in full_dict.keys():
                full_dict[position] = {}
            if stack_size not in full_dict[position].keys():
                full_dict[position][stack_size] = {}

            full_range = compact_range_to_dict(compact_range)
            full_dict[position][stack_size][ante] = full_range

            position_index += 1

        stack_size += 1

with open('no_antes_tab.tsv', newline='') as csvfile:
    lines = csv.reader(csvfile, delimiter='\t', quotechar='|') 
    convert_lines(lines, 'None')
with open('no_antes_10.tsv', newline='') as csvfile:
    lines = csv.reader(csvfile, delimiter='\t', quotechar='|') 
    convert_lines(lines, '10%')
with open('no_antes_12.tsv', newline='') as csvfile:
    lines = csv.reader(csvfile, delimiter='\t', quotechar='|') 
    convert_lines(lines, '12.5%')

with open(f"result_full.json", "w") as outfile:
    json.dump(full_dict, outfile)
