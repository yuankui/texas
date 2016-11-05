# coding=utf-8
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

class Card:
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
            if not 2 <= int(num) <= 14:
                raise Exception("invalid card {}{}".format(num, color))
            if not 'A' <= color <= 'D':
                raise Exception('invalid card {}{}'.format(num, color))

            cards.append(Card(int(num), color))
        return cards


# 一期：
#     简单统计每种牌的概率即可
#        1. 判断牌
#        2. 单测
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
            return func.func_name
    return None


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


if __name__ == '__main__':
    cards = Card.create('14A 12AA')

    func = group_cards

    print func
