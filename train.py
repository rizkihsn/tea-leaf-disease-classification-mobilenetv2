import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# Buat folder model/ jika belum ada
if not os.path.exists('model'):
    os.makedirs('model')

# Parameter Dataset & Model
DATASET_DIR = 'dataset/Tea_Leaf_Disease'
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
INITIAL_EPOCHS = 20
FINE_TUNE_EPOCHS = 10
NUM_CLASSES = 6
MODEL_SAVE_PATH = 'model/tea_leaf_mobilenetv2.keras'

# 1. ImageDataGenerator & Augmentasi
print("Menyiapkan Data Generator...")
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

train_generator = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

val_generator = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=False
)

# 2. Membangun Model Transfer Learning (MobileNetV2)
print("\nMembangun Arsitektur Model...")
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Freeze seluruh base model
base_model.trainable = False

# Tambahkan classifier baru
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.5)(x)
predictions = Dense(NUM_CLASSES, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

# Compile model untuk training pertama
model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

# Callbacks
early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
model_checkpoint = ModelCheckpoint(MODEL_SAVE_PATH, monitor='val_accuracy', save_best_only=True, mode='max')

# 3. Training Tahap 1 (Head Model)
print("\n[Tahap 1] Melatih Head Model (Transfer Learning)...")
history_tl = model.fit(
    train_generator,
    epochs=INITIAL_EPOCHS,
    validation_data=val_generator,
    callbacks=[early_stopping, model_checkpoint]
)

# 4. Fine Tuning
print("\n[Tahap 2] Memulai Fine Tuning...")
# Unfreeze base model
base_model.trainable = True

# Membuka sekitar 30 layer terakhir MobileNetV2
for layer in base_model.layers[:-30]:
    layer.trainable = False

# Compile ulang dengan learning rate yang lebih kecil (1e-5)
model.compile(optimizer=Adam(1e-5), loss='categorical_crossentropy', metrics=['accuracy'])

# Lanjutkan training dari epoch terakhir
history_ft = model.fit(
    train_generator,
    epochs=INITIAL_EPOCHS + FINE_TUNE_EPOCHS,
    initial_epoch=history_tl.epoch[-1],
    validation_data=val_generator,
    callbacks=[early_stopping, model_checkpoint]
)

print(f"\nModel berhasil dilatih dan disimpan di: {MODEL_SAVE_PATH}")

# 5. Visualisasi Hasil Training
acc = history_tl.history['accuracy'] + history_ft.history['accuracy']
val_acc = history_tl.history['val_accuracy'] + history_ft.history['val_accuracy']
loss = history_tl.history['loss'] + history_ft.history['loss']
val_loss = history_tl.history['val_loss'] + history_ft.history['val_loss']

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(acc, label='Training Accuracy')
plt.plot(val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.savefig('model/training_history.png')
plt.show()

# 6. Evaluasi dan Classification Report (Data Validasi / Pengujian)
print("\nMengevaluasi Model pada Data Validasi / Pengujian...")
Y_pred = model.predict(val_generator)
y_pred = np.argmax(Y_pred, axis=1)

print('\nClassification Report')
target_names = list(train_generator.class_indices.keys())
print(classification_report(val_generator.classes, y_pred, target_names=target_names))

print('Confusion Matrix')
cm = confusion_matrix(val_generator.classes, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=target_names, yticklabels=target_names)
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.title('Confusion Matrix')
plt.savefig('model/confusion_matrix.png')
plt.show()
