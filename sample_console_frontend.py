import requests
import argparse

# Basic routines, don't need to go much over them, although I would advise
# looking into how streaming and non-streaming responses are being handled.

def main_sync():
    response = requests.post(
        'http://172.16.101.171:42069/generate',
        json={
            'prompt': [
                {
                    'role': 'system',
                    'content': input("Enter system prompt: ")
                },
                {
                    'role': 'user',
                    'content': input("Enter prompt: ")
                }
            ],
            'stream': False,
        }
    )
    print(response.content.decode('utf-8'))

def main_async():
    for response in requests.post(
        'http://172.16.101.171:42069/generate',
        json={
            'prompt': [
                {
                    'role': 'system',
                    'content': input("Enter system prompt: ")
                },
                {
                    'role': 'user',
                    'content': input("Enter prompt: ")
                }
            ],
            'stream': True,
        },
        stream=True,
    ).iter_content(chunk_size=4096):
        print(response.decode('utf-8'), end='', flush=True)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--stream',
        type=bool,
        default=False,
        help="Whether to stream the response or get it all in one go."
    )
    args = parser.parse_args()

    if args.stream:
        main_async()
    else:
        main_sync()