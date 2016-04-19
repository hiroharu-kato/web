#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import codecs
import shutil
import subprocess

import yaml
import werkzeug.contrib.atom
import BeautifulSoup

IS_LOCAL = True
DIRECTORY_SRC = '../src'
DIRECTORY_FEED = '/note'
DIRECTORY_HTML = '../html'
TEMPLATE_FILE = 'template.html'
URL_BASE = 'http://hiroharu-kato.com'
PANDOC_OPTIONS = [
    '-f', 'markdown-markdown_in_html_blocks',
    '-t', 'html',
    '--smart',
    '--normalize',
    '--highlight-style=pygments',
    '--email-obfuscation=javascript',
    '--id-prefix=md-',
    '--base-header-level=2',
]

# set root directory
if IS_LOCAL:
    root = os.path.abspath(DIRECTORY_HTML)
else:
    root = ''

# get snipets
snipets = {}
for filename in glob.glob('%s/snipets/*.html' % DIRECTORY_SRC):
    snipet = open(filename).read()
    name = os.path.basename(filename)[:-5]
    snipets[name] = snipet


def convert_directory(dir_from, dir_to):
    # make directory
    if not os.path.exists(dir_to):
        os.mkdir(dir_to)

    for filename_from in glob.glob('%s/*' % dir_from):
        directory = os.path.dirname(filename_from)
        basename = os.path.basename(filename_from)
        if os.path.isdir(filename_from):
            filename_to = '%s/%s' % (dir_to, basename)
            convert_directory(filename_from, filename_to)
        elif filename_from.endswith('.md'):
            filename_to = '%s/%s.html' % (dir_to, basename[:-3])
            print 'processing', filename_from, filename_to

            # set root and snipts
            html = open(filename_from).read()
            html = html.replace('$root$', root)
            for k, v in snipets.items():
                html = html.replace('$%s$' % k, v)
            open(filename_to, 'w').write(html)

            dir_ = directory
            while True:
                template = '%s/%s' % (dir_, TEMPLATE_FILE)
                if os.path.exists(template):
                    break
                else:
                    dir_ = os.path.dirname(dir_)

            pandoc = ['pandoc', '-o', filename_to]
            pandoc += ['--template=%s' % template]
            pandoc += ['--variable=root:%s' % root]
            pandoc += PANDOC_OPTIONS
            pandoc += [filename_to]
            p = subprocess.Popen(pandoc)
            p.wait()


def make_feed():
    title = get_title()
    feed = werkzeug.contrib.atom.AtomFeed(title, url='%s/feed' % URL_BASE)
    pages = glob.glob('%s/%s/*.md' % (DIRECTORY_SRC, DIRECTORY_FEED))
    pages = sorted(pages)[::-1]
    for page in pages:
        if 'index' in page:
            continue
        title = None
        state = 'head'
        str_yaml = ''
        str_md = ''
        for line in codecs.open(page, 'r', 'utf-8').readlines():
            if line.startswith('---'):
                if state == 'head':
                    state = 'yaml'
                elif state == 'yaml':
                    state = 'md'
                continue
            if state == 'yaml':
                str_yaml += line
            elif state == 'md':
                str_md += line
        str_yaml = yaml.load(str_yaml)
        title = str_yaml['title'].replace('\\', '')
        date = str_yaml['date']
        content = str_md.strip().replace('\n', '<br>')
        content = content.replace('\\', '')[:140] + '...'
        url_page = '%s%s/%s' % (
            URL_BASE, DIRECTORY_FEED,
            os.path.basename(page).replace('md', 'html'),
        )
        feed.add(
            title, content, content_type='html', updated=date,
            id=os.path.basename(page), url=url_page,
        )
    fp = codecs.open('%s/feed.xml' % DIRECTORY_HTML, 'w', 'utf-8')
    fp.write(feed.get_response().response[0].decode('utf-8'))
    fp.close()


def get_title():
    bs = BeautifulSoup.BeautifulSoup(
        open('%s/%s' % (DIRECTORY_SRC, TEMPLATE_FILE)))
    return bs('h1')[0].text

shutil.rmtree(DIRECTORY_HTML)
shutil.copytree('%s/assets' % DIRECTORY_SRC, '%s/assets' % DIRECTORY_HTML)
convert_directory(DIRECTORY_SRC, DIRECTORY_HTML)
make_feed()
