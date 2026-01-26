

intent_map={
	"OPEN_APP":["open","start","run"],
	"CLOSE_APP":["close","exit","quit"],
	"MINI_OFF":["sleep"],
	"TEXT_TYPE":["type"]

}

def intent_detect(text:str):
	for intent,keywords in intent_map.items():
		for kw in keywords:
			if kw in text:
				return intent,kw
	return None,None

def argument_extract(text:str,action_word:str):
	return text.replace(action_word,"").strip()

def parse(text:str):
	intent,action_word=intent_detect(text)
	if not intent:
		return None
	argument=argument_extract(text,action_word)
	print("action: ",intent,"argument: ",argument)
	return {
	"action":intent,
	"argument":argument or None
	}
