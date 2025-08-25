from collections import Counter
import heapq
import struct
from dataclasses import dataclass

@dataclass
class Node:
    freq:int
    byte:int|None
    left:'Node|None'
    right:'Node|None'

def build_freq_table(data: bytes):
    cnt=Counter(data)
    lista_bytes=[0]*256
    for i in range(0,256):
        lista_bytes[i]=cnt.get(i,0)
    assert len(lista_bytes)==256, 'La tabella deve avere 256 voci'
    assert sum(lista_bytes)==len(data), 'Somma frequenze != numero di byte'

    return lista_bytes
def build_huffman_tree(freqs: list[int]):
    heap=[]
    tie_breaker=0
    for i in range(0,256):
        if freqs[i]>0:
            node=Node(freq=freqs[i], byte=i, left=None, right=None)
            heapq.heappush(heap, (freqs[i],tie_breaker,node))
            tie_breaker+=1
    if heap==[]:
        return None
    if len(heap)==1:
        return heap[0][2]
    while len(heap)>1:
        freq1,_tie_breaker1,left=heapq.heappop(heap)
        freq2,_tie_breaker2,right=heapq.heappop(heap)
        freq_new=freq1+freq2
        new_node=Node(freq=freq_new, byte=None, left=left, right=right)
        heapq.heappush(heap,(freq_new, tie_breaker,new_node))
        tie_breaker+=1
    return heap[0][2]

def build_code_table(root):
    if root is None:
        return {}
    codes={}
    def visit(node,prefix):
        if node.byte is not None:
            codes[node.byte]=prefix or '0'
        else:
            if node.left:
                visit(node.left, prefix+'0')
            if node.right:
                visit(node.right, prefix+'1')
    visit(root,'')             
    return codes                   

def encode_bytes(data: bytes, codes: dict[int,str]):
    buffer=0
    bits=0
    out=bytearray()
    for b in data:
        code=codes[b]
        for c in code:
            if c == '0': 
                bit = 0; 
            else: 
                bit = 1   
            buffer = (buffer << 1) | bit
            bits+=1
            if bits==8:
                out.append(buffer & 0xFF)
                buffer=0
                bits=0
    bit_length=sum(len(codes[b]) for b in data)
    if bits > 0:
        buffer=buffer<<(8-bits)
        out.append(buffer & 0xFF)
    return bytes(out),bit_length  
      
def serialize(freqs: list[int], original_size: int, bit_length: int, payload: bytes):
    assert len(freqs)==256
    assert sum(freqs)==original_size
    assert len(payload)==(bit_length+7)//8

    buf=bytearray()
    for i in range(0,256):
        buf.extend(struct.pack('<I', freqs[i]))
    buf.extend(struct.pack('<I', original_size))
    buf.extend(struct.pack('<I', bit_length))
    buf.extend(payload)

    return bytes(buf)    
     
def compress_bytes(data: bytes):
    freqs=build_freq_table(data)
    root=build_huffman_tree(freqs)
    if root is None:
        payload=b''
        bit_length=0
    else:    
        codes=build_code_table(root)
        payload, bit_length=encode_bytes(data,codes)
    blob=serialize(freqs,len(data),bit_length,payload)
    report={
        "original_size": len(data),
        "compressed_size": len(blob),
        "bit_length": bit_length
    }  

    return blob,report  