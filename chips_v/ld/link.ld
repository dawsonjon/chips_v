OUTPUT_ARCH( "riscv" )
ENTRY( _start )

MEMORY
{
  RAM   (rwx) : ORIGIN = 0x00000000, LENGTH = 16K
}

SECTIONS
{
  .text : {
	  	. = 0x000000;
		*(.init);
		*(.text);
		. = ALIGN(4);
		*(.rodata);
		*(.sdata);
		*(.bss);
		_end = .;
  } >RAM
}
