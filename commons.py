from colorama import Fore

def color_println(string: str, color) -> str:
    print(color + string + Fore.RESET)

def divide_list_into_chunks(lst, chunk_size):
    if chunk_size <= 0:
        raise ValueError("Chunk size must be a positive integer.")
    if len(lst) == 0:
        raise ValueError("List must not be empty.")

    chunks = []
    for i in range(0, len(lst), chunk_size):
        chunk = lst[i:i + chunk_size]
        chunks.append(chunk)
    return chunks
