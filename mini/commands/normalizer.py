import re


def normalize(cmd:str)->str:
	cmd=cmd.lower()
	cmd=re.sub(r"[^\w\s.]","",cmd)
	filler_words=["hey","mini","can you","please"," do ","i want to","you","now"," i "," me ","good","think","this","that",
	"one thing","also ","then ","the ","for "]
	for word in filler_words:
		cmd=cmd.replace(word,"")
	cmds=cmd.split('and')
	return cmds


