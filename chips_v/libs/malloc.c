//The heap is implemented as a global array
extern const int heap_size;
extern int heap[];

//helper functions allocate array elements
//in blocks
static int _malloc(unsigned size){
    int block = 0;
    int block_size;
    int allocated;

    if(size == 0) return 0;

    //if uninitialised, initialise heap
    if(!heap[0]) heap[0]=heap_size-1;

    //search for an unallocated block
    while(1){

        //If we have run out of blocks to allocate return null
        if(block >= heap_size) return 0;

        //the first location in each block contains the size of the block
        //and a flag to say whether the block is allocated.
        block_size = heap[block] & 0xffff;
        allocated = heap[block] & 0x80000;

        //If the block is big enough and not allocated then allocate this block
        if(block_size >= size && !allocated) break;

        //Otherwise go to the start of the next block
        block = block + block_size + 1;
    }

    //write the size and allocated flag of the block
    heap[block] = 0x80000 | size;

    //if the block was larger than needed, the spare space in the block can
    //be split the second half is an unallocated block
    if(block_size > size){
        heap[block + size + 1] = block_size - size - 1;
    }

    //return pointer to the second location in the block
    return block + 1;
}

//Defragment the heap, joining together contiguous blocks
static void _clean(){
    int block = 0, next_block;
    int block_size, next_block_size;
    int allocated, next_allocated;

    while(1){
        if(block >= heap_size) return;
        block_size = heap[block] & 0xffff;
        allocated = heap[block] & 0x80000;
	    next_block = block + block_size + 1;
        if(!allocated){
            while(1){
                if(next_block >= heap_size) return;
                next_block_size = heap[next_block] & 0xffff;
                next_allocated = heap[next_block] & 0x80000;
                if(!next_allocated){
                    block_size = block_size + next_block_size + 1;
                    heap[block] = block_size;
                    next_block += next_block_size + 1;
                } else {
                    break;
                }
            }
        }
        block = next_block;
    }
}

// Deallocate the block
static void _free(int block){
    //clear the allocated flag
    heap[block - 1] &= 0xffff;

    //merge unallocated blocks
    _clean();
}

void* malloc(unsigned size){

    /* round up to the next 4 bytes */
    int size_in_words = (size + 3)/4;
    int element = _malloc(size_in_words);

    return (void *) &heap[element];
}

void free(void* block){
    int element = (int*)block - (int*)&heap;
    _free(element);
}
