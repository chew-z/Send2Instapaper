#!/usr/bin/env zsh

today=$(date +"%d-%m-%Y")
# This works OK
# echo '<dc:creator>ft2text.py -> ft.sh -> pandoc</dc:creator>' >| metadata.xml
# echo '<dc:date opf:event="publication">' $today '</dc:date>' >> meta/data.xml
# echo '<dc:date>' $today '</dc:date>' >> meta/data.xml
# echo '<dc:language>en-GB</dc:language>' >> metadata.xml
# echo '<dc:rights>© 2016 Free as in "free coffee"</dc:rights>' >> metadata.xml
# echo '<dc:source>ft.com</dc:source>' >> metadata.xml
# echo '<dc:publisher>Financial Times</dc:publisher>' >> metadata.xml
# echo '<dc:title>Financial Times</dc:title>' >> metadata.xml
# I think that YAML gets ignored when we use metadata.xml
echo '---' >| metadata.yaml
echo 'title:' >> metadata.yaml
echo '-\ttype: main' >> metadata.yaml
echo '\ttext: Financial Times' >> metadata.yaml
# echo '-\ttype: subtitle' >> metadata.yaml
# echo '\ttext: Chrome to iBooks' >> metadata.yaml
echo '-\ttype: short' >> metadata.yaml
echo '\ttext: FT' >> metadata.yaml
echo '-\ttype: edition' >> metadata.yaml
echo '\ttext: International Edition'  >> metadata.yaml
echo 'lang: en-GB' >> metadata.yaml
echo 'publisher:  ft.com' >> metadata.yaml
echo 'format: epub' >> metadata.yaml
echo 'description: ' >> metadata.yaml
# echo 'cover-image: FT.jpg' >> metadata.yaml
# echo 'stylesheet: iBooks.css' >> metadata.yaml
echo 'creator: ft2text.py -> ft.sh' >> metadata.yaml
echo 'date: ' $today >> metadata.yaml
echo '...' >> metadata.yaml 
# echo '![FT](FT.jpg)' >> metadata.yaml 
#
pandoc --smart --self-contained -r markdown -w epub3 *.md metadata.yaml -o "FT $today.epub" \
    --toc --toc-depth=1           \
    --epub-chapter-level=1        \
    --epub-cover-image=FT.jpg     \
    --epub-stylesheet=ft.css      
#    --variable=title:"Financial Times" \
#    --variable=subtitle:"edition $today" \
#    --variable=creator:ft2text.py  \
#    --epub-metadata=metadata.xml





