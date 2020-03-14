import tensorflow as tf


from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

import os
import numpy as np

class_names = ['melanoma', 'nevus', 'seborrheic_keratosis']

disease_name = {'melanoma': 'Melanoma', 'nevus': 'Nevus', 'seborrheic_keratosis': 'Seborrheic keratosis'}

disease_info = {'melanoma': """Melanoma occurs when the pigment-producing cells that give colour to the skin become cancerous.
Symptoms might include a new, unusual growth or a change in an existing mole. Melanomas can occur anywhere on the body.
Treatment may involve surgery, radiation, medication or in some cases, chemotherapy.""",

'nevus': """A common pigmented skin lesion, usually developing during adulthood.
Most people develop several moles (naevi) throughout adulthood.
Moles can be found anywhere on the body, usually in sun-exposed areas, and are usually brown, smooth and slightly raised.
In most cases, a nevus is benign and doesn't require treatment. Rarely, they turn into melanoma or other skin cancers. A nevus that changes shape, grows bigger or darkens should be evaluated for removal.""",

'seborrheic_keratosis': """A non-cancerous skin condition that appears as a waxy brown, black or tan growth.
A seborrhoeic keratosis is one of the most common non-cancerous skin growths in older adults. While it's possible for one to appear on its own, multiple growths are more common.
Seborrheic keratosis often appears on the face, chest, shoulders or back. It has a waxy, scaly, slightly elevated appearance.
No treatment is necessary. If the seborrhoeic keratosis causes irritation, it can be removed by a doctor."""
}


model = load_model(os.getcwd() + '/project/category_model.h5')

def predict_disease(image_path):
    img = image.load_img(image_path, target_size=(150, 150))
    img = np.expand_dims(img, axis=0)

    prediction = model.predict_classes(img)

    result = class_names[int(prediction)]

    return disease_name[result], disease_info[result]
