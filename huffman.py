import numpy as np
import queue
from skimage.io import imread


class Node:
    def __init__(self):
        self.prob = None
        self.code = None
        self.data = None
        self.left = None
        self.right = None

    def __lt__(self, other):
        if self.prob < other.prob:
            return 1
        else:
            return 0

    def __ge__(self, other):
        if self.prob > other.prob:
            return 1
        else:
            return 0


def rgb2gray(image):
    gray_img = np.rint(image[:, :, 0] * 0.2989 + image[:, :, 1] * 0.5870 + image[:, :, 2] * 0.1140)
    gray_img = gray_img.astype(int)
    return gray_img


def tree(probabilities_):
    prq = queue.PriorityQueue()
    for color, probability in enumerate(probabilities_):
        leaf = Node()
        leaf.data = color
        leaf.prob = probability
        prq.put(leaf)
    while prq.qsize()>1:
        newnode = Node()
        newnode.left = prq.get()
        newnode.right = prq.get()
        newnode.prob = newnode.left.prob + newnode.right.prob
        prq.put(newnode)
    return prq.get()


def huffman_traversal(rt_node, tmp_arr, f):
    if rt_node.left is not None:
        tmp_arr[huffman_traversal.count] = 1
        huffman_traversal.count += 1
        huffman_traversal(rt_node.left, tmp_arr, f)
        huffman_traversal.count -= 1
    if rt_node.right is not None:
        tmp_arr[huffman_traversal.count] = 0
        huffman_traversal.count += 1
        huffman_traversal(rt_node.right, tmp_arr, f)
        huffman_traversal.count -= 1
    else:
        huffman_traversal.output_bits[rt_node.data] = huffman_traversal.count
        bitstream = ''.join(str(cell) for cell in tmp_arr[1:huffman_traversal.count])
        color = str(rt_node.data)
        wr_str = color + ' ' + bitstream + '\n'
        f.write(wr_str)
    return


img = imread('PSX_20200327_171456.bmp')

gray_img = rgb2gray(img)

hist = np.bincount(gray_img.ravel(), minlength=256)
probabilities = hist/np.sum(hist)

root_node = tree(probabilities)
tmp_array = np.ones([64], dtype=int)
huffman_traversal.output_bits = np.empty(256, dtype=int)
huffman_traversal.count = 0
file = open('codes.txt', 'w')
huffman_traversal(root_node, tmp_array, file)

input_bits = img.shape[0]*img.shape[1]*8
compression = (1-np.sum(huffman_traversal.output_bits*hist)/input_bits)*100
print('Compression is ', compression, ' percent')