from dataclasses import dataclass, field


@dataclass
class State:
    instruction_ptr: int = 0
    registers: list[int] = field(default_factory=lambda: [0, 0, 0])
    output: list[int] = field(default_factory=list)


def _get_combo_value(operand: int, state: State) -> int:
    if 0 <= operand <= 3:
        return operand
    elif 4 <= operand <= 6:
        return state.registers[operand - 4]
    else:
        raise ValueError


def adv(operand: int, state: State) -> State:
    numerator = state.registers[0]
    denominator = 2 ** _get_combo_value(operand, state)
    state.registers[0] = numerator // denominator
    return state


def bxl(operand: int, state: State) -> State:
    state.registers[1] = state.registers[1] ^ operand
    return state


def bst(operand: int, state):
    state.registers[1] = _get_combo_value(operand, state) % 8
    return state


def jnz(operand, state):
    if state.registers[0] != 0:
        state.instruction_ptr = operand
    return state


def bxc(operand, state):
    state.registers[1] = state.registers[1] ^ state.registers[2]
    return state


def out(operand, state):
    state.output.append(_get_combo_value(operand, state) % 8)
    return state


def bdv(operand, state):
    numerator = state.registers[0]
    denominator = 2 ** _get_combo_value(operand, state)
    state.registers[1] = numerator // denominator
    return state


def cdv(operand, state):
    numerator = state.registers[0]
    denominator = 2 ** _get_combo_value(operand, state)
    state.registers[2] = numerator // denominator
    return state


def execute_program(program: list[int], state):
    ops = [
        adv,
        bxl,
        bst,
        jnz,
        bxc,
        out,
        bdv,
        cdv,
    ]

    while state.instruction_ptr < len(program):
        prev_ptr = state.instruction_ptr
        operation = ops[program[state.instruction_ptr]]
        operand = program[state.instruction_ptr + 1]
        state = operation(operand, state)
        if state.instruction_ptr == prev_ptr:
            state.instruction_ptr += 2
    return state


# state = execute_program(
#     [0, 1, 5, 4, 3, 0],
#     State(registers=[729, 0, 0]),
# )
# print(state)

# state = execute_program(
#     [2, 4, 1, 3, 7, 5, 1, 5, 0, 3, 4, 1, 5, 5, 3, 0],
#     State(registers=[21539243, 0, 0]),
# )
# print(state)

program = [2, 4, 1, 3, 7, 5, 1, 5, 0, 3, 4, 1, 5, 5, 3, 0]
for i in range(2**20, 2**30):
    state = State(registers=[i, 0, 0])
    final_state = execute_program(program, state)
    if final_state.output == program:
        print(i)
        break
