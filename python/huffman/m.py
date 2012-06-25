#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Queue

from collections import defaultdict
from pprint import pprint as pp

def huff(seq):
    ## we expose the input characters are in basic char set
    freq = defaultdict(int)
    ## get the frequncy data
    [freq.update({k:freq[k]+1}) for k in seq]
    #pp(freq)

    ## build a priority queue and prepare the data
    prior_queue = Queue.PriorityQueue()
    [prior_queue.put((v, k)) for (k,v) in freq.iteritems()]

    ## loop until the final one has been generated
    while prior_queue.qsize() > 1:
        item1, item2 = prior_queue.get(), prior_queue.get()
        #print 'item1', item1, 'item2', item2
        left_data = item1[1] if item1[0] > item2[0] else item2[1]
        right_data = item2[1] if item1[0] > item2[0] else item1[1]
        new_item = item1[0] + item2[0], {'left': left_data, 'right': right_data}

        prior_queue.put(new_item)

    final_item = prior_queue.get()

    symbol_mapping = {}
    build_mapping('', symbol_mapping, final_item[1])

    pp(symbol_mapping)

    result_str = huff_encode(seq, symbol_mapping)
    normal_str = ''.join([bin(ord(char))[2:] for char in seq])

    decoded_str = huff_decode(result_str, final_item[1])
    assert decoded_str == seq, 'decoding error'

    print 'encoded length', len(result_str)
    print 'origin length', len(normal_str)
    print 'compression rat: %.2f%%' % (float(len(result_str))/float(len(normal_str))*100)

def build_mapping(prefix, mapping, node):
    ## left = 0, right = 1
    left, right = node['left'], node['right']
    if isinstance(left, dict):
        build_mapping(prefix+'0', mapping, left)
    else:
        mapping[left] = prefix+'0'

    if isinstance(right, dict):
        build_mapping(prefix+'1', mapping, right)
    else:
        mapping[right] = prefix+'1'


def huff_encode(seq, mapping):
    return ''.join([mapping[char] for char in seq])

def huff_decode(seq_encoded, final_node):
    source = iter(seq_encoded)
    result = []
    path = final_node

    while 1:
        try:
            bit = source.next()
            direct = 'left' if bit == '0' else 'right'
            path_node = path[direct]
            if not isinstance(path_node, dict):
                ## match
                result.append(path_node)
                path = final_node
            else:
                path = path_node

        except StopIteration:
            return ''.join(result)


test_text = """
You’ve probably heard about David Huffman and his popular compression algorithm. If you didn’t, you’ll find that info on the Internet. I will not bore you with history or math lessons in this article. I’m going to try to show you a practical example of this algorithm applied to a character string. This application will only generate console output representing the code values for the symbols inputted and generate the original symbols from a given code.

The source code attached to this article will show you how Huffman Coding works so you will get a basic understanding of it. This is for the people who have difficulty understanding the mathematics of it. In a future article (I hope) we’ll be talking about how to apply this to any files to produce their compressed format. (A simple file archiver like WinZip or WinRAR.)

The idea behind Huffman coding is based upon the frequency of a symbol in a sequence. The symbol that is the most frequent in that sequence gets a new code that is very small, the least frequent symbol will get a code that is very long, so that when we’ll translate the input we want to encode the most frequent symbols will take less space than they used to and the least frequent symbols will take more space but because they’re less frequent it won’t matter that much. For this application I chose the symbol to be 8 bits long so that the symbol will be a character (char).

We could just as easily have chosen the symbol to be 16 bits long, so we could have grouped 2 characters together as a symbol or 10 bits or 20 etc. Depending on the input we expect to have, we’ll chose the size of the symbol and the way we use it. For example, if I expect to encode raw video files, I’ll chose the symbol to be the size of a pixel. Keep in mind that when increasing or decreasing the size of the symbol, it will affect the size of the code for each symbol because the bigger the size, the more symbols you can have of that size. There are less ways to write the ones and zeroes on 8 bits than there are on 16 bits. You’ll want to adjust the size of the symbol depending on how the ones and zeroes are likely to repeat themselves in a sequence.

For this algorithm you need to have a basic understanding of binary tree data structure and the priority queue data structure. In the source code we’ll actually use the priority queue code available in a previous article.

Let’s say we have the string “beep boop beer!” which in his actual form, occupies 1 byte of memory for each character. That means that in total, it occupies 15*8 = 120 bits of memory. Through encoding, the string will occupy 40 bits. (Theoretically, in this application we’ll output to the console a string of 40 char elements of 0 and 1 representing the encoded version of the string in bits. For this to occupy 40 bits we need to convert that string directly into bits using logical bit operations which we’ll not discuss now.)

To better understand this example, we’ll going to apply it on an example. The string “beep boop beer!” is a very good example to illustrate this. In order to obtain the code for each element depending on it’s frequency we’ll need to build a binary tree such that each leaf of the tree will contain a symbol (a character from the string). The tree will be build from the leafs to the root, meaning that the elements of least frequency will be farther from the root than the elements that are more frequent. You’ll see soon why we chose to do this.

To build the tree this way we’ll use a priority queue with a slight modification, that the element with the least priority is the most important. Meaning that the elements that are the least frequent will be the first ones we get from the queue. We need to do this so we can build the tree from the leaves to the root.
"""

##test_text = 'hello, world'
huff(test_text)

