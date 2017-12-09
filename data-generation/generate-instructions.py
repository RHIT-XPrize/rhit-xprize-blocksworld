

from random import randint, random


"""

Classes

"""

class NoActionException(Exception):
    pass


class Block:
    def __init__(self, side1_letter,
                 side1_color,
                 side2_letter,
                 side2_color,
                 pos):
        self.side1_letter = side1_letter
        self.side1_color = side1_color
        self.side2_letter = side2_letter
        self.side2_color = side2_color
        self.position = pos

    def __eq__(self, other):
        return self.side1_letter == other.side1_letter and \
            self.side2_letter == other.side2_letter and \
            self.side1_color == other.side1_color and \
            self.side2_color == other.side2_color

    def __ne__(self, other):
        return not self == other

    def shift_to(self, position):
        return Block(self.side1_letter,
                     self.side1_color,
                     self.side2_letter,
                     self.side2_color,
                     position)

    def flip(self):
        return Block(self.side2_letter,
                     self.side2_color,
                     self.side1_letter,
                     self.side1_color,
                     self.position)

    def __str__(self):
        return '{side1: (%s, %s), side2: (%s, %s), pos: %s}' % \
            (self.side1_letter, self.side1_color,
             self.side2_letter, self.side2_color,
             self.position)


class Instruction:
    def __init__(self, phrase, point):
        self.phrase = phrase
        self.point = point

    def __str__(self):
        return self.phrase


class Configuration:
    def __init__(self, blocks, final_blocks=[]):
        self.current_blocks = blocks
        self.final_blocks = final_blocks

    def is_complete(self):
        return self.current_blocks == []

    def get_instruction(self, moved_block):
        point = moved_block.position
        phrase = 'move the %s %s block here: %s' \
                 % (moved_block.side1_color,
                    moved_block.side1_letter,
                    point)
        return Instruction(phrase, point)

    def get_action(self, goal):
        if self.is_complete():
            raise NoActionException('Board is already complete')

        block_to_move = rand_element(self.current_blocks)
        moved_block = goal.final_blocks[goal.final_blocks.index(block_to_move)]
        # moved_block = rand_element(goal.final_blocks)
        new_current_blocks = self.current_blocks[:]
        new_current_blocks.remove(moved_block)
        # new_current_blocks = [
        #     b for b in self.current_blocks if b != moved_block
        # ]
        new_configuration = Configuration(
            new_current_blocks,
            self.final_blocks + [moved_block]
        )
        instruction = self.get_instruction(moved_block)
        return Action(self, new_configuration, instruction)

    def scatter(self):
        return Configuration(list(map(randomize_block,
                                      self.current_blocks + self.final_blocks)))

    def __str__(self):
        # :(
        return str(list(map(str, self.current_blocks + self.final_blocks)))

    def mark_complete(self):
        return FinalConfiguration(self.current_blocks + self.final_blocks)


class FinalConfiguration(Configuration):
    def __init__(self, blocks):
        self.current_blocks = []
        self.final_blocks = blocks


class Action:
    def __init__(self, start_conf, end_conf, phrase):
        self.start_conf = start_conf
        self.end_conf = end_conf
        self.phrase = phrase

    def __str__(self):
        return str(self.phrase)


"""

Random actions

"""

def rand_element(ls):
    return ls[rand_index(ls)]


def rand_index(ls):
    return randint(0, len(ls) - 1)


def random_position():
    return (randint(0, 1000), randint(0, 1000))


def random_block(letters, colors):
    l = len(letters) - 1
    c = len(colors) - 1
    side1_letter = letters[randint(0, l)]
    side2_letter = letters[randint(0, l)]
    side1_color  = colors[randint(0, c)]
    side2_color  = colors[randint(0, c)]
    position = random_position()
    return Block(side1_letter, side1_color, side2_letter, side2_color, position)


def randomize_block(block):
    def maybe_flip(b):
        if random() < 0.5:
            # return b.flip()
            pass
        return b
    def maybe_shift(b):
        if random() < 0.95:
            return b.shift_to(random_position())
        return b
    return maybe_flip(maybe_shift(block))


def random_configuration(num_blocks, letters, colors):
    blocks = [random_block(letters, colors) for i in range(num_blocks)]
    return Configuration(blocks)


"""

Not random actions

"""

def solve_board(current_config, goal_config):
    try:
        action = current_config.get_action(goal_config)
        rest = solve_board(action.end_conf, goal_config)
        return [action] + rest
    except NoActionException as e:
        return []

"""

Entry point

"""

def main():
    colors = ['RED', 'GREEN', 'BLUE']
    letters = ['A', 'B', 'C']
    start = random_configuration(2, letters, colors)
    end = start.scatter().mark_complete()

    b = random_block(colors, letters)
    b_prime = b.shift_to(random_position())

    print('start: %s' % start)
    print('end: %s' % end)
    print()
    print('actions: %s' % str(list(map(str, solve_board(start, end)))))


if __name__ == '__main__':
    main()
