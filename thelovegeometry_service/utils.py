def clean_request_text_input(input_: bytes):
    return input_.decode('utf-8').strip()