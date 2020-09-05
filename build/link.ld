OUTPUT_ARCH( "riscv" )
ENTRY( _start )

MEMORY
{
  ROM   (rwx) : ORIGIN = 0x00000000, LENGTH = 1K
  RAM   (rwx) : ORIGIN = 0x00000400, LENGTH = 1M
}

SECTIONS
{
  .text : {
	  	. = 0x000000;
		*(.init);
		*(.text);
		. = ALIGN(4);
		end = .;
  } >ROM
  .data : {
	  	. = 0x000000;
		*(.rodata);
		end = .;
  } >RAM
}
