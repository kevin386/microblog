# -*- coding: utf-8 -*-
import os
import sys
# if sys.platform == 'wn32':
#     pybabel = 'flask\\Scripts\\pybabel'
# else:
#     pybabel = 'flask/bin/pybabel'
pybabel = "pybabel"
if len(sys.argv) != 2:
    print "usage: python tr_init.py <language-code>\nNote: Simplified-chinese language code must be \"zh_Hans_CN\""
    sys.exit(1)
os.system(pybabel + ' extract -F babel.cfg -k lazy_gettext -o messages.pot app')
os.system(pybabel + ' init -i messages.pot -d app/translations -l ' + sys.argv[1])
os.unlink('messages.pot')