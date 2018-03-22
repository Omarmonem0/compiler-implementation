lower_chars = [chr(x) for x in range(ord('a'), ord('a') + 26)]
upper_chars = [chr(x) for x in range(ord('A'), ord('A') + 26)]
numbers = [chr(x) for x in range(ord('0'), ord('0') + 10)]


def start_parsing(file_name):
    regular_definitions_lines = []
    regular_expressions_lines = []
    keywords = []
    punctuations = []
    file = open(file_name, 'r')
    content = file.read()
    for line in content.split('\n'):
        if line == '':
            continue
        line = line.strip()
        if check_if_regular_definition(line):
            regular_definitions_lines.append(line)
        if check_if_regular_expression(line):
            regular_expressions_lines.append(line)
        if check_if_keywords(line):
            line_keywords = get_keywords_from_line(line)
            keywords.extend(line_keywords)
        if check_if_punctuations(line):
            line_punctuations = get_punctuations_from_line(line)
            punctuations.extend(line_punctuations)
    regular_definitions = parse_regular_definition(regular_definitions_lines)
    print(regular_expressions_lines)
    print(regular_definitions_lines)
    print(keywords)
    print(punctuations)
    print(regular_definitions)


def check_char_not_escaped(line, char, must_be_before):
    char_index = line.find(char)
    must_be_before_index = line.find(must_be_before)
    if must_be_before_index != -1 and must_be_before_index < char_index:
        return False
    elif char_index != -1 and line[char_index - 1] != '\\':
        return True
    else:
        return False


def check_if_regular_definition(line):
    return check_char_not_escaped(line, '=', ':')


def check_if_regular_expression(line):
    return check_char_not_escaped(line, ':', '=')


def check_if_keywords(line):
    return line[0] == '{' and line[len(line) - 1] == '}'


def check_if_punctuations(line):
    return line[0] == '[' and line[len(line) - 1] == ']'


def get_keywords_from_line(line):
    return line.replace('{', '').replace('}', '').strip().split(' ')


def get_punctuations_from_line(line):
    stripped_line = line[1:len(line) - 1]
    modified_line = stripped_line.replace(' ', '').strip()
    return [x for x in modified_line]


def parse_regular_definition(lines):
    result = {}
    upper_range_start = False
    lower_range_start = False
    number_range_start = False
    hyphen_found = False
    for line in lines:
        buffer = ''
        LHS = line.split('=')[0].strip()
        RHS = line.split('=')[1].strip()
        for char in RHS:
            if char == ' ':
                continue
            elif char in upper_chars and not hyphen_found:
                upper_range_start = char
            elif char in lower_chars and not hyphen_found:
                lower_range_start = char
            elif char in numbers and not hyphen_found:
                number_range_start = char
            elif char == '-':
                hyphen_found = True
            elif upper_range_start and hyphen_found:
                buffer += str('|'.join(upper_chars[upper_chars.index(upper_range_start):upper_chars.index(char) + 1]))
                upper_range_start = False
                hyphen_found = False
            elif lower_range_start and hyphen_found:
                buffer += str('|'.join(lower_chars[lower_chars.index(lower_range_start):lower_chars.index(char) + 1]))
                lower_range_start = False
                hyphen_found = False
            elif number_range_start and hyphen_found:
                buffer += str('|'.join(numbers[numbers.index(number_range_start):numbers.index(char) + 1]))
                number_range_start = False
                hyphen_found = False
            elif char == '|':
                buffer += char
            else:
                upper_range_start = False
                lower_range_start = False
                number_range_start = False
                hyphen_found = False
        result[LHS] = buffer
    return result



start_parsing('inputs/lexical-rules.txt')
# print(upper_chars)
