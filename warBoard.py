class Ships:
    def __init__(self, leng):
        self.status = 'not a board'
        self.leng = leng
        self.cord = None

    def hit_ship(self, board):
        for i in self.cord:
            if board.board[i] == "X":
                continue
            else:
                return 'you hit ship'
        self.destroy_ship(board)
        return 'you destroy ship'

    def destroy_ship(self, board):
        x1, y1 = board.grey_zone(self.cord)
        for i in y1:
            for j in x1:
                if board.board[f'{i},{j}'] == 0:
                    board.board[f'{i},{j}'] = '*'
        self.status = 'destroy'
        board.shipslive[f'{self.leng} size'] -= 1
        board.brokenships[f'{self.leng} size'] += 1
        return board


class Board:
    def __init__(self, name):
        self.name = name
        self.flag = True
        self.__shipsorder = {'4 size': 1, '3 size': 2, '2 size': 3, '1 size': 4}
        self.shipslive = {'4 size': 0, '3 size': 0, '2 size': 0, '1 size': 0}
        self.brokenships = {'4 size': 0, '3 size': 0, '2 size': 0, '1 size': 0}
        self.board = {}
        self.__x = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        self.__y = 'abcdefghij'
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
        print("   " + str(self.__x).strip("()").replace(",", " "))
        for j in range(len(self.__y)):
            print(self.__y[j], end='  ')
            for i in range(len(self.__x)):
                z = self.board.get(f'{self.__y[j]},{self.__x[i]}')
                if type(z) == Ships:
                    z = 's'
                print(z, end='  ')
            print('')

    @property
    def shiporder(self):
        return self.__shipsorder

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def cleanboard(self):
        """
        Clear boards and stats ships live or broken
        :return: None
        """
        for i in self.shipslive:
            self.shipslive[i] = 0
            self.brokenships[i] = 0
        if len(self.__x) == len(self.__y) and len(self.__x) >= 8:
            for j in range(len(self.__y)):
                for i in range(len(self.__x)):
                    self.board[f'{self.__y[j]},{self.__x[i]}'] = 0

    def grey_zone(self, cord):
        if type(cord) is str:
            cord = [cord, '']
        x1 = []
        y1 = []
        #print(cord)
        for g in cord:
            if len(g) > 2:
                #print(g)
                e, f = g[0], g[2:]
                #print(e, f)
                y1 = y1 + list(grey_line(e, self.__y))
                x1 = x1 + list(grey_line(int(f), self.__x))

        x1, y1 = set(x1), set(y1)
        #print(x1, y1)
        return x1, y1


def grey_line(e, y):
    # print(e,y)
    if y.index(e) == 0:
        return y[0:2]
    elif y[-1] == e:
        return y[-2:]
    else:
        return y[y.index(e) - 1:y.index(e) + 2]


class EnemyBoard(Board):

    def __init__(self, name):
        super().__init__(name)
        self.active_target = None

    def shot(self, cord, board):
        z, f = board.shot(cord)
        if f == 'miss':
            self.board[f'{cord}'] = '*'
        elif f == 'you hit ship':
            self.board[f'{cord}'] = 'X'
            self.active_target = cord
        elif f == 'you destroy ship':
            self.board[f'{cord}'] = 'X'
            print(self.no_ships_zone(cord))
        return z

    def no_ships_zone(self, cord):
        #print('--------------------------------')
        if type(cord) is str:
            cord = [cord, '']
        flag = False
        x1, y1 = self.grey_zone(cord)
        #print(x1, y1, cord, end='')
        for y in y1:
            for x in x1:
                if self.board[f'{y},{x}'] == 'X':
                    if f'{y},{x}' not in cord:
                        cord.append(f'{y},{x}')
                        self.no_ships_zone(cord)
                    else:
                        flag = True
        if len(cord) == 4 or flag:
            for y in y1:
                for x in x1:
                    if self.board[f'{y},{x}'] == 0:
                        self.board[f'{y},{x}'] = '*'






        return 'ship destroy'


class MyBoard(Board):
    def __init__(self, name):
        super().__init__(name)

    def addShips(self, ship, *pos):
        """
        добавляет корабль на доску, если он соответсвует правилам
        :param ship: силка на кораблик
        :param pos: позиции корабля
        :return: None
        """
        if not self.flag:
            return 'you not change board, after start'
        if self.checks_ship(ship, *pos):
            ship.cord = pos
            ship.status = 'live'
            for i in pos:
                self.board[i] = ship
            return 'ship enabled'
        else:
            return 'Что-то пошло не так'

    def remove_ship(self, ship):
        if self.flag:
            return 'you not remove ship, after start'
        if ship.status == 'live':
            self.shipslive[f'{ship.leng} size'] -= 1
            ship.status = 'not a board'
            for i in ship.cord:
                self.board[i] = 0
            return 'ship remove'

    def shot(self, cord):
        f = self.board.get(cord)
        if type(f) == Ships:
            self.board[cord] = 'X'
            res = f.hit_ship(self)
            return True, res
        elif f == 0 or f == '*':
            self.board[cord] = '*'
            return False, 'miss'

    def checks_ship(self, ship, *cords):
        """
        Сложный функция проверять кораблика на валидность очень сложна
        :param self:
        :param ship: кораблик
        :param cords: координаты
        :return: True or False
        """
        if ship.leng == len(cords):
            if ship.leng <= len(self.shiporder):
                if self.shiporder[f'{ship.leng} size'] > self.shipslive[f'{ship.leng} size']:
                    vector_i = set()
                    vector_j = set()
                    for i in cords:
                        if i != None:
                            vector_i.add(i[0])
                            vector_j.add(i[2:])
                    if len(vector_j) == 1 or len(vector_i) == 1:
                        if len(cords) > 1:
                            if len(vector_i) != 1:
                                z = checks_index(vector_i, self.y)
                            else:
                                z = checks_index(vector_j, self.x)
                            if not z:
                                return False
                        x1, y1 = self.grey_zone(cords)
                        for i in y1:
                            for j in x1:
                                if self.board[f'{i},{j}'] == 0:
                                    continue
                                return False
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False


def checks_index(res, lister):
    res = list(res)
    res.sort()
    if res[0] in lister:
        j = lister.index(res[0])
    else:
        res = list(map(int, res))
        res.sort()
        j = lister.index(int(res[0]))
    for i in res:
        # print(type(i),type(lister[j]), end='')
        if j == lister.index(i):
            j -= -1
        else:
            return False
    return True


if '__main__' == __name__:
    mywarboard = MyBoard('myboard')
    warboard = EnemyBoard('warboard')
    lodka4 = Ships(4)
    lodka3 = Ships(3)
    lodka2 = Ships(2)
    lodka1 = Ships(1)

    print(mywarboard.addShips(lodka4, "j,7", "j,8", "j,9", "j,10"))
    print(mywarboard.addShips(lodka3, "a,2", "b,2", "c,2"))
    print(mywarboard.addShips(lodka2, "f,5", "f,4", ))
    print(mywarboard.addShips(lodka1, "a,9"))

    # mywarboard.printBoard()
    for i in ('a,1', 'a,9', 'a,2', 'd,3', 'a,3', 'b,2', 'c,2', 'j,7', 'j,8', 'j,9', 'j,10'):
        print(warboard.shot(i, mywarboard))
    print(mywarboard)
    mywarboard.printBoard()
    warboard.printBoard()
