import os
import sys 
import crcmod

sys.path.append("./huffman_coding_MMagdys/")

from HuffmanCompressor import HuffmanCompressor

from adapter import compress_file_splitted

def main():
	filePath = "" 		# ex "./testFiles/sum"
	outDirectory = "" 	# ex "./testFiles/bin/"

	file_directory, file_name_with_extension = os.path.split(filePath)
	filename, file_extension = os.path.splitext(file_name_with_extension)

	huffman = HuffmanCompressor()


	#Comprime o arquivo, e retorna o os dados e a arvore compressos em separado
	encoded_data, encoded_tree = compress_file_splitted(huffman, filePath)

	#Junta os elementos e cria um cabecalho
	huff_bytes = bytearray( huffman.encoded_arr(encoded_data, encoded_tree, filename) )

	#Determina o crc da arvore huffman
	crc8_func = crcmod.predefined.mkCrcFun('crc-8')
	crc = crc8_func( encoded_tree )

	crc_byte = crc.to_bytes(1, byteorder="little")

	with open(outDirectory + filename + ".huffmanCRC", "wb") as dest:
			#Escreve a codificacao huffman
   			dest.write(huff_bytes)
			#Escreve o crc como ultimo byte
			dest.write(crc_byte)

	print(filename + ".huffman created criado na pasta " +outDirectory)

	dest.close()

if __name__ == '__main__':
	main()
