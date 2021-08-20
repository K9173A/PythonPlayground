"""
Позволяет извлекать список коммитов в иерархии директорий.
Коммиты сортируются по дате, чтобы их можно было потом последовательно черри-пикнуть в другую ветку.
"""


import datetime
import operator
import os
import re
import subprocess


def fetch_file_commits(file_path):
    p1 = subprocess.Popen(
        ['git', 'log', '--follow', '--', file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    p2 = subprocess.Popen(
        ['grep', '-E', '(commit|Author|Date)'],
        stdin=p1.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    out, _ = p2.communicate()

    out = list(zip(*[iter(out.decode('utf-8').split('\n'))] * 3))

    for index, data in enumerate(out):
        formatted_data = datetime.datetime.strptime(' '.join(re.split(r'\s+', data[2])[2:6]), '%b %d %H:%M:%S %Y')
        out[index] = (data[0], data[1], formatted_data)

    return out


def commit_exists(commits, commit_hash):
    for _hash, author, date in commits:
        if _hash == commit_hash:
            return True
    return False


def main(root_directory):
    commits = []
    for current_path, _, child_files in os.walk(root_directory):
        for child_file in child_files:
            current_file_commits = fetch_file_commits(os.path.join(current_path, child_file))
            commits.extend(commit for commit in current_file_commits if not commit_exists(commits, commit[0]))

    commits = sorted(commits, key=operator.itemgetter(2))
    for _hash, author, date in commits:
        print(_hash, author, date)


if __name__ == '__main__':
    main('/home/k9173a/dev/')
