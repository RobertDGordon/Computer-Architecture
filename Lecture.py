PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3
PRINT_REG = 4

memory = [
    PRINT_BEEJ,
    SAVE_REG,
    0,
    12,
    PRINT_REG,
    0,
    PRINT_BEEJ,
    HALT
]

registers = [0, 0, 0, 0, 0, 0, 0, 0]

halted = False

pc = 0

while not halted:
    instruction = memory[pc]

    if instruction == PRINT_BEEJ:
        print("Beej!")
        pc += 1
    elif instruction == SAVE_REG:
        reg_num = memory[pc + 1]
        value = memory[pc + 2]
        registers[reg_num] = value
        pc += 3
    elif instruction == PRINT_REG:
        reg_num = memory[pc + 1]
        print(registers[reg_num])
        pc += 2
    elif instruction == HALT:
        halted = True
    else:
        print(f'Unknown instruction {instruction} at address {pc}')
        exit(1)
