from model import Model
from llm_chat_history import LLMChatHistory

import os
import argparse
import configparser

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='TensorRT-LLM Demo',
        description=(
            "A demo that hosts how TensorRT-LLM runs and performs"
            "inference on an engine."
        )
    )

    parser.add_argument(
        '--gpu',
        type=int,
        default=0,
        help='Which GPU to use for hosting the LLM engine.'
    )

    parser.add_argument(
        '--run_type',
        type=str,
        default='local',
        choices=['local', 'api'],
        help='Whether to host the LLM locally or through an API.'
    )

    parser.add_argument(
        '--port',
        type=int,
        default=50000,
        help='What port to launch the application on.'
    )

    return parser.parse_args()


args = get_args()

def main_local() -> None:
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Pick out the model to use
    model_to_use = config.get('defaults', 'model')
    model = Model(
        # Retrieved picked model's directory.
        config.get('model_paths', model_to_use)
    )

    # Initialise the chat history.
    history = LLMChatHistory()

    history.append(
        {
            'role': 'system',
            'content': input("Enter your system prompt: ")
        }
    )

    print("Starting chat with the LLM...\n\n")

    while True:
        try:
            history.append(
                {
                    'role': 'user',
                    'content': input("Message: ")
                }
            )

            response = ''
            for output in model.generate(
                history.history,
                stream=True,
            ):
                print(output, end='', flush=True)
                response += output
            print("\n")
            
            history.append(
                {
                    'role': 'assistant',
                    'content': response
                }
            )

        except KeyboardInterrupt:
            print("\n\nClosing gracefully.")
            break
    

def main_api() -> None:
    import fastapi, uvicorn

    config = configparser.ConfigParser()
    config.read('config.ini')

    model_to_use = config.get('defaults', 'model')
    model = Model(
        config.get('model_paths', model_to_use)
    )

    api = fastapi.FastAPI()
    history = LLMChatHistory()

    #! EXPERIMENTAL - Use if only ONE person is communicating with the API.
    #  Assumes that only one person is communicating with the LLM, hence
    #  handling of the history done in the backend.
    @api.post('/handled_generate')
    def generate_handled(
        body: dict = fastapi.Body(...)
    ) -> fastapi.responses.StreamingResponse:
        """"""
        if len(history.history) == 0:
            if body.get('system') is None:
                raise ValueError("A system prompt is required initially.")
            else:
                history.append(
                    {
                        'role': 'system',
                        'content': body.get('system')
                    }
                )
        history.append(
            {
                'role': 'user',
                'content': body.get('prompt')
            }
        )

        return fastapi.responses.StreamingResponse(
            content=(
                model.generate(
                    prompt=history.history,
                    stream=body.get('stream', False),
                    do_sample=body.get('do_sample'),
                    temperature=body.get('temperature'),
                    top_k=body.get('top_k'),
                    top_p=body.get('top_p'),
                    repetition_penalty=body.get('repetition_penalty'),
                    max_new_tokens=body.get('max_new_tokens')
                )
            ),
            media_type='text/plain'
        )
    
    @api.post('/generate')
    async def generate(
        body: dict = fastapi.Body(...)
    ) -> fastapi.responses.StreamingResponse:
        # This one only accepts list-of-dictionaries format.
        if not isinstance(body.get('prompt'), list):
            raise TypeError("I can only accept List-Of-Dictionaries prompt.")

        return fastapi.responses.StreamingResponse(
            content=model.generate(
                prompt=body.get('prompt'),
                stream=body.get('stream', False),
                do_sample=body.get('do_sample'),
                temperature=body.get('temperature'),
                top_k=body.get('top_k'),
                top_p=body.get('top_p'),
                repetition_penalty=body.get('repetition_penalty'),
                max_new_tokens=body.get('max_new_tokens')
            ),
            media_type='text/plain'
        )
    
    uvicorn.run(
        api,
        host='0.0.0.0',
        port=int(args.port)
    )

if __name__ == '__main__':
    os.environ['CUDA_VISIBLE_DEVICES'] = str(args.gpu)
    if args.run_type == 'local':
        main_local()
    else:
        main_api()