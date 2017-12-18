import generate_instructions as gi

"""
Block tests
"""

def test_block_inequality_with_generated_ids():
    assert gi.Block('A', 'BLUE', 'B', 'GREEN', (0, 0)) \
        != gi.Block('A', 'BLUE', 'B', 'GREEN', (0, 0))

def test_block_equality_with_given_ids():
    assert gi.Block('A', 'BLUE', 'B', 'GREEN', (0, 0), 30) \
        == gi.Block('D', 'YELLOW', 'C', 'ORANGE', (-1, 2), 30)

def test_block_shift_to_keeps_id():
    base_block = gi.Block('A', 'BLUE', 'B', 'GREEN', (0, 0))
    shifted_block = base_block.shift_to((2, 3))

    assert base_block.block_id == shifted_block.block_id

def test_block_shift_to_keeps_visuals():
    base_block = gi.Block('A', 'BLUE', 'B', 'GREEN', (0, 0))
    shifted_block = base_block.shift_to((2, 3))

    assert base_block.side1_letter == shifted_block.side1_letter
    assert base_block.side1_color == shifted_block.side1_color
    assert base_block.side2_letter == shifted_block.side2_letter
    assert base_block.side2_color == shifted_block.side2_color

def test_block_shift_to_updates_pos():
    new_pos = (2, 3)
    base_block = gi.Block('A', 'BLUE', 'B', 'GREEN', (0, 0))
    shifted_block = base_block.shift_to(new_pos)

    assert shifted_block.position == new_pos

def test_block_flip_keeps_block_id():
    base_block = gi.Block('A', 'BLUE', 'B', 'GREEN', (0, 0))
    flipped_block = base_block.flip()

    assert base_block.block_id == flipped_block.block_id


def test_block_flip_keeps_pos():
    base_block = gi.Block('A', 'BLUE', 'B', 'GREEN', (0, 0))
    flipped_block = base_block.flip()

    assert base_block.position == flipped_block.position

def test_block_flip_swaps_visuals():
    base_block = gi.Block('A', 'BLUE', 'B', 'GREEN', (0, 0))
    flipped_block = base_block.flip()

    assert base_block.side1_letter == flipped_block.side2_letter
    assert base_block.side1_color == flipped_block.side2_color
    assert base_block.side2_letter == flipped_block.side1_letter
    assert base_block.side2_color == flipped_block.side1_color


"""
Configuration
"""

def test_is_complete_empty_current_empty_final():
    assert gi.Configuration([], []).is_complete()

def test_is_complete_nonempty_current_empty_final():
    assert not gi.Configuration([1], []).is_complete()

def test_is_complete_nonempty_current_nonempty_final():
    assert not gi.Configuration([1], [2]).is_complete()

def test_get_instruction_phrase():
    moved_block = gi.Block('A', 'BLUE', 'B', 'GREEN', (1, 2))
    instruction = gi.Configuration.get_instruction(moved_block)

    assert 'A' in instruction.phrase
    assert 'BLUE' in instruction.phrase

def test_get_instruction_point():
    moved_block = gi.Block('A', 'BLUE', 'B', 'GREEN', (1, 2))
    instruction = gi.Configuration.get_instruction(moved_block)

    assert instruction.point == (1, 2)
