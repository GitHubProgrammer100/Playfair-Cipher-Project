import argparse
class Playfair:
    def __init__(self):
        # Define the set of letters
        self.letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '
        self.pletters = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    def firstFormat(self, str):
        str = str.upper()
        str = str.replace(' ', '')
        str = str.replace('J', 'I')
        return str

    def Q_ifier(self, str):
        newtext = []
        count = 0
        while count < len(str):
            if count + 1 < len(str):
                if str[count].upper() != str[count+1].upper():
                    newtext.append(str[count]+str[count + 1])
                    count += 1
                else:
                    newtext.append(str[count] + 'Q')
            else:
                newtext.append(str[count] + 'Q')
            count += 1
        return ''.join(newtext)

    # makes sure there are only letters
    def valid_key(self, key):
        key = key.upper()
        for each in key:
            if each not in self.letters:
                return False
        return True
    
    # makes sure there are only letters
    def gridmaker(self, key):
        if self.valid_key(key) == True:
            key = self.firstFormat(key)
            grid = []
            for x in key:
                if x not in grid:
                    grid.append(x)

            for x in self.pletters:
                if x not in key:
                    grid.append(x)
            grid = ''.join(grid)
            return grid.upper()
        else:
            print("Invalid key")
    
    # Execute the playfair cipher
    def playfair_swaps (self, key, text, direction):
        text = list(text)
        block = []
        for x in range(0,len(text),2):
            block.append(text[x]+text[x + 1])
        swapified = []
        for i in block:
            first = key.find(i[0])
            second = key.find(i[1])
            fx = first % 5
            fy = (first - fx) // 5
            sx = second % 5
            sy = (second -sx) // 5
            if fx == sx:
                fy += 1 *direction
                sy += 1 *direction
                if fy > 4:
                    fy = 0
                if sy > 4:
                    sy = 0
                if fy < 0:
                    fy = 4
                if sy < 0:
                    sy = 4
            elif fy == sy:
                fx += 1 *direction
                sx += 1 *direction
                if fx > 4:
                    fx = 0
                if sx > 4:
                    sx = 0
                if fx < 0:
                    fx = 4
                if sx < 0:
                    sx = 4
            else:
                hold = fx
                fx = sx
                sx = hold
            first = fy * 5 + fx
            second = sy * 5 + sx
            swapified.append(key[first]+key[second])
        return ''.join(swapified)

class Railtalk:

    def encrypt(self, english_text):
        split_text = list(english_text)
        lineA = []
        lineB = []
        for i in range(len(split_text)):
            if i%2 == 0:
                lineA.append(split_text[i])
            else:
                lineB.append(split_text[i])
        return ''.join(lineA) + ''.join(lineB)

    def decrypt(self, rail_text):
        split_text = list(rail_text)
        if len(split_text) % 2 != 0:
            split_text.append(' ')
        x = int(len(split_text) /2)
        newtext = []
        for i in range(x):
            newtext.append(split_text[i]+split_text[i + x])
        return ''.join(newtext)

class Subtalk:
    def __init__(self):
        self.ori = 'abcdefghijklmnopqrstuvwxyz '

    def valid_phrase(self, phrase, key):
        phrase = phrase.lower()
        for each in phrase:
            if each not in self.ori:
                return False
        for each in key:
            if each not in self.ori:
                return False
        return True
    def keymaker(self, key):
        key = key.lower()
        newkey = []
        for x in key:
            if x not in newkey:
                newkey.append(x)
        stop = self.ori.find(newkey[-1])
        first = self.ori[stop+1:]
        last = self.ori[:stop]
        for x in first:
            if x not in key:
                newkey.append(x)
        for x in last:
            if x not in key:
                newkey.append(x)
        newkey = ''.join(newkey)
        print(newkey)
        return newkey.lower()
    def encrypt(self, english_text, key):
        split_text = list(english_text.lower())
        key = self.keymaker(key)
        shuffler = []
        newtext = []
        c = 0
        for i in self.ori:
            shuffler.append([i,key[c]])
            c += 1
        for x in split_text:
            search = False
            c = 0
            while search == False:
                if shuffler[c][0] == x:
                    newtext.append(shuffler[c][1])
                    search = True
                c += 1
        return ''.join(newtext)

    def decrypt(self, sub_text, key):
        split_text = list(sub_text.lower())
        key = self.keymaker(key)
        shuffler = []
        newtext = []
        c = 0
        for i in self.ori:
            shuffler.append([i, key[c]])
            c += 1
        for x in split_text:
            search = False
            c = 0
            while search == False:
                if shuffler[c][1] == x:
                    newtext.append(shuffler[c][0])
                    search = True
                c += 1
        return ''.join(newtext)

def main():

    parser = argparse.ArgumentParser(description='Encrypts and decrypts rail-2, substitution, or playfair cypher')
    parser.add_argument('phrase', type=str, help='message to translate')
    parser.add_argument('mode', type=str, choices=['rail', 'sub', 'derail', 'desub', 'play', 'deplay'],help='choose to translate to Rail-2, Substitution, Playfair, or plaintext')
    parser.add_argument('key', type=str, help='key using letters of alphabet')
    args = parser.parse_args()

    if args.mode == 'rail' or args.mode == 'derail':
        translator = Railtalk()
        if args.mode == 'rail':
            print(translator.encrypt(args.phrase))
        elif args.mode == 'derail':
            print(translator.decrypt(args.phrase))

    elif args.mode == 'sub' or args.mode == 'desub':
        translator = Subtalk()
        if translator.valid_phrase(args.phrase, args.key) == True:
            if args.mode == 'sub':
                print(translator.encrypt(args.phrase, args.key))
            elif args.mode == 'desub':
                print(translator.decrypt(args.phrase, args.key))
                
    elif args.mode == 'play' or args.mode == 'deplay':
        translator = Playfair()
        if translator.valid_key(args.key) == True:
            if args.mode == 'play':
                key = translator.gridmaker(args.key)
                phrase = translator.firstFormat(args.phrase)
                phrase = translator.Q_ifier(phrase)

                phrase = translator.playfair_swaps(key, phrase, 1)
                print(phrase)

            elif args.mode == 'deplay':
                key = translator.gridmaker(args.key)
                phrase = translator.De_Q_ifier(translator.playfair_swaps(key, args.phrase, -1))
                print(phrase)
        else:
            print('Invalid phrase or key, please check that there is only letters and spaces')
    else:
        print('Error: Not an expected mode')
    return
    
if __name__ == '__main__':
    main()