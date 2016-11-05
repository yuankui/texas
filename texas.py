# coding=utf-8
import random
import re
import sys

#
# 输入已有的几张牌，然后程序自动随机生成剩余的牌10000+次，算出一个综合得分，以及得出一个继续操作的建议
# TODO 引入其他的的攻击行为因素
#
# 牌的表示
# 点数：2,3,4,5,6,7,8,9,10,11,12,13,14(A)
# 花色：A（黑桃）,B（梅花）,C（红桃）,D（方片）
# 比如红桃8可以用8C表示，梅花A用14B表示
import card_map


class Card(object):
    def __init__(self, num, color):
        self.num = num
        self.color = color

    def __repr__(self):
        return '{}{}'.format(self.num, self.color)

    @staticmethod
    def create(card_str):
        regex = re.compile(r'(\d+)([a-zA-Z])')
        matches = regex.findall(card_str)

        cards = []
        for num, color in matches:
            if not (2 <= int(num) <= 14):
                raise Exception("invalid card {}-{}".format(num, color))
            if not 'A' <= color <= 'D':
                raise Exception('invalid card {}-{}'.format(num, color))

            cards.append(Card(int(num), color))
        return cards


# 一期：
#     简单统计每种牌的概率即可
#       1. 判断牌
#       2. 单测
#       3. 随机发剩下的牌
#       4. 去掉两张，判断剩下的5张牌 TODO
# 二期：
#     算出一个综合分
def judge_cards(cards):
    """根据五张牌，判断这是什么样的五张牌，同花顺？葫芦？同花？"""
    funcions = [is_straight_flush,
                is_four_of_a_kind,
                is_full_house,
                is_flush,
                is_straight,
                is_three_of_a_kind,
                is_two_pairs,
                is_one_pair,
                ]
    for is_func in funcions:
        if is_func(cards):
            return is_func.func_name
    return ""


def is_royal_flush(cards):
    """由于这种概率极低，也忽略吧，对统计整体结果没有太大影响"""
    pass


def is_straight_flush(cards):
    return is_straight(cards) and is_flush(cards)


def is_four_of_a_kind(cards):
    card_num_map = group_cards(cards)
    return any(num == 4 for num in card_num_map.values())


def is_full_house(cards):
    card_num_map = group_cards(cards)
    card_nums = sorted(card_num_map.values())
    return card_nums[0] == 2 and card_nums[1] == 3


def is_flush(cards):
    return len(set(map(lambda x: x.color, cards))) == 1


def is_straight(cards):
    nums = map(lambda x: x.num, cards)
    nums = sorted(nums)
    return nums[-1] - nums[0] == 4


def is_three_of_a_kind(cards):
    card_num_map = group_cards(cards)
    return any(num == 3 for num in card_num_map.values())


def is_two_pairs(cards):
    card_num_map = group_cards(cards)
    pairs = filter(lambda x: x == 2, card_num_map.values())
    return len(pairs) >= 2


def is_one_pair(cards):
    card_num_map = group_cards(cards)
    return any(num == 2 for num in card_num_map.values())


def is_high_card(cards):
    """由于high是普通牌，所以直接忽略"""
    pass


def group_cards(cards):
    card_num_map = {}
    for card in cards:
        card = card.num
        num = card_num_map.get(card, 0)
        card_num_map[card] = num + 1

    return card_num_map


card_score_map = {
    is_royal_flush.func_name: 11,
    is_straight_flush.func_name: 10,
    is_four_of_a_kind.func_name: 9,
    is_full_house.func_name: 8,
    is_flush.func_name: 7,
    is_straight.func_name: 6,
    is_three_of_a_kind.func_name: 5,
    is_two_pairs.func_name: 4,
    is_one_pair.func_name: 3,
    '': 2
}

rand = random.Random()


def generate_card(card_str_set):
    global rand

    while True:
        card_seq = rand.randint(0, 51)
        card = card_map.car_map[card_seq]
        if str(card) not in card_str_set:
            return card


def try_five(cards, current, left):
    if left + len(current) < 5:
        return set()

    if len(current) == 5:
        return set([judge_cards(current)])

    current.append(cards[len(cards) - left])
    first = try_five(cards, current, left - 1)
    current.pop()
    second = try_five(cards, current, left - 1)

    return first.union(second)


def get_card_func(cards):
    funcs = try_five(cards, [], 7)
    return funcs


def try_rand_cards(cards):
    cards = cards[:]
    card_str_set = set(map(str, cards))

    for i in range(7 - len(cards)):
        card = generate_card(card_str_set)
        cards.append(card)
        card_str_set.add(str(card))

    funcs = get_card_func(cards)

    funcs = sorted(funcs, key=lambda x:card_score_map[x])
    return funcs[-1]

if __name__ == '__main__':

    # 获取已有牌
    inp = " ".join(sys.argv[1:])
    cards = Card.create(inp)

    if len(cards) >= 7:
        raise Exception("card is full")

    # 模拟不发剩余牌
    func_num_map = {}
    for j in range(100):
        func = try_rand_cards(cards)
        num = func_num_map.get(func, 0)
        func_num_map[func] = num + 1

    print func_num_map