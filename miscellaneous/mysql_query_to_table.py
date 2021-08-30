import copy
import datetime
import re

from prettytable import PrettyTable


class Table(PrettyTable):
    FILTERS = {
        # 'like': {
        #     'json': 'added_before_chat_ready'
        # },
        'equal_to': {
            'threadid': '761797'
        }
    }

    def __init__(self):
        super(Table, self).__init__()

    def has_field_names(self):
        return bool(self.field_names)

    def initialize_field_names(self, raw_row: str):
        self.field_names = self._prepare(raw_row)

    def append_row(self, raw_row: str):
        self.add_row(self._prepare(raw_row))

    @staticmethod
    def _prepare(raw_row: str):
        return [field.strip() for field in raw_row.split('|') if len(field) > 0]

    def _keep_row(self, row):
        for filter_category, filters in Table.FILTERS.items():
            for filter_name, filter_value in filters.items():
                field_index = self.field_names.index(filter_name)
                if filter_category == 'like':
                    if filter_value not in row[field_index]:
                        return False
                elif filter_category == 'equal_to':
                    if filter_value != row[field_index]:
                        return False
        return True

    def _make_ts_fields_human_readable(self, row):
        for field_name in ['createdts', 'insertedts', 'modifiedts', 'updatedts']:
            field_index = self._field_names.index(field_name)
            row[field_index] = datetime.datetime.fromtimestamp(int(row[field_index]) / 1e6).strftime('%Y-%m-%d %H:%M:%S')
        return row

    def _get_rows(self, options):
        rows = copy.deepcopy(self._rows)
        if options["oldsortslice"]:
            rows = rows[options["start"]: options["end"]]

        rows = [self._make_ts_fields_human_readable(row) for row in rows if self._keep_row(row)]

        # Sort
        if options["sortby"]:
            sortindex = self._field_names.index(options["sortby"])
            # Decorate
            rows = [[row[sortindex]] + row for row in rows]
            # Sort
            rows.sort(reverse=options["reversesort"], key=options["sort_key"])
            # Undecorate
            rows = [row[1:] for row in rows]

        # Slice if necessary
        if not options["oldsortslice"]:
            rows = rows[options["start"]: options["end"]]

        return rows


def main(path):
    table = Table()
    with open(path) as f:
        for line in f.readlines():
            # line = bytes(line, encoding='raw_unicode_escape').decode('utf-8')
            if re.match(r'^[-|+]+$', line):
                continue
            if table.has_field_names():
                table.append_row(line)
            else:
                table.initialize_field_names(line)

    table.align = 'l'
    # table.max_width = 50

    print(table.get_string(fields=[
        'threadid', 'message', 'createdts', 'insertedts', 'modifiedts', 'updatedts'
    ]))


if __name__ == '__main__':
    main('/home/k9173a/Downloads/chatmessage_202108271750.txt')
