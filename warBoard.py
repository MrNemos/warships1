def grey_zone(e, y):
    #print(e,y)
    if y.index(e) == 0:
        return y[0:2]
    else:
        return y[y.index(e) - 1:y.index(e) + 2]
class Ships:
    def __init__(self, leng, status, cord):
        self.status = status or 'live'
        self.leng = leng
        for i in cord:
            self.cord[f'{i}'] = leng
class Board:

    def __init__(self,name,x,y,ships):
        self.name = name
        self.flag = True
        self.__shipsorder = ships or {'4 size': 1,'3 size':2,'2 size':3,'1 size':4}
        self.__shipslive = ships or {'4 size': 0,'3 size':0,'2 size':0,'1 size':0}
        self.__brokenships = ships or {'4 size': 0,'3 size':0,'2 size':0,'1 size':0}
        self.__board = {}
        self.__x = x or (1,2,3,4,5,6,7,8,9,10)
        self.__y = y or 'abcdefghij'
        Board.cleanboard(self)


    def __repr__(self):
        """
        :return: Board name and size
        """
        return f"Board {self.name}-{self.flag}: size {len(self.__x)}x{len(self.__y)}"

    def printBoard(self):
        """
        Print board for matrix form
        :return: none
        """
        print("   " + str(self.__x).strip("()").replace(","," "))
        for j in range(len(self.__y)):
            print(self.__y[j],end = '  ')
            for i in range(len(self.__x)):
                print(self.__board.get(f'{self.__y[j]}{self.__x[i]}'), end='  ')
            print('')
    def cleanboard(self):
        """
        Clear boards and stats ships live or broken
        :return: None
        """
        for i in self.__shipslive:
            self.__shipslive[i] = 0
            self.__brokenships[i] = 0
        if len(self.__x) == len(self.__y) and len(self.__x)>=8:
            for j in range(len(self.__y)):
                for i in range(len(self.__x)):
                    self.__board[f'{self.__y[j]}{self.__x[i]}'] = 0


    def addShips(self,leng,*pos):
        """
        добавляет корабль на доску, если он соответсвует правилам
        :param leng: длина корабля
        :param pos: позиции корабля
        :return: None
        """
        if leng == len(pos):
            if leng <= len(self.__shipsorder):
                if self.__shipsorder[f'{leng} size'] > self.__shipslive[f'{leng} size']:
                    if Board.cheks_ship(self, *pos):
                        for i in pos:
                            self.__board[i] = 'L'
                            self.__shipslive[f'{leng} size'] += 1

                    # elif leng == 1:
                    #     cords = list(startpos)
                    #     if Board.cheks_ship(self, *cords):
                    #         self.__board[startpos] = 'live'
                    #         self.__shipslive[f'{leng} size'] += 1
        else:
            print("Strange input")

    def shot(self,cord):
        f = self.__board.get(cord)
        if f == 0:
            self.__board[cord] = 'm'
            return 'miss'
        elif f in 'm,d':
            return "you hit this place of previous shot. Try again"
        elif f == 'l':
            self.__board[cord] = 'd'
            return 'you hit ships'

    def cheks_ship(self, *cords):
        x1 = []
        y1 = []
        for g in cords:
            if g != None:
                e, f = list(g)
                y1 = y1 + list(grey_zone(e, self.__y))
                x1 = x1 + list(grey_zone(int(f), self.__x))
        x1, y1 = set(x1), set(y1)
        for i in y1:
            for j in x1:
                if self.__board[f'{i}{j}'] == 0:
                    continue
                #print(f"{i}{j}")
                return False
        return True

mywarboard = Board('myboard',None,None,None)
mywarboard.printBoard()
#print(myboard)