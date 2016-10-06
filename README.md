Netscape Bookmark Manager
===================

[![license](https://img.shields.io/github/license/kafene/netscape-bookmark-parser.svg?style=flat-square)](https://opensource.org/licenses/MIT)

Netscape Bookmark Manager is a command line utility that helps you to keep your bookmarks in order.

For now it has only one option: `clean`. It will remove duplicate links, merge folders with the same name and remove
empty folders after that. There is support only for `href` attribute.

It is tested with Safari only.

Requirements
------------

Netscape Bookmark Manager requires python3 and [BeautifulSoup][1] package.

Installation
------------

Installing can be done with pip:

```txt
pip install nebooman
```

How to use
-------

First of all export your bookmarks as html-file. It should has [Netscape bookmark file format][4]

Then just run `nebooman` command:

```
nebooman clean path/to/your/bookmarks.html -o procesed_bookmarks.html
```

TODO
----
- Fetch titles
- Remove dead links
- Sort bookmarks and folders
- Support for other attributes (
        `add_date`,
        `last_visit`,
        `last_modified`,
        `icon`
)

License
-------

Licensed under [the MIT License][3].

By [German Lashevich][2].

[1]: https://pypi.python.org/pypi/beautifulsoup4
[2]: https://github.com/zebradil
[3]: https://github.com/zebradil/nebooman/blob/master/LICENSE
[4]: https://msdn.microsoft.com/en-us/library/aa753582(v=vs.85).aspx
