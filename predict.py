import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Define model path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'tea_leaf_mobilenetv2.keras')

# Define class labels (Alphabetical order based on flow_from_directory)
CLASS_LABELS = {
    0: 'Algal Spot',
    1: 'Brown Blight',
    2: 'Gray Blight',
    3: 'Healthy',
    4: 'Helopeltis',
    5: 'Red Spot'
}

# Global variable for model
model = None

def get_model():
    """Load model if not already loaded."""
    global model
    if model is None:
        if os.path.exists(MODEL_PATH):
            model = load_model(MODEL_PATH)
        else:
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Please train the model first.")
    return model

def predict_image(image_path):
    """
    Menerima path gambar, melakukan preprocessing, dan mengembalikan hasil prediksi.
    """
    try:
        # Load model
        m = get_model()

        # Load and preprocess image
        img = load_img(image_path, target_size=(224, 224))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Rescaling

        # Predict
        predictions = m.predict(img_array)[0]
        predicted_class_index = np.argmax(predictions)
        confidence = float(predictions[predicted_class_index]) * 100
        disease_name = CLASS_LABELS.get(predicted_class_index, "Unknown")

        return disease_name, confidence

    except Exception as e:
        error_msg = str(e)
        print(f"Error during prediction: {error_msg}")
        return False, error_msg
