import os
import sys
import crcmod

sys.path.append("./huffman_coding_MMagdys/")

from HuffmanDecompressor import HuffmanDecompressor

from adapter import get_tree_bytes, decompress_file_with_pathname

def main():
    file_path = "" # ex: "./testFiles/bin/alice29.huffmanCRC"
    out_file = "" # ex: "./testFiles/decompressed/alice29.txt"
    
    file_size = os.path.getsize(file_path)
    huffman = HuffmanDecompressor()

    with open(file_path, "rb") as decomp:
        #Le o arquivo
        compressed_file = bytearray(decomp.read())
        
        #Pega o ultimo bit do arquivo, que é o crc criado na compressao
        crc_file = compressed_file.pop( file_size-1 )
        
        tree_bytes = get_tree_bytes( compressed_file )
        
        #Recria o crc a partir do tree_bytes
        crc8_func = crcmod.predefined.mkCrcFun('crc-8')
        crc_from_tree = crc8_func( tree_bytes )
        
        #Determina se existe erro na arvore huffman
        if crc_file != crc_from_tree:
            print( "Houve um erro no envio de dados. Por Favor retransmita o arquivo" )
            return
        
        decompress_file_with_pathname(huffman, compressed_file, out_file )
        
        print( "file decompressed at: " + out_file)
        
    decomp.close()
    
if __name__ == '__main__':
	main()
