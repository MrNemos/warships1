
class Ships:
    def __init__(self, leng, status, cord):
        self.status = status or 'not a board'
        self.leng = leng
        self.cord = cord

    def hit_ship(self, board):
        for i in self.cord:
            if board.board[i] == "X":
                continue
            else:
                return 'you hit ship'
        board = self.destroy_ship(board)
        return 'you destroy ship'

    def destroy_ship(self,board):
        x1, y1 = board.grey_zone(self.cord)
        for i in y1:
            for j in x1:
                if board.board[f'{i}{j}'] == 0:
                    board.board[f'{i}{j}'] = '*'
        self.status = 'destroy'
        board.shipslive[f'{self.leng} size'] -= 1
        board.brokenships[f'{self.leng} size'] += 1
        return board


class Board:

    def __init__(self,name,x,y,ships):
        self.name = name
        self.flag = True
        self.__shipsorder = ships or {'4 size': 1,'3 size':2,'2 size':3,'1 size':4}
        self.shipslive = ships or {'4 size': 0,'3 size':0,'2 size':0,'1 size':0}
        self.brokenships = ships or {'4 size': 0,'3 size':0,'2 size':0,'1 size':0}
        self.board = {}
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
                z = self.board.get(f'{self.__y[j]}{self.__x[i]}')
                if type(z) == Ships:
                    z = 's'
                print(z, end='  ')
            print('')


    def cleanboard(self):
        """
        Clear boards and stats ships live or broken
        :return: None
        """
        for i in self.shipslive:
            self.shipslive[i] = 0
            self.brokenships[i] = 0
        if len(self.__x) == len(self.__y) and len(self.__x)>=8:
            for j in range(len(self.__y)):
                for i in range(len(self.__x)):
                    self.board[f'{self.__y[j]}{self.__x[i]}'] = 0


    def addShips(self,ship,*pos):
        """
        добавляет корабль на доску, если он соответсвует правилам
        :param leng: длина корабля
        :param pos: позиции корабля
        :return: None
        """
        if not self.flag:
            return 'you not change board, after start'
        if ship.leng == len(pos):
            if ship.leng <= len(self.__shipsorder):
                if self.__shipsorder[f'{ship.leng} size'] > self.shipslive[f'{ship.leng} size']:
                    if Board.cheks_ship(self, *pos):
                        ship.cord = pos
                        ship.status = 'live'
                        for i in pos:
                            self.board[i] = ship

                        return 'ship enabled'
                    else:
                        print('Что-то пошло не так')
                else:
                    print('Лимит корабликов сего размера превышен')
            else:
                print("Размер кораблика слегка большеват")
        else:
            print("Strange input")

    def remove_ship(self,ship):
        if self.flag:
            return 'you not remove ship, after start'
        if ship.status == 'live':
            self.shipslive[f'{ship.leng} size'] -= 1
            ship.status = 'not a board'
            for i in ship.cord:
                self.board[i] = 0
            return 'ship remove'


    def shot(self,cord):
        f = self.board.get(cord)
        if type(f) == Ships:
            self.board[cord] = 'X'
            res = f.hit_ship(self)
            return res
        elif f == 0:
            self.board[cord] = '*'
            return 'miss'
        elif f in '*,X':
            return "you hit this place of previous shot. Try again"


    def cheks_ship(self, *cords):
        vector_i = ''
        vector_j = ''
        for i in cords:
            vector_i = vector_i + i[0]
            vector_j = vector_j + i[1]
        if len(set(vector_j)) == 1 or len(set(vector_i)) == 1:
            x1, y1 = self.grey_zone(cords)
            for i in y1:
                for j in x1:
                    if self.board[f'{i}{j}'] == 0:
                        continue
                    #print(f"{i}{j}")
                    return False
            return True
        return False

    def grey_zone(self, cord):
        x1 = []
        y1 = []

        for g in cord:
            if g != None:
                print(g)
                e, f = g[0],g[1]
                y1 = y1 + list(grey_line(e, self.__y))
                x1 = x1 + list(grey_line(int(f), self.__x))
        x1, y1 = set(x1), set(y1)
        return x1, y1
def grey_line(e, y):
    # print(e,y)
    if y.index(e) == 0:
        return y[0:2]
    elif y[-1] == e:
        return y[-2:-1]
    else:
        return y[y.index(e) - 1:y.index(e) + 2]

class EnemyBoard(Board):
    def __init__(self,*args,**kwargs):
        super.__init__(*args,**kwargs)

    def shot(self,cord):
        pass


if '__main__' == __name__:
    mywarboard = Board('myboard', None, None, None)
    lodka = Ships(4, None, 0)
    mywarboard.addShips(lodka, "j7", "j8", "j9", "j10")
    mywarboard.printBoard()
    for i in ('a1', 'a4', 'a2', 'd3', 'a3'):
        print(mywarboard.shot(i))
    print(mywarboard)
    mywarboard.printBoard()