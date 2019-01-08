import re

author =  '<div class="copyright-area">原文出处： <a target="_blank" href="https://www.cnblogs.com/dotey/p/10220520.html">宝玉（@宝玉XP）</a>\xa0\xa0\xa0</div>'
author = '<div class="copyright-area">本文由 <a href="http://blog.jobbole.com">伯乐在线</a> - <a href="http://www.jobbole.com/members/aoi">伯小乐</a> 翻译。未经许可，禁止转载！<br>英文出处：<a target="_blank" href="https://blog.usejournal.com/rethinking-how-we-interview-in-microsofts-developer-division-8f404cfd075a">John Montgomery</a>。欢迎加入<a target="_blank" href="https://github.com/jobbole/translation-project">翻译组</a>。</div>'

match_re = re.match(".*?出处：.*?>(.*?)<",author)
print(match_re.group(1))
