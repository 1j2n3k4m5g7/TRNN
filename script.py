import tensorflow as tf
import numpy as np
import os
import gc
import sys

gc.collect()

def get_model():
    model = tf.keras.models.Sequential([

        # ---- augmentation ----
        tf.keras.layers.RandomRotation(0.1),
        tf.keras.layers.RandomTranslation(0.1, 0.1),
        tf.keras.layers.RandomZoom(0.2),

        # ---- main ----
        tf.keras.layers.Rescaling(1./255, input_shape=(48, 48, 1)),

        # layers

        # 1st layer
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        # 2nd
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        # 3rd
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.MaxPooling2D((2, 2)),

        # ---- rest (trailer) ----
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

data_dir = input("Enter the path to your dataset root folder:\n")
model_dir=input("Enter model path (where to save/from where to load):\n")
dataset = tf.keras.utils.image_dataset_from_directory(
    data_dir, image_size=(48, 48), batch_size=16, color_mode='grayscale'
)
class_names=dataset.class_names
num_classes=len(class_names)

while True:
    choice=input("Do you want to train (T), predict (P) or quit (Q)?\n").upper()

    if choice == 'T':
        model=get_model()
        model.fit(dataset, epochs=400)
        model.save(f'{model_dir}/handwriting_model.keras')
        print(class_names)
        print("Model saved as handwriting_model.keras")

    elif choice == 'P':
        model=tf.keras.models.load_model(f'{model_dir}/handwriting_model.keras')
        img_path = input("Enter path to the image file to check:\n")

        img=tf.keras.utils.load_img(
            img_path, target_size=(48, 48), color_mode='grayscale'
        )
        img_array=tf.keras.utils.img_to_array(img)
        img_array=np.expand_dims(img_array, 0)

        predictions=model.predict(img_array)
        predicted_idx=np.argmax(predictions)

        print(f"Prediction: {class_names[predicted_idx]}")

    elif choice == 'Q':
        sys.exit(0)