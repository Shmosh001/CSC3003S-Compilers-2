	.text
	.file	"<string>"
	.section	.rodata.cst4,"aM",@progbits,4
	.align	4
.LCPI0_0:
	.long	1079613850
	.text
	.globl	main
	.align	16, 0x90
	.type	main,@function
main:
	.cfi_startproc
	subq	$16, %rsp
.Ltmp0:
	.cfi_def_cfa_offset 24
	movl	$1067030938, 12(%rsp)
	movl	$1079613850, 8(%rsp)
	movss	12(%rsp), %xmm0
	movabsq	$.LCPI0_0, %rax
	mulss	(%rax), %xmm0
	movss	%xmm0, 4(%rsp)
	addq	$16, %rsp
	retq
.Ltmp1:
	.size	main, .Ltmp1-main
	.cfi_endproc


	.section	".note.GNU-stack","",@progbits

