"""
###############################################################################

  Copyright (c) 2020  Baidu, Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
################################################################################
"""

# -*- coding: UTF-8 -*-

import time
from io import open
from imp import ahocorasick_dict
from imp import tried_dict
from imp import tried_dar
from imp import prefix_dict


def test_eval(imp, data_name):
    try:
      ac = imp.Ahocorasick()
    except:
      ac = imp.TriedTree()
    word_file = "data/%s_words.txt"%data_name
    data_file = "data/%s_data.txt"%data_name
    words = [word.strip() for word in open(word_file, 'r', encoding='utf8')]

    start = time.time()
    for word in words:
      ac.add_word(word)
    end_add = time.time()
    print("%s %s add_word time: %f"%(imp.__name__, data_name, end_add-start))
    ac.make()
    end = time.time()
    print("%s %s load time: %f"%(imp.__name__, data_name, end-start))

    start = time.time()
    for line in open(data_file, 'r', encoding='utf8'):
      ac.search(line.strip())
    end = time.time()

    print("%s %s search time: %f"%(imp.__name__, data_name, end-start))

if __name__ == "__main__":
  test_eval(tried_dict, 'pku')
  test_eval(tried_dict, 'as')
  test_eval(tried_dict, 'jieba')

  # test_eval(ahocorasick_dict, 'pku')
  # test_eval(ahocorasick_dict, 'as')
  # test_eval(ahocorasick_dict, 'jieba')

  test_eval(prefix_dict, 'pku')
  test_eval(prefix_dict, 'as')
  test_eval(prefix_dict, 'jieba')

  # test_eval(tried_dar, 'pku')
  # test_eval(tried_dar, 'as')

