from flask import Flask, jsonify, request 
import torch
from backend_classes import *
from torchvision.transforms import Compose, Resize, ToTensor, Normalize
import torchvision
import torchvision.transforms.functional as F
import os
from PIL import Image
import base64
import io
from flask_cors import CORS


transform = Compose([
    Resize((256, 256)),          # Resize to the input size expected by the model
    ToTensor(),                  # Convert the image to a PyTorch tensor
    Normalize(mean=0.5, std=0.5) # Normalize to the range [-1, 1] (same as training)
])

### We should load all trainers we need well in advance,
### Possibly into a single array??
# Load the trained generator
device = "cuda" if torch.cuda.is_available() else "cpu"

generators = [Generator(in_channels=3, features=64), Generator(in_channels=3, features=64)]

generators[0].load_state_dict(torch.load("models/monet/generator_weights.pth", map_location=device))
generators[0].to(device).eval()

generators[1].load_state_dict(torch.load("models/vangogh/generator_weights.pth", map_location=device))
generators[1].to(device).eval()


# creating a Flask app 
app = Flask(__name__) 
CORS(app)
  
def preprocess_image(img):
    image = img.convert("RGB")  # Ensure it's in RGB format
    return transform(image).unsqueeze(0).to(device)

# on the terminal type: curl http://127.0.0.1:5000/ 
# returns hello world when we use GET. 
# returns the data that we send when we use POST. 
@app.route('/processing/<int:gennum>', methods=['POST'])
def process(gennum):
    file = request.files['image']
    
    img = Image.open(file.stream)

    #data = file.stream.read()
    #data = base64.b64encode(data).decode()
    
    img = preprocess_image(img)

    with torch.no_grad():  # Disable gradient calculations for inference
        img = generators[gennum](img)

    img = img.squeeze(0).cpu() * 0.5 + 0.5

    img = F.to_pil_image(img)
    
    buffer = io.BytesIO()
    img.save(buffer, 'png')
    buffer.seek(0)
    
    data = buffer.read()
    data = base64.b64encode(data).decode()
    
    #return jsonify({
    #            'msg': 'success', 
    #            'size': [img.width, img.height], 
    #            'format': img.format,
    #            'img': data
    #       })

    return f'<img src="data:image/png;base64,{data}">'

  
  

# driver function 
if __name__ == '__main__': 
  
    app.run(debug = True) 
