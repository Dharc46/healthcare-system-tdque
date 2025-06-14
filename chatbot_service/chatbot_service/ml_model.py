import numpy as np
import tensorflow as tf

# Training data từ VIRTUAL ROBOT FOR HEATHCARE ASSISTANCE.pdf
X_train = np.array([
    [1,1,0,1,0,0],  # Flu
    [0,1,1,0,0,0],  # Cold
    [1,1,0,0,1,0],  # COVID-19
    [0,0,1,0,0,1]  # Allergy
], dtype=np.float32)

y_train = tf.keras.utils.to_categorical([0,1,2,3], num_classes=4)
diseases = ["Flu", "Cold", "COVID-19", "Allergy"]

def build_model():
    inputs = tf.keras.Input(shape=(6,))
    x = tf.keras.layers.Dense(16, activation='relu')(inputs)
    x = tf.keras.layers.Dropout(0.5)(x, training=True)
    x = tf.keras.layers.Dense(16, activation='relu')(x)
    x = tf.keras.layers.Dropout(0.5)(x, training=True)
    outputs = tf.keras.layers.Dense(4, activation='softmax')(x)
    model = tf.keras.Model(inputs, outputs)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=100, verbose=0)
    return model

def predict_with_uncertainty(model, x, n_iter=100):
    preds = np.array([model(x, training=True).numpy() for _ in range(n_iter)])
    mean = preds.mean(axis=0)
    std = preds.std(axis=0)
    return mean, std

# Khởi tạo mô hình
model = build_model()

# Mapping xét nghiệm và thuốc từ PDF
test_map = {
    "Flu": "Influenza A/B test",
    "Cold": "Nasal swab",
    "COVID-19": "PCR test",
    "Allergy": "Allergy skin test"
}
medicine_map = {
    "Flu": "Oseltamivir (Tamiflu)",
    "Cold": "Rest, fluids, antihistamines",
    "COVID-19": "Isolation + Paracetamol",
    "Allergy": "Loratadine or Cetirizine"
}