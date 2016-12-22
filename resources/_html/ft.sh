#!/usr/bin/env zsh

today=$(date +"%d-%m-%Y")
# This works OK
# This works OK
echo '<dc:creator>ft2text.py -> ft.sh -> pandoc</dc:creator>' >| metadata.xml
echo '<dc:date opf:event="publication">' $today '</dc:date>' >> metadata.xml
echo '<dc:date>' $today '</dc:date>' >> metadata.xml
echo '<dc:language>en-GB</dc:language>' >> metadata.xml
echo '<dc:rights>© 2016 Free as in "free coffee"</dc:rights>' >> metadata.xml
echo '<dc:source>ft.com</dc:source>' >> metadata.xml
echo '<dc:publisher>Financial Times</dc:publisher>' >> metadata.xml
echo '<dc:title>Financial Times</dc:title>' >> metadata.xml
# I think that gets ignored when we use metadata.xml
echo '<!DOCTYPE html>\n<html>\n<head>\n<meta charset="UTF-8">' >| title_page.htm
echo '<title>Financial Times</title>' >> title_page.htm
# # echo '<subtitle>edition' $today '</subtitle>' >> title_page.htm
# # echo '<date>' $today '</date>' >> title_page.htm
echo '<author>ft.com</author>' >> title_page.htm
echo '</head>\n<body>' >> title_page.htm
echo '<section epub:type="titlepage">' >> title_page.htm
echo '<h1 class="title">Financial Times</h1>' >> title_page.htm
echo '<p class="subtitle">edition: ' $today '</p>' >> title_page.htm
echo '<p class="author">ft.com</p>' >> title_page.htm
echo '<p class="date">' $today '</p>' >> title_page.htm
echo '</section>' >> title_page.htm
echo '</body></html>' >> title_page.htm
#
pandoc --smart --self-contained -r html -w epub3 -o "../FT $today.epub"   *.html  title_page.htm  \
    --epub-cover-image="../_img/FT.jpg"     \
    --epub-stylesheet="../_css/ft.css"      \
    --epub-metadata=metadata.xml  \
    --toc                         \
    --toc-depth=1                 \
    --variable=title:"Financial Times" \
#    --variable=subtitle:"edition $today" \


