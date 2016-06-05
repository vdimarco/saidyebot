import sys
from wit import Wit
################################################
# access_token = "KIUPZGZHRIUHRMBOV5YKGQ2CGDD3X3ZJ"
input_text_for_wit = "hi!"
################################################

def return_text_of_wit_reply(input_text_for_wit):
	resp = client.message(input_text_for_wit)
	for k,v in resp.items():
		if k=='entities':
			for k1,v1 in v.items():
				if k1=='greeting':
					for k2,v2 in v1[0].items():
						result = v2
	return result
def say(session_id, context, msg):
    print(msg)

def merge(session_id, context, entities, msg):
    return context

def error(session_id, context, e):
    print(str(e))
actions = {
    'say': say,
    'merge': merge,
    'error': error,
}


client = Wit("KIUPZGZHRIUHRMBOV5YKGQ2CGDD3X3ZJ", actions)
# print return_text_of_wit_reply(access_token, input_text_for_wit)
