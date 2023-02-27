from emora_stdm import DialogueFlow

def test_emora():
    chatbot = DialogueFlow('start')
    transitions = {
        'state': 'start',
        '"Hello. How are you?"': {
            '[{good, okay, fine}]': {
                '"Good. I am doing well too."': {
                    'error': {
                        '"See you later!"': 'end'
                    }
                }
            },
            'error': {
                '"Well I hope your day gets better!"': {
                    'error': {
                        '"Bye!"': 'end'
                    }
                }
            }
        }
    }
    chatbot.load_transitions(transitions)
    
    return chatbot

if __name__ == "__main__":
    chatbot = test_emora()
    chatbot.run()