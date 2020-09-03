OUTPUT_ARCH( "riscv" )
ENTRY( _start )

MEMORY
{
  RAM   (rwx) : ORIGIN = 0x00000000, LENGTH = 1M
}

SECTIONS
{
  .text : {
	  	. = 0x000000;
		*(.init);
		*(.text);
		. = ALIGN(4);
		end = .;
  } >RAM
}
