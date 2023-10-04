from deep_translator import GoogleTranslator

def translate_en_de(to_translate):

    return GoogleTranslator(source='auto', target='de').translate(to_translate)

def translate_de_en(to_translate):

    return GoogleTranslator(source='auto', target='en').translate(to_translate)
