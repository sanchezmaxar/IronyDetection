import tensorflow as tf
import sys 
## Ejemplo de uso 
## La ruta de exportacion deber absoluta tal vez 
# python3 Exportador.py Experimento4/Pesos/weights0_g3.hd5 Experimento4/Modelo.json IronyDetection_Presentation/webapi/Modelos/Experimento4

# The export path contains the name and the version of the model
tf.keras.backend.set_learning_phase(0)  # Ignore dropout at inference
pesos=sys.argv[1]
modelo=sys.argv[2]
export_path =sys.argv[3] 
model=tf.keras.models.model_from_json(open(modelo).read())
model.load_weights(pesos)

# Fetch the Keras session and save the model
# The signature definition is defined by the input and output tensors
# And stored with the default serving key
with tf.keras.backend.get_session() as sess:
    tf.saved_model.simple_save(
        sess,
        export_path,
        inputs={'input_image': model.input},
        outputs={t.name: t for t in model.outputs})