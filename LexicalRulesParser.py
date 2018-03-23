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
    regular_definitions = parse_regular_definitions(regular_definitions_lines)
    regular_expressions = parse_regular_expressions(regular_expressions_lines, regular_definitions)
    return {
        'regular_expressions': regular_expressions,
        'regular_definitions': regular_definitions,
        'keywords': keywords,
        'punctuations': punctuations
    }


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


def parse_regular_definitions(lines):
    """
    this function parses regular definition lines
    accepted rules: ranges (a-m, 0-9), regex symbols (- | + * ( ))
    no concatenation or static words are accepted as no regular definition will have ones.
    :param lines: list of strings each represent regular definition rule
    :return: dict with keys as tokens and values as valid regular expressions
    """
    result = {}
    symbols = ['|', '+', '*', '(', ')']
    upper_range_start = False
    lower_range_start = False
    number_range_start = False
    hyphen_found = False
    for line in lines:
        rhs_buffer = ''
        word_buffer = ''
        equal_index = line.index('=')
        LHS = line[:equal_index].strip()
        RHS = line[equal_index + 1:].strip()
        for (index, char) in enumerate(RHS):
            # characters Range handling (e.g a-z)
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
                rhs_buffer += str('|'.join(upper_chars[upper_chars.index(upper_range_start):upper_chars.index(char) + 1]))
                upper_range_start = False
                hyphen_found = False
            elif lower_range_start and hyphen_found:
                rhs_buffer += str('|'.join(lower_chars[lower_chars.index(lower_range_start):lower_chars.index(char) + 1]))
                lower_range_start = False
                hyphen_found = False
            elif number_range_start and hyphen_found:
                rhs_buffer += str('|'.join(numbers[numbers.index(number_range_start):numbers.index(char) + 1]))
                number_range_start = False
                hyphen_found = False
            else:
                upper_range_start = False
                lower_range_start = False
                number_range_start = False
                hyphen_found = False

            # predefined tokens/words handling (e.g digit+)
            if char not in symbols:
                word_buffer += char
            else:
                if word_buffer and result.get(word_buffer):
                    rhs_buffer += '('
                    rhs_buffer += result[word_buffer]
                    rhs_buffer += ')'
                    rhs_buffer += char
                else:
                    rhs_buffer += char
                word_buffer = ''

            # if last word in the line with no symbols (e.g letter+digit)
            if index == (len(RHS) - 1):
                if result.get(word_buffer):
                    rhs_buffer += '('
                    rhs_buffer += result[word_buffer]
                    rhs_buffer += ')'

        result[LHS] = rhs_buffer
    return result


def parse_regular_expressions(lines, regular_definitions):
    symbols = ['+', '*', '|', '(', ')', '.']
    result = {}
    for line in lines:
        rhs_buffer = ''
        word_buffer = ''
        skip_iteration = False
        colon_index = line.index(':')
        LHS = line[:colon_index].strip()
        RHS = line[colon_index + 1:].strip()
        for (index, char) in enumerate(RHS):
            if skip_iteration:
                skip_iteration = False
                continue
            if char == ' ':
                continue
            if char == '\\':
                next_char = RHS[index + 1]
                if next_char == 'L':
                    rhs_buffer += '$'
                else:
                    rhs_buffer += next_char
                skip_iteration = True
                continue
            if (char not in symbols) and (char in upper_chars or char in lower_chars):
                word_buffer += char
            else:
                if word_buffer:
                    rhs_buffer += '('
                    if regular_definitions.get(word_buffer):
                        # predefined regular definition
                        rhs_buffer += regular_definitions[word_buffer]
                    else:
                        # static word: keep the word as is
                        rhs_buffer += word_buffer
                    rhs_buffer += ')'
                # it is a symbol always push into buffer and clear the word buffer
                rhs_buffer += char
                word_buffer = ''
        result[LHS] = rhs_buffer
    return result

print(start_parsing('inputs/lexical-rules.txt'))
# print(upper_chars)
