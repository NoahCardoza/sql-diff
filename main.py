import sys

diff = sys.stdin.read()

def split_sections(diff):
    """
    takes a git diff and breaks it up into sections
    :param diff: a diff piped from git
    :return: a list of sections
    """
    sections = []
    section = ''

    for line in diff.splitlines():
        line = line.strip()
        if line.startswith('@@'):
            if section:
                sections.append(section)
            section = line
            continue

        if line and section.startswith('@@'):
            section += '\n' + line

    sections.append(section)
    return sections


sections = split_sections(diff)


for section in sections:
    header = section.splitlines()[0]
    cmd = header.split('@@ ')[2]
    # only filter out create table sections
    if cmd[:12].upper() == 'CREATE TABLE':
        table = cmd.split()[2].replace('`', '')
        args = section.split('(', 1)[1].rsplit(')', 1)[0].split(',')
        sub = set()
        add = set()
        for arg in args:
            arg = arg.strip()
            if arg:
                diff_stat = arg[0]
                if diff_stat == '+':
                    add.add(arg[1:].strip().replace('`', ''))
                elif diff_stat == '-':
                    sub.add(arg[1:].strip().replace('`', ''))
        # check if there are differences
        if add - sub:
            for a, s in zip(add, sub):
                a_specs = a.split()
                s_specs = s.split()
                if a_specs[0] != s_specs[0]:
                    print('err: columns do not match  ({} & {})',format(a_specs[0], s_specs[0]))
                    continue
                print('alter table {} modify {};'.format(
                    table,
                    a
                ))
    else:
        print('err: cannot process statements other than `CREATE TABLE`')