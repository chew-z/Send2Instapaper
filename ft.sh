#!/usr/bin/env zsh
cd /Users/rrj/Documents/Python/utils/resources/_tmp
today=$(date +"%d-%m-%Y")
# This works OK
# This works OK
echo '<dc:creator>get4instapaper.py</dc:creator>' >| metadata.xml
echo '<dc:date opf:event="publication">' $today '</dc:date>' >> metadata.xml
echo '<dc:date>' $today '</dc:date>' >> metadata.xml
echo '<dc:language>en-US</dc:language>' >> metadata.xml
echo '<dc:rights>© 2017 Free as in "free coffee"</dc:rights>' >> metadata.xml
echo '<dc:source>Instapaper.com</dc:source>' >> metadata.xml
echo '<dc:publisher>Instapaper</dc:publisher>' >> metadata.xml
echo '<dc:title>Instapaper</dc:title>' >> metadata.xml
# I think that gets ignored when we use metadata.xml
echo '<!DOCTYPE html>\n<html>\n<head>\n<meta charset="UTF-8">' >| title_page.htm
echo '<title>Instapaper</title>' >> title_page.htm
echo '<subtitle>edition' $today '</subtitle>' >> title_page.htm
echo '<date>' $today '</date>' >> title_page.htm
echo '<author>Instapaper.com</author>' >> title_page.htm
echo '</head>\n<body>' >> title_page.htm
echo '<section epub:type="titlepage">' >> title_page.htm
echo '<h1 class="title">Instapaper</h1>' >> title_page.htm
echo '<p class="subtitle">edition: ' $today '</p>' >> title_page.htm
echo '<h2 class="author">instapaper.com</h2>' >> title_page.htm
echo '<h3 class="date">' $today '</h3>' >> title_page.htm
echo '</section>' >> title_page.htm
echo '</body></html>' >> title_page.htm
#
pandoc --toc --toc-depth=2 --smart --self-contained -r html -w epub3 -o "Instapaper $today.epub" *.html  title_page.htm \
    --epub-stylesheet="iBooks.css"      \
    --epub-metadata=metadata.xml
    --epub-cover-image="Stadsbiblioteket_.jpg" \



