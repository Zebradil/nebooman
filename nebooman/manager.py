# vim:fileencoding=utf-8:noet

import urllib.request

from bs4 import BeautifulSoup


class Manager:
    header = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks Menu</H1>

"""
    bookmark_attrs = [
        'href',
        'add_date',
        'last_visit',
        'last_modified',
        'icon',
    ]

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.soup = None
        self.bookmarks = None

    def read_bookmarks_file(self, file_handler):
        self.soup = BeautifulSoup(file_handler, 'html5lib')
        self.bookmarks = self.html_to_bookmarks(self.soup.body)

    def write_bookmarks_file(self, file_handler):
        file_handler.write(self.header + self.bookmarks_to_html(self.bookmarks))

    def cleanup(self):
        self.remove_duplicate_links(self.bookmarks)
        self.merge_folders(self.bookmarks)
        self.remove_empty_folders(self.bookmarks)

    def merge_folders(self, bookmarks, folders={}, parent_name=''):
        for obj in bookmarks:
            if 'children' in obj:
                name = parent_name + obj['title']
                self.merge_folders(obj['children'], folders, name + '→')
                if name in folders:
                    if self.verbose:
                        print('Merge folder: ' + name)
                    folders[name]['children'] += obj['children']
                    bookmarks.remove(obj)
                else:
                    folders[name] = obj

    def remove_empty_folders(self, bookmarks, folders={}, parent_name=''):
        for obj in bookmarks:
            if 'children' in obj:
                name = parent_name + obj['title']
                self.remove_empty_folders(obj['children'], folders, name + '→')
                if not obj['children']:
                    if self.verbose:
                        print('Remove folder: ' + name)
                    bookmarks.remove(obj)

    def remove_duplicate_links(self, bookmarks, links=[]):
        for obj in bookmarks:
            if 'href' in obj:
                if obj['href'] in links:
                    if self.verbose:
                        print('Remove link: {} [{}]'.format(obj['title'], obj['href']))
                    bookmarks.remove(obj)
                else:
                    links.append(obj['href'])
            elif 'children' in obj:
                self.remove_duplicate_links(obj['children'], links)

    def fetch_titles(self, bookmarks, no_title='NO_TITLE'):
        for obj in bookmarks:
            if 'href' in obj and obj['title'] == no_title:
                if self.verbose:
                    print('Fetching title for: ' + obj['href'])
                title = self.fetch_title(obj['href'])
                if title is None:
                    print('\tfailed')
                else:
                    print('\tnew title: ' + title)
                    obj['title'] = title
            elif 'children' in obj:
                self.fetch_titles(obj['children'])

    @staticmethod
    def fetch_title(url):
        try:
            with urllib.request.urlopen(url) as response:
                html = str(response.read())
                start = html.find('<title>')
                if start == -1:
                    return None
                end = html.find('</title>')
                # 7 == len('<title>')
                return html[start + 7:end]
        except:
            return None

    def html_to_bookmarks(self, bookmarks_container):
        bookmarks = []
        for element in bookmarks_container.children:
            if not element.name or element.name in ['h1', 'p']:
                continue
            if element.name == 'dt':
                folder_title = element.find(folded=True, recursive=False)
                if folder_title:
                    folder = element.find('dl', recursive=False)
                    if folder:
                        bookmarks.append({
                            'title': xstr(folder_title.string),
                            'children': self.html_to_bookmarks(folder)
                        })
                    continue
                bookmark = element.find('a', recursive=False)
                if bookmark:
                    bookmarks.append({
                        'href': bookmark['href'],
                        'title': xstr(bookmark.string)
                    })
                    continue
            print('Unsupported element: ', element.name)
        return bookmarks

    def bookmarks_to_html(self, bookmarks, level=0):
        html = ''
        for obj in bookmarks:
            if 'href' in obj:
                attrs = ''
                for attr in self.bookmark_attrs:
                    if attr in obj:
                        attrs += ' ' + attr.upper() + '="{}"'.format(obj[attr])
                html += pad(level) + '<DT><A' + attrs + '>' + obj['title'] + '</A>\n'
                continue
            html += pad(level) + '<DT><H3>' + obj['title'] + '</H3>\n'
            html += pad(level) + '<DL><p>\n'
            html += self.bookmarks_to_html(obj['children'], level + 1)
            html += pad(level) + '</DL><p>\n'
        return html


def pad(level):
    return ' ' * level * 4


def xstr(something):
    return '' if something is None else str(something)
