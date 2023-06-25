import random
import sys

class Card:
    suits = ["h", "d", "c", "s"] #["ハート", "ダイヤ", "クローバー", "スペード"]
    values = ["A","2","3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]

    def __init__(self, intorstr):
        if type(intorstr)==str:
            suit = intorstr[1]
            value = intorstr[0]
            if suit not in self.suits or value not in self.values:
                raise ValueError("不正なスートまたは値です。")
            hand_int = self.suits.index(suit) + self.values.index(value)*4
        elif type(intorstr)==int:
            if not 0<=intorstr<= 51:
                raise ValueError("不正な値です。")
            hand_int = intorstr
            suit = self.suits[intorstr%4]
            value = self.values[intorstr//4]
        else:
            raise TypeError("不正なタイプです。")
        self.suit = suit
        self.value = self.values.index(value)
        self.hand_int = hand_int

    def __str__(self):
        return f"{self.values[self.value]}{self.suit}"

    def __hash__(self):
        return hash(self.hand_int)
    
    def __lt__(self, other):
        return self.value < other.value
    
    def __gt__(self, other):
        return self.value > other.value
    
    def __eq__(self, other):
        return self.hand_int == other.hand_int
    
deck = set(Card(i) for i in range(52))
    
class razzhand:
    def __init__(self, cards):
        self.cards = cards
        self.values= [card.value for card in cards]
        self.suits= [card.suit for card in cards]
        self.hand_ints= [card.hand_int for card in cards]
        sames = [value + 20*(self.values[:i].count(value)) for i,value in enumerate(self.values)]
        self.razzrank = sorted(list(set(sames)))[:5][::-1]
        #self.diamond = self.cards.count("d")
    
    def __str__(self):
        return "".join([str(card) for card in self.cards])
    
    
    def __lt__(self, other):
        return self.razzrank > other.razzrank
    
    def __gt__(self, other):
        return self.razzrank < other.razzrank
    
    def __eq__(self, other):
        return self.razzrank == other.razzrank
    
class diamondhand:
    def __init__(self, cards):
        self.cards = cards
        self.values= [card.value for card in cards]
        self.suits= [card.suit for card in cards]
        self.hand_ints= [card.hand_int for card in cards]
        #sames = [value + 20*(self.value.count(value)-1) for value in self.values]
        #self.razzrank = sorted(list(set(sames)),reverse=True)
        self.diamond = self.suits.count("d")
    
    def __str__(self):
        return "".join([str(card) for card in self.cards])
    
    def __lt__(self, other):
        return self.diamond < other.diamond
    
    def __gt__(self, other):
        return self.diamond > other.diamond
    
    def __eq__(self, other):
        return self.diamond == other.diamond

def add(a,b):
    return [aa+bb for aa,bb in zip(a,b)]

def mul(a,m):
    return [aa/m for aa in a]

class studhands_undetermined:
    def __init__(self, hand_list,expose=""):
        self.hand_list = [[Card(hand[i:i+2]) for i in range(0, len(hand), 2)] for hand in hand_list]
        self.leftover = deck.copy()
        for h in self.hand_list:
            self.leftover-=set(h)
            #print(*h)
        for i in range(0,len(expose),2):
            ex = Card(expose[i:i+2])
            self.leftover-=ex.hand_int
        #for l in self.leftover:
        #    print(l)
    
    def random_deal(self):
        random_deck = random.sample(self.leftover,len(self.leftover))
        razz = []
        diamond = []
        for i in range(len(self.hand_list)):
            razz.append(razzhand(self.hand_list[i]+random_deck[-(7-len(self.hand_list[i])):]))
            diamond.append(diamondhand(self.hand_list[i]+random_deck[-(7-len(self.hand_list[i])):]))
            del random_deck[-(7-len(self.hand_list[i])):]
        razzwinhand = max(razz)
        razzeq = [1/razz.count(razzwinhand) if r==razzwinhand else 0 for r in razz]        
        diamondwinhand = max(diamond)
        diamondeq = [1/diamond.count(diamondwinhand) if r==diamondwinhand else 0 for r in diamond]
        #print(razzeq,diamondeq,razz[0],razz[1],razz[0].razzrank,razz[1].razzrank)
        return mul(add(razzeq,diamondeq),2)
    
    def random_diamond(self):
        random_deck = random.sample(self.leftover,len(self.leftover))
        #razz = []
        diamond = []
        for i in range(len(self.hand_list)):
            #razz.append(razzhand(self.hand_list[i]+random_deck[-(7-len(self.hand_list[i])):]))
            diamond.append(diamondhand(self.hand_list[i]+random_deck[-(7-len(self.hand_list[i])):]))
            del random_deck[-(7-len(self.hand_list[i])):]
        #razzwinhand = max(razz)
        #razzeq = [1/razz.count(razzwinhand) if r==razzwinhand else 0 for r in razz]        
        diamondwinhand = max(diamond)
        diamondeq = [1/diamond.count(diamondwinhand) if r==diamondwinhand else 0 for r in diamond]
        #print(razzeq,diamondeq,razz[0],razz[1],razz[0].razzrank,razz[1].razzrank)
        return diamondeq
    
    def random_razz(self):
        random_deck = random.sample(self.leftover,len(self.leftover))
        razz = []
        #diamond = []
        for i in range(len(self.hand_list)):
            razz.append(razzhand(self.hand_list[i]+random_deck[-(7-len(self.hand_list[i])):]))
            #diamond.append(diamondhand(self.hand_list[i]+random_deck[-(7-len(self.hand_list[i])):]))
            del random_deck[-(7-len(self.hand_list[i])):]
        razzwinhand = max(razz)
        razzeq = [1/razz.count(razzwinhand) if r==razzwinhand else 0 for r in razz]        
        #diamondwinhand = max(diamond)
        #diamondeq = [1/diamond.count(diamondwinhand) if r==diamondwinhand else 0 for r in diamond]
        #print(razzeq,diamondeq,razz[0],razz[1],razz[0].razzrank,razz[1].razzrank)
        return razzeq


def main():
    random_num=10**5
    und = studhands_undetermined(sys.argv[1:])
    ans = [0] * (len(sys.argv) - 1)
    for i in range(random_num):
        ans=add(ans,und.random_deal())
    print(mul(ans,random_num))
    

if __name__ == "__main__":
    main()

       

            



        



    

