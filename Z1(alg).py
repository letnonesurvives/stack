import traceback


class TestRunner(object):
    def __init__(self, name):
        self.name = name
        self.testNo = 1

    def expectTrue(self, cond):
        try:
            if cond():
                self._pass()
            else:
                self._fail()
        except Exception as e:
            self._fail(e)

    def expectFalse(self, cond):
        self.expectTrue(lambda: not cond())

    def expectException(self, block):
        try:
            block()
            self._fail()
        except:
            self._pass()

    def _fail(self, e=None):
        print(f'FAILED: Test  # {self.testNo} of {self.name}')
        self.testNo += 1
        if e is not None:
            traceback.print_tb(e.__traceback__)

    def _pass(self):
        print(f'PASSED: Test  # {self.testNo} of {self.name}')
        self.testNo += 1


def match(string, pattern):
    if len(string) != len(pattern):
        return False
    for i in range(len(string)):
        if pattern[i] == "a":
            if string[i] not in "abcdefghigklmnopkrstuvwxyz":
                return False
        if pattern[i] == "d":
            if string[i] not in "1234567890":
                return False
        if pattern[i] == "*":
            if string[i] not in "abcdefghigklmnopkrstuvwxyz1234567890":
                return False
        if pattern[i] == " ":
            if string[i] != " ":
                return False
    if ("a" not in pattern) and ("d" not in pattern) and (" " not in pattern) and ("*" not in pattern):
        raise Exception("forbidden symbol")

    return True




def testMatch():
    runner = TestRunner('match')

    runner.expectFalse(lambda: match('xy', 'a'))
    runner.expectFalse(lambda: match('x', 'd'))
    runner.expectFalse(lambda: match('0', 'a'))
    runner.expectFalse(lambda: match('*', ' '))
    runner.expectFalse(lambda: match(' ',  'a'))

    runner.expectTrue(lambda:  match('01 xy', 'dd aa'))
    runner.expectTrue(lambda: match('1x', '**'))

    runner.expectException(lambda:  match('x', 'w'))


tasks = {
    'id': 0,
    'name': 'Все задачи',
    'children': [
        {
            'id': 1,
            'name': 'Разработка',
            'children': [
                {'id': 2, 'name': 'Планирование разработок', 'priority': 1},
                {'id': 3, 'name': 'Подготовка релиза', 'priority': 4},
                {'id': 4, 'name': 'Оптимизация', 'priority': 2},
            ],
        },
        {
            'id': 5,
            'name': 'Тестирование',
            'children': [
                {
                    'id': 6,
                    'name': 'Ручное тестирование',
                    'children': [
                        {'id': 7, 'name': 'Составление тест-планов', 'priority': 3},
                        {'id': 8, 'name': 'Выполнение тестов', 'priority': 6},
                    ],
                },
                {
                    'id': 9,
                    'name': 'Автоматическое тестирование',
                    'children': [
                        {'id': 10, 'name': 'Составление тест-планов', 'priority': 3},
                        {'id': 11, 'name': 'Написание тестов', 'priority': 3},
                    ],
                },
            ],
        },
        {'id': 12, 'name': 'Аналитика', 'children': []},
    ],
}


def findMaxPriority(tasks, MaxPriority):
    a = None
    if "priority" not in tasks.keys():
        for i in tasks["children"]:
            b = findMaxPriority(i, MaxPriority)
            try:
                if b["priority"] > MaxPriority:
                    a = b
                    MaxPriority = b["priority"]
            except:
                pass
    else:
        if tasks["priority"] > MaxPriority:
            a = tasks
    return a


def findTaskHavingMaxPriorityInGroup(tasks, groupId):
    if FindException(tasks, groupId) != True:
        raise Exception("Exception")
    return mainfunction(tasks, groupId)


def mainfunction(tasks, groupId):
    a = None
    MaxPriority = -1
    if tasks["id"] == groupId and "priority" not in tasks.keys() and tasks["children"] != []:
        for i in tasks["children"]:
            b = findMaxPriority(i, MaxPriority)
            try:
                if b["priority"] > MaxPriority:
                    a = b
                    MaxPriority = b["priority"]
            except:
                pass
        return a
    elif tasks["id"] == groupId and tasks["children"] == []:
        return None
    elif tasks["id"] == groupId and "priority" in tasks.keys():
        raise Exception("Some Exception")
    elif "priority" not in tasks.keys():
        for i in tasks["children"]:
            b = mainfunction(i, groupId)
            try:
                if b["priority"] > MaxPriority:
                    a = b
                    MaxPriority = b["priority"]
            except:
                pass
        return a


def FindException(tasks, groupId):
    if "children" in tasks.keys() and groupId != tasks["id"]:
        for i in tasks["children"]:
            if FindException(i, groupId) == True:
                return True
    elif tasks["id"] == groupId:
        return True
    return False


def taskEquals(a, b):
    return (
        not 'children' in a and
        not 'children' in b and
        a['id'] == b['id'] and
        a['name'] == b['name'] and
        a['priority'] == b['priority']
    )


def testFindTaskHavingMaxPriorityInGroup():
    runner = TestRunner('findTaskHavingMaxPriorityInGroup')

    runner.expectException(lambda: findTaskHavingMaxPriorityInGroup(tasks, 13))
    runner.expectException(lambda: findTaskHavingMaxPriorityInGroup(tasks, 2))

    runner.expectTrue(lambda: findTaskHavingMaxPriorityInGroup(tasks, 12) is None)

    runner.expectTrue(lambda: taskEquals(findTaskHavingMaxPriorityInGroup(tasks, 0), {
        'id': 8,
        'name': 'Выполнение тестов',
        'priority': 6,
    }))
    runner.expectTrue(lambda: taskEquals(findTaskHavingMaxPriorityInGroup(tasks, 1), {
        'id': 3,
        'name': 'Подготовка релиза',
        'priority': 4,
    }))

    runner.expectTrue(lambda: findTaskHavingMaxPriorityInGroup(tasks, 9)['priority'] == 3)


testMatch()
testFindTaskHavingMaxPriorityInGroup()