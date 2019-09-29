import argparse, os
import sys 
from textwrap import wrap
import crcmod

sys.path.append("./huffman_coding_MMagdys/")

from HuffmanTree import HuffmanTree
from HuffmanCompressor import HuffmanCompressor
from HuffmanDecompressor import HuffmanDecompressor

from BWT import bw_transform
from LZW import LZW_encode

def compress_file_splitted(compressor, filename):

	'''
	Funcao modificada do HuffmanCompressor, para retornar os
	bytes dos dados e da arvore em separado
	'''

	with open(filename, "rb") as src:

		txt = src.read()

		tree = HuffmanTree()
		codes , compressor.encoded_tree = tree.huffman_coding(txt)
		# print(codes)
		compressor.get_encoded_txt(txt, codes)

	src.close()

	return compressor.encoded_txt, compressor.encoded_tree

def main():

	filePath = "./testFiles/alice29.txt"
	outDirectory = "./testFiles/bin/"

	file_directory, file_name_with_extension = os.path.split(filePath)
	filename, file_extension = os.path.splitext(file_name_with_extension)

	huffman = HuffmanCompressor()

	encoded_data, encoded_tree = compress_file_splitted(huffman, filePath)

	huff_bytes = bytearray( huffman.encoded_arr(encoded_data, encoded_tree, filename) )

	crc8_func = crcmod.predefined.mkCrcFun('crc-8')
	crc = crc8_func( encoded_tree )

	print(crc)

	c = crc.to_bytes(1, byteorder="little")

	print(c)
 
	cd = int.from_bytes( c, byteorder="little" )
 
	print(cd)

	with open(outDirectory + filename + ".huffmanCRC", "wb") as dest:
			dest.write(huff_bytes)
			dest.write(c)

	print(filename + ".huffman created criado na pasta " +outDirectory)

	dest.close()

if __name__ == '__main__':
	main()