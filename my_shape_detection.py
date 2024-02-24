import base64
from openai import OpenAI
import time

class shape_detection :
    def __init__(self,image_path):
        self.image_path = image_path
    
    def encode_image(self):
        with open(self.image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
        
    def detect_shape(self):
        image_url = f"data:image/jbeg;base64,{self.encode_image()}"

        gpt = OpenAI(
            organization="org-1YE6y1OohJmJIe8W3Xifd2RW",
            api_key="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",
        )
        r = gpt.chat.completions.create(
            model = 'gpt-4-vision-preview',
            messages = [
                {
                    "role" : "user",
                    "content" : [
                        {"type": "text", "text": "Given the following pill image, the list of possible shapes is:\nRound\nOval\nOblong\nEgg\n3 sided\n4 sided\nIn one word, select the shape that best represents this pill"},
                        {
                            "type" : "image_url",
                            "image_url": {
                                "url": image_url,
                                "detail" : "low"
                            },
                        }
                    ]
                }
            ],
            max_tokens=300,
        )

        return r.choices[0].message.content


## Sample Class Usage
if __name__ == "__main__":
    start = time.time()
    pill = shape_detection('./Pills/Pills/APO_Circle.JPG')
    result = pill.detect_shape()
    print(result)
    end = time.time()
    print(f'\n\nElapsed time = {end - start} seconds')

