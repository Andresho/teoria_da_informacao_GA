#Funcoes modificadas da lib Huffman
import sys 
sys.path.append("./huffman_coding_MMagdys/")
from HuffmanTree import HuffmanTree

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

def decompress_file_with_pathname(huffman, encode_txt, pathname):
		'''
        Funcao modificada do HuffmanDecompressor, para adicionar o caminho
        do arquivo de saidas
        '''

		trailing = encode_txt[0]
		tree_size = encode_txt[1:5]
		tree_size = int.from_bytes(tree_size, byteorder="little")
		tree_bytes = encode_txt[5 : 5+tree_size]

		# File name size
		index = 5+tree_size
		filename_size = int.from_bytes(encode_txt[index:index+1], byteorder="little")
		filename = encode_txt[index+1:index+1+filename_size].decode("UTF-8")
		# print(filename)

		# File extension
		index = index+1+filename_size
		file_exten_size = int.from_bytes(encode_txt[index:index+1], byteorder="little")
		file_exten = encode_txt[index+1:index+1+file_exten_size].decode("UTF-8")

		# Encode Text
		index = index+1+file_exten_size

		txt_size = int.from_bytes(encode_txt[index : index+5], byteorder="little")
		# print(txt_size)
		txt_bytes = encode_txt[index + 5 : index + 5 + txt_size]
		# print(txt_bytes)
		txt_bin = format(int.from_bytes(txt_bytes, byteorder="little"), "b")[:-trailing]

		huffman.get_codes(tree_bytes)
		huffman.plain_text(txt_bin, huffman.root)
		huffman.write_file(pathname, file_exten)

		index = index + 5 + txt_size
		
		if index < len(encode_txt):
			huffman.pln_text = ""
			huffman.decompress_files(encode_txt[index:])


def get_tree_bytes(encode_txt):
    #Trata o cabecalho para retornar apenas os bytes da arvore huffman
    
    trailing = encode_txt[0]
    tree_size = encode_txt[1:5]
    tree_size = int.from_bytes(tree_size, byteorder="little")
    tree_bytes = encode_txt[5: 5+tree_size]
    return tree_bytes