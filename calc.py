from enum import Enum
from typing import List
import copy
import random
DIAMOND = "♦️"
HEART = "♥️"
SPADE = "♠️"
CLUB = "♣️"
N2, N3, N4, N5, N6, N7, N8, N9, N10, NJ, NQ, NK, NA  = "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"
nums = [N2, N3, N4, N5, N6, N7, N8, N9, N10, NJ, NQ, NK, NA]
suites = [SPADE, CLUB, DIAMOND, HEART]
numerilized_num = {}
numerilized_suite = {}
for i, num in enumerate(nums):
    numerilized_num[num] = i + 2
for i, suite in enumerate(suites):
    numerilized_suite[suite] = i

class Num:
    def __init__(self, num):
        self.num = num
        self._val = numerilized_num[self.num]
        self._str = f'{num}'
    def __ge__(self, x):
        return self._val >= x._val
    def __eq__(self, x):
        return self._val == x._val
    def __lt__(self, x):
        return self._val < x._val
    def __str__(self):
        return self._str
    def __repr__(self):
        return self._str
    def __len__(self):
        return len(self.num)
    def __int__(self):
        return self._val

class Suite:
    def __init__(self, suite):
        self.suite = suite
        self._val = numerilized_suite[self.suite]
        self._str = f'{suite}'
    def __ge__(self, x):
        return self._val >= x._val
    def __eq__(self, x):
        return self._val == x._val
    def __lt__(self, x):
        return self._val < x._val
    def __str__(self):
        return self._str
    def __repr__(self):
        return self._str
    def __int__(self):
        return self._val


class Card:
    def __init__(self, num, suite):
        self.num = Num(num)
        self.suite = Suite(suite)
        self._str = (" " + str(self.num) if len(self.num) != 2 else str(self.num)) + str(self.suite)
        self._val =  int(self.num)
        self._hash = (int(self.suite) << 4) + int(self.num)
    def __str__(self):
        return self._str
    def __int__(self):
        return self._val
    def __repr__(self):
        return self._str
    def __ge__(self, x):
        return self._val >= x._val
    def __eq__(self, x):
        return self._val == x._val
    def __lt__(self, x):
        return self._val < x._val
    def __hash__(self):
        return self._hash

cards = {}
r_cards = {}
for suite in suites:
    cards[suite] = {}
    for num in nums:
        cards[suite][num] = Card(num, suite)
for num in nums:
    r_cards[num] = {}
    for suite in suites:
        r_cards[num][suite] = cards[suite][num]

D2 = cards["♦️"]["2"]
D3 = cards["♦️"]["3"]
D4 = cards["♦️"]["4"]
D5 = cards["♦️"]["5"]
D6 = cards["♦️"]["6"]
D7 = cards["♦️"]["7"]
D8 = cards["♦️"]["8"]
D9 = cards["♦️"]["9"]
D10 = cards["♦️"]["10"]
DJ = cards["♦️"]["J"]
DQ = cards["♦️"]["Q"]
DK = cards["♦️"]["K"]
DA = cards["♦️"]["A"]
H2 = cards["♥️"]["2"]
H3 = cards["♥️"]["3"]
H4 = cards["♥️"]["4"]
H5 = cards["♥️"]["5"]
H6 = cards["♥️"]["6"]
H7 = cards["♥️"]["7"]
H8 = cards["♥️"]["8"]
H9 = cards["♥️"]["9"]
H10 = cards["♥️"]["10"]
HJ = cards["♥️"]["J"]
HQ = cards["♥️"]["Q"]
HK = cards["♥️"]["K"]
HA = cards["♥️"]["A"]
S2 = cards["♠️"]["2"]
S3 = cards["♠️"]["3"]
S4 = cards["♠️"]["4"]
S5 = cards["♠️"]["5"]
S6 = cards["♠️"]["6"]
S7 = cards["♠️"]["7"]
S8 = cards["♠️"]["8"]
S9 = cards["♠️"]["9"]
S10 = cards["♠️"]["10"]
SJ = cards["♠️"]["J"]
SQ = cards["♠️"]["Q"]
SK = cards["♠️"]["K"]
SA = cards["♠️"]["A"]
C2 = cards["♣️"]["2"]
C3 = cards["♣️"]["3"]
C4 = cards["♣️"]["4"]
C5 = cards["♣️"]["5"]
C6 = cards["♣️"]["6"]
C7 = cards["♣️"]["7"]
C8 = cards["♣️"]["8"]
C9 = cards["♣️"]["9"]
C10 = cards["♣️"]["10"]
CJ = cards["♣️"]["J"]
CQ = cards["♣️"]["Q"]
CK = cards["♣️"]["K"]
CA = cards["♣️"]["A"]

def hash_card_list(cards, debug=False):
    tmp = sorted(cards, key=lambda c: c._hash)
    if debug:
        print(cards, tmp)
    v = 0
    for i, card in enumerate(tmp):
        v += hash(card) << (6 * i)
    return v

class GroupType(Enum):
    STRAIGHT_FLUSH = ("STRAIGHT_FLUSH", 9)
    FOUR_OAK = ("FOUR_OAK", 8)
    FULL_HOUSE = ("FULL_HOUSE", 7)
    FLUSH = ("FLUSH", 6)
    STRAIGHT = ("STRAIGHT", 5)
    THREE_OAK = ("THREE_OAK", 4)
    TWO_PAIRS = ("TWO_PAIRS", 3)
    PAIR = ("PAIR", 2)
    HIGH_CARD = ("HIGH_CARD", 1)
    def __str__(self):
        return self.value[0]
    def __repr__(self):
        return self.value[0]
    def __ge__(self, x):
        return self.value[1] >= x.value[1]
    def __eq__(self, x):
        return self.value[1] == x.value[1]
    def __lt__(self, x):
        return self.value[1] < x.value[1]
    def __int__(self):
        return self.value[1]

class Group:
    def __init__(self, cards_list, group_type, val):
        self.cards = cards_list
        self.group_type = group_type
        self._val = (int(group_type) << 20) + val
        self._hash = hash_card_list(self.cards)
    def __ge__(self, x):
        return self._val >= x._val
    def __eq__(self, x):
        return self._val == x._val
    def __lt__(self, x):
        return self._val < x._val
    def __int__(self):
        return self._val
    def calcVal(self):
        val = 0
        for i in range(0, 5):
            val += int(self.cards[i].num) << (i * 4)
        return val
    def __hash__(self) -> int:
        return self._hash
    def __str__(self):
        return f'{self.cards}'

class StraightFlushGroup(Group):
    def __init__(self, cards_list: List[Card], inputVal=None):
        self.cards = sorted(cards_list)
        val = self.calcVal() if inputVal == None else inputVal
        super().__init__(self.cards, GroupType.STRAIGHT_FLUSH, val)

G = [cards[SPADE][N2], cards[SPADE][N3], cards[SPADE][N4], cards[SPADE][N5], cards[SPADE][N6]]
print(G)
print(hex(int(StraightFlushGroup(G))))

class FourOakGroup(Group):
    def __init__(self, cards_list: List[Card]):
        self.cards = sorted(cards_list)
        val = self.calcVal()
        super().__init__(self.cards, GroupType.FOUR_OAK, val)
    def calcVal(self):
        if self.cards[0] == self.cards[1]:
            kindCard = self.cards[0]
            singleCard = self.cards[4]
        else:
            kindCard = self.cards[1]
            singleCard = self.cards[0]
        val = (int(kindCard.num) << 4) + int(singleCard.num)
        return val
G = [cards[SPADE][N2], cards[DIAMOND][N2], cards[CLUB][N2], cards[HEART][N2], cards[CLUB][N6]]
print(G)
print(hex(int(FourOakGroup(G))))

class FullHouseGroup(Group):
    def __init__(self, cards_list: List[Card]):
        self.cards = sorted(cards_list)
        val = self.calcVal()
        super().__init__(self.cards, GroupType.FULL_HOUSE, val)
    def calcVal(self):
        if self.cards[1] == self.cards[2]:
            triCard = self.cards[0]
            dualCard = self.cards[4]
        else:
            triCard = self.cards[4]
            dualCard = self.cards[0]
        val = (int(triCard.num) << 4) + int(dualCard.num)
        return val
G = [cards[SPADE][N2], cards[DIAMOND][N2], cards[CLUB][N2], cards[HEART][N6], cards[SPADE][N6]]
print(G)
print(hex(int(FullHouseGroup(G))))

class FlushGroup(Group):
    def __init__(self, cards_list: List[Card]):
        self.cards = sorted(cards_list)
        val = self.calcVal()
        super().__init__(self.cards, GroupType.FLUSH, val)

G = [cards[DIAMOND][NA], cards[DIAMOND][N3], cards[DIAMOND][N5], cards[DIAMOND][N6], cards[DIAMOND][N7]]
print(G)
print(hex(int(FlushGroup(G))))

class StraghitGroup(Group):
    def __init__(self, cards_list: List[Card], inputVal=None):
        self.cards = sorted(cards_list)
        val = self.calcVal() if inputVal == None else inputVal
        super().__init__(self.cards, GroupType.STRAIGHT, val)

G = [cards[SPADE][N2], cards[DIAMOND][N3], cards[CLUB][N4], cards[HEART][N5], cards[SPADE][NA]]
print(G)
print(hex(int(StraghitGroup(G))))

class TwoPairsGroup(Group):
    def __init__(self, cards_list: List[Card]):
        self.cards = sorted(cards_list)
        val = self.calcVal()
        super().__init__(self.cards, GroupType.TWO_PAIRS, val)
    def calcVal(self):
        count = {}
        for i in range(0, 5):
            n = int(self.cards[i].num)
            count[n] = 1 if not (n in count) else (count[n] + 1)
        tmp = []
        for c in count:
            if count[c] == 2:
                tmp.append(c)
            if count[c] == 1:
                single = c
        tmp.sort()
        val = int(single) + (int(tmp[0]) << 4) + (int(tmp[1]) << 8)
        return val 

G = [cards[SPADE][N2], cards[DIAMOND][N2], cards[CLUB][N4], cards[HEART][N4], cards[SPADE][NA]]
print(G)
print(hex(int(TwoPairsGroup(G))))

class PairGroup(Group):
    def __init__(self, cards_list: List[Card]):
        self.cards = sorted(cards_list)
        val = self.calcVal()
        super().__init__(self.cards, GroupType.PAIR, val)
    def calcVal(self):
        count = {}
        for i in range(0, 5):
            n = int(self.cards[i].num)
            count[n] = 1 if not (n in count) else (count[n] + 1)
        tmp = []
        for c in count:
            if count[c] == 2:
                pairNum = c
            else:
                tmp.append(c)
        tmp.sort()
        val = (int(pairNum) << 12) + (int(tmp[2]) << 8) + (int(tmp[1]) << 4) + int(tmp[0])
        return val

class HighCardGroup(Group):
    def __init__(self, cards_list: List[Card]):
        self.cards = sorted(cards_list)
        val = self.calcVal()
        super().__init__(self.cards, GroupType.HIGH_CARD, val)

G = [cards[SPADE][NJ], cards[DIAMOND][N2], cards[CLUB][N6], cards[HEART][N4], cards[SPADE][NA]]
print(G)
print(hex(int(HighCardGroup(G))))

StraightFlushGroupSet = set()
FourOakGroupSet = set()
FullHouseGroupSet = set()
FlushGroupSet = set()
StraghitGroupSet = set()
TwoPairsGroupSet = set()
def calculate_group_set():
    print("calculating straight flush...")
    for suite in suites:
        for i in range(0, len(nums) - 4):
            tmp = []
            for j in range(0, 5):
                tmp.append(cards[suite][nums[i + j]])
            g = StraightFlushGroup(tmp)
            StraightFlushGroupSet.add(hash(g))
        StraightFlushGroupSet.add(hash(StraightFlushGroup(
            [cards[suite][NA], cards[suite][N2], cards[suite][N3], cards[suite][N4], cards[suite][N5]],
            0x954321
        )))
    print("calculating four of a kind...")
    nums_set = set()
    for i in range(0, len(nums)):
        nums_set.add(nums[i])
    for n in nums_set:
        tmp = []
        for suite in suites:
            tmp.append(cards[suite][n])
        for r in nums_set:
            if n == r:
                continue
            for suite in suites:
                ttmp = copy.copy(tmp)
                ttmp.append(cards[suite][r])
                FourOakGroupSet.add(hash(FourOakGroup(ttmp)))
    print("calculating full house...")
    for tri_num in nums_set:
        for du_num in nums_set:
            if tri_num == du_num:
                continue
            for s1 in range(0, 4):
                for s2 in range(s1 + 1, 4):
                    for s3 in range(s2 + 1, 4):
                        for d1 in range(0, 4):
                            for d2 in range(d1 + 1, 4):
                                FullHouseGroupSet.add(hash(FullHouseGroup([cards[suites[s1]][tri_num], cards[suites[s2]][tri_num], cards[suites[s3]][tri_num], cards[suites[d1]][du_num], cards[suites[d2]][du_num]])))
    print("calculating flush...")
    for s in suites:
        for n1 in range(0, len(nums)):
            for n2 in range(n1 + 1, len(nums)):
                for n3 in range(n2 + 1, len(nums)):
                    for n4 in range(n3 + 1, len(nums)):
                        for n5 in range(n4 + 1, len(nums)):
                            g = FlushGroup([cards[s][nums[n1]], cards[s][nums[n2]], cards[s][nums[n3]], cards[s][nums[n4]], cards[s][nums[n5]]])
                            if n5 == (n4 + 1) == (n3 + 2) == (n2 + 3) == (n1 + 4) or (n1 == 0 and n2 == 1 and n3 == 2 and n4 == 3 and n5 == 12):
                                continue
                            FlushGroupSet.add(hash(g))
    print("calculating straight...")
    for s1 in suites:
        for s2 in suites:
            for s3 in suites:
                for s4 in suites:
                    for s5 in suites:
                        if s1 == s2 == s3 == s4 == s5:
                            continue
                        for i in range(0, len(nums) - 4):
                            StraghitGroupSet.add(hash(StraghitGroup([cards[s1][nums[i]], cards[s2][nums[i + 1]], cards[s3][nums[i + 2]], cards[s4][nums[i + 3]], cards[s5][nums[i + 4]]])))
                        StraghitGroupSet.add(hash(StraghitGroup([cards[s1][NA], cards[s2][N2], cards[s3][N3], cards[s4][N4], cards[s5][N5]], 0x554321)))
    print("calculating two pairs...")
    for p1 in nums_set:
        for p2 in nums_set:
            if p1 == p2:
                continue
            for p3 in nums_set:
                if p3 == p1 or p3 == p2:
                    continue
                for s11 in range(0, len(suites)):
                    for s12 in range(s11 + 1, len(suites)):
                        for s21 in range(0, len(suites)):
                            for s22 in range(s21 + 1, len(suites)):
                                for s30 in range(0, len(suites)):
                                    TwoPairsGroupSet.add(hash(TwoPairsGroup([
                                        cards[suites[s11]][p1],
                                        cards[suites[s12]][p1],
                                        cards[suites[s21]][p2],
                                        cards[suites[s22]][p2],
                                        cards[suites[s30]][p3],
                                    ])))

def get_group(cards) -> Group:
    hashVal = hash_card_list(cards)
    if hashVal in StraightFlushGroupSet:
        return StraghitGroup(cards)
    elif hashVal in FourOakGroupSet:
        return FourOakGroup(cards)
    elif hashVal in FullHouseGroupSet:
        return FullHouseGroup(cards)
    elif hashVal in FlushGroupSet:
        return FlushGroup(cards)
    elif hashVal in StraghitGroupSet:
        return StraightFlushGroup(cards)
    elif hashVal in TwoPairsGroupSet:
        return TwoPairsGroup(cards)
    count = {}
    for card in cards:
        count[card] = 1 if not (card in count) else (count[card] + 1)
    for card in count:
        if count[card] == 2:
            return PairGroup(cards)
    return HighCardGroup(cards)

def combination(candidates: list, num: int) -> list:
    if num == 0:
        return [[]]
    tmp = []
    for i in range(0, len(candidates) - num + 1):
        rest_combinations = combination(candidates[i + 1:], num - 1)
        for c in rest_combinations:
            new_combination = copy.copy(c)
            new_combination.append(candidates[i])
            tmp.append(new_combination)
    return tmp

def calculate_all_in(num_players, iteration=1000):
    print(f'vs {num_players} player{"s" if num_players > 1 else ""}, iteration: {iteration}')
    flattern_cards = []
    for s in suites:
        for n in nums:
            flattern_cards.append(cards[s][n])
    all_possible_hands = combination(flattern_cards, 2)
    # all_possible_hands = [[cards[SPADE][NA], cards[DIAMOND][NA]]]
    for hands in all_possible_hands:
        hands.sort(reverse=True)

    win_count = {}
    for n1 in range(len(nums) - 1, -1, -1):
        for n2 in range(n1, -1, -1):
            if n1 != n2:
                win_count[f'{nums[n1]}{nums[n2]}同色'] = [0, 0]
            win_count[f'{nums[n1]}{nums[n2]}异色'] = [0, 0]
    epoch = 0
    for _ in range(iteration):
        for hands in all_possible_hands:
            cards_on_table = set()
            cards_on_table.add(hands[0])
            cards_on_table.add(hands[1])
            def roll():
                while True:
                    new_card = flattern_cards[random.randint(0, len(flattern_cards) - 1)]
                    if not (new_card in cards_on_table):   
                        break
                cards_on_table.add(new_card)
                return new_card
            deals = [roll() for _ in range(5)]
            win_this_turn = True
            for _ in range(0, num_players):
                c1 = roll()
                c2 = roll()
                if not win(hands, [c1, c2], deals):
                    win_this_turn = False
                    break
            key = f'{hands[0].num}{hands[1].num}{"同色" if hands[0].suite == hands[1].suite else "异色"}'
            if win_this_turn:    
                win_count[key][0] += 1
            else:
                win_count[key][1] += 1
        epoch += 1
        print("epoch: " + str(epoch) + "/" + str(iteration))
    
    tmp = []
    for k in win_count:
        if win_count[k][0] + win_count[k][1] == 0:
            continue
        tmp.append([k, round((win_count[k][0] / (win_count[k][0] + win_count[k][1])) * 100, 2)])
    tmp.sort(key=lambda x: x[1])
    for t in tmp:
        t[1] = f'{t[1]}%'
    print(tmp)

def win(a_hands, b_hands, deals):
    rtn = highest_point(a_hands, deals) > highest_point(b_hands, deals)
    # print(a_hands, b_hands, deals, "win" if rtn else "lose")
    return rtn

def get(suite, num):
    return cards[suite][num]

def highest_point(hands, deals):
    combinations = combination(hands + deals, 5)
    pts = 0
    for c in combinations:
        g = get_group(c)
        if g._val > pts:
            pts = g._val
    return pts

calculate_group_set()
calculate_all_in(1, 500)
# calculate_all_in(2, 500)
# calculate_all_in(3, 500)
# calculate_all_in(4, 500)
# calculate_all_in(5, 500)
# calculate_all_in(6, 500)
# calculate_all_in(7, 500)
