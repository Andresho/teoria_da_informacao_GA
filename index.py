import argparse, os
import sys 

sys.path.append("./huffman_coding_MMagdys/")

from HuffmanTree import HuffmanTree
from HuffmanCompressor import HuffmanCompressor
from HuffmanDecompressor import HuffmanDecompressor

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

	filePath = "./testFiles/sum"
	outDirectory = "./testFiles/bin/"

	file_directory, file_name_with_extension = os.path.split(filePath)
	filename, file_extension = os.path.splitext(file_name_with_extension)

	huffman = HuffmanCompressor()
	
	encoded_data, encoded_tree = compress_file_splitted(huffman, filePath)

	#codificar encoded_tree com o crc aqui
	crc_encoded_tree = encoded_tree

	huff_bytes = bytearray( huffman.encoded_arr(encoded_data, crc_encoded_tree, filename) )

	with open(outDirectory + filename + ".huffman", "wb") as dest:
			dest.write(huff_bytes)

	print(filename + ".huffman created criado na pasta " +outDirectory)

if __name__ == '__main__':
	main()