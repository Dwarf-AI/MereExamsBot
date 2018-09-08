from random import choice

def anything_else():
    return choice(['How else can I help you?',
                            'What else I can do for you?',
                            'Anything else you want me to help with?'])

def detail_gen(detail_type, id, value):
	return choice([f"{detail_type} of {id} is {value}.",
					f"As much as I remember, {detail_type} of {id} is {value}.",
					f"As my creators told me, {detail_type} of {id} is {value}.",
					f"As per MHRD records, {detail_type} of {id} is {value}."
					]) 
                          