"""
В Confluence простым способом не вставить таблицу. Нужно использовать макрос, либо вручную заполнять таблицу.
Макросы далеко не всегда работают, плюс в них едет выравнивание таблицы. А вручную заполнять таблицу на 1000 строк
вряд ли кто будет. Альтернативное решение:
1. Указать путь до файла с исходной таблицей, данные которой нужно извлечь и вставить в Confluence.
2. Указать путь до файла, в который будет записан результат работы данного скрипта - Confluence-like таблица.
3. Выполнить скрипт.
4. Открыть Confluence, нажать "Редактировать" на странице, куда будет вставляться таблица. Открыть консоль браузера
   и вставить следующий код, заменив `<HTML_CONTENT_HERE>` на html-код таблицы, сгенерированный данным скриптом.
   parser = new DOMParser();
   tinymce = document.getElementById('tinymce');
   str = `<HTML_CONTENT_HERE>`;
   parsedHtml = parser.parseFromString(str, 'text/html');
   tableDiv = parsedHtml.querySelector('div');
   tinymce.appendChild(tableDiv);
"""

from pathlib import Path

from bs4 import BeautifulSoup


def make_link(url: str, content: str) -> str:
    return f'<a class="external-link" href="{url}" style="text-align: left;" rel="nofollow">{content}</a>'


def main(input_html_file_path: Path, output_html_file_path: Path) -> None:
    visible_header_row = BeautifulSoup('''
    <thead class="tableFloatingHeaderOriginal">
        <tr role="row" class="tablesorter-headerRow"></tr>
    </thead>
    ''', features='html.parser')

    hidden_header_row = BeautifulSoup('''
    <thead class="tableFloatingHeader" style="display: none;">
        <tr role="row" class="tablesorter-headerRow"></tr>
    </thead>
    ''', features='html.parser')

    header_columns = ['Проект', 'Задача', 'Тема', 'Приоритет', 'Статус', 'Файлы', 'Связанные задачи', 'Описание']
    for index, column_title in enumerate(header_columns):
        visible_header_column_html = '''
        <th class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted"
            data-column="{column_index}" tabindex="0" scope="col" role="columnheader" aria-disabled="false"
            unselectable="on" aria-sort="none" style="user-select: none; min-width: 8px; max-width: none;"
            aria-label="Задача: No sort applied, activate to apply an ascending sort">
            <div class="tablesorter-header-inner">{column_title}</div>
        </th>
        '''.format(column_index=index, column_title=column_title)
        visible_header_row.findChild('tr').append(BeautifulSoup(visible_header_column_html, features='html.parser'))

        hidden_header_column_html = '''
        <th class="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted"
            data-column="{column_index}" tabindex="0" scope="col" role="columnheader" aria-disabled="false"
            unselectable="on" aria-sort="none" style="user-select: none;"
            aria-label="Задача: No sort applied, activate to apply an ascending sort">
            <div class="tablesorter-header-inner">{column_title}</div>
        </th>
        '''.format(column_index=index, column_title=column_title)
        hidden_header_row.findChild('tr').append(BeautifulSoup(hidden_header_column_html, features='html.parser'))

    dst_table = BeautifulSoup('''
    <div class="table-wrap">
        <table class="wrapped relative-table confluenceTable tablesorter tablesorter-default stickyTableHeaders"
               style="width: 100%; padding: 0px;" role="grid" resolved="">
    </div>
    ''', features='html.parser')

    dst_table_element = dst_table.find('table')
    dst_table_element.append(visible_header_row)
    dst_table_element.append(hidden_header_row)

    with open(input_html_file_path) as f:
        html_content = f.read()

    src_table_body = BeautifulSoup(html_content, features='html.parser').find(id='issuetable').findChild('tbody')
    dst_table_body = BeautifulSoup('<tbody aria-live="polite" aria-relevant="all"></tbody>', features='html.parser')

    for ticket_element in src_table_body.findChildren('tr', recursive=False):
        # Проект, к которому принадлежит задача
        project = ticket_element.find('td', {'class': 'project'}).text.strip()
        # Ссылка на задачу
        issue_key_href = ticket_element.find('td', {'class': 'issuekey'}).findChild('a')['href']
        issue_key = make_link(
            url=issue_key_href,
            content=ticket_element['data-issuekey']
        )
        # Тема
        summary = ticket_element.find('td', {'class', 'summary'}).text.strip()
        # Приоритет задачи
        priority = ticket_element.find('td', {'class': 'priority'}).text.strip()
        # Статус задачи
        resolution_element = ticket_element.find('td', {'class': 'resolution'})
        try:
            resolution = resolution_element.findChild('em').text.strip()
        except AttributeError:
            resolution = resolution_element.text.strip()
        # Ссылки на скриншоты из задачи
        thumbnails = '\n'.join([
            make_link(url=a['href'], content=a['href'])
            for a in ticket_element.find('td', {'class': 'thumbnail'}).findChildren('a', recursive=False)
        ])
        # Связанные задачи
        issue_links = ticket_element.find('td', {'class': 'issuelinks'}).text.strip()
        # Описание задачи
        description = ticket_element.find('td', {'class': 'description'}).text.strip()

        dst_table_row = BeautifulSoup(f'''
        <tr role="row">
            <td class="confluenceTd">{project}</td>
            <td class="confluenceTd">{issue_key}</td>
            <td class="confluenceTd">{summary}</td>
            <td class="confluenceTd">{priority}</td>
            <td class="confluenceTd">{resolution}</td>
            <td class="confluenceTd">{thumbnails}</td>
            <td class="confluenceTd">{issue_links}</td>
            <td class="confluenceTd">{description}</td>
        </tr>
        ''')

        dst_table_body.findChild('tbody').append(dst_table_row)

    dst_table_element.append(dst_table_body)

    with open(output_html_file_path, mode='w', encoding='utf-8') as f:
        f.write(str(dst_table).replace('`', ''))


if __name__ == '__main__':
    main(
        input_html_file_path=Path('/home/k9173a/dev/PythonPlayground/miscellaneous/confluence/jira.html'),
        output_html_file_path=Path('/home/k9173a/dev/PythonPlayground/miscellaneous/confluence/jira-output.html')
    )
