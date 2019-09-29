import os
import sys
import crcmod

sys.path.append("./huffman_coding_MMagdys/")

from HuffmanDecompressor import HuffmanDecompressor

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
    trailing = encode_txt[0]
    tree_size = encode_txt[1:5]
    tree_size = int.from_bytes(tree_size, byteorder="little")
    tree_bytes = encode_txt[5: 5+tree_size]
    return tree_bytes

def main():
    file_path = "./testFiles/bin/alice29.huffmanCRC"
    out_file = "./testFiles/decompressed/alice29.txt"
    file_size = os.path.getsize(file_path)

    huffman = HuffmanDecompressor()

    print("teste")

    # int.from_bytes( bytes, byteorder, *, signed=False )

    with open(file_path, "rb") as decomp:
        compressed_file = bytearray(decomp.read())
        crc_file = compressed_file.pop( file_size-1 )
        
        tree_bytes = get_tree_bytes( compressed_file )
        
        crc8_func = crcmod.predefined.mkCrcFun('crc-8')
        crc_from_tree = crc8_func( tree_bytes )
        
        if crc_file != crc_from_tree:
            print( "Houve um erro no envio de dados. Por Favor retransmita o arquivo" )
            return
        
        decompress_file_with_pathname(huffman, compressed_file, out_file )
        
    decomp.close()
    
if __name__ == '__main__':
	main()
