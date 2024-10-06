import tensorflow as tf
import numpy as np

# Загрузка модели и меток
MODEL_PATH = 'Moderation/retrained_graph.pb'
LABELS_PATH = 'Moderation/retrained_labels.txt'

def load_graph(model_path):
    with tf.io.gfile.GFile(model_path, 'rb') as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

def load_labels(label_path):
    with open(label_path, 'r') as f:
        return [line.strip() for line in f.readlines()]

def classify_image(image_path):
    # Загрузка модели и меток
    load_graph(MODEL_PATH)
    labels = load_labels(LABELS_PATH)

    # Инициализация сессии
    with tf.compat.v1.Session() as sess:
        # Получение тензоров для входных данных и выходных результатов
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        image_data = tf.io.gfile.GFile(image_path, 'rb').read()

        # Выполнение классификации
        predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)

        # Получение результата
        top_k = predictions.argsort()[-len(predictions):][::-1]
        result = {}
        for node_id in top_k:
            human_string = labels[node_id]
            score = predictions[node_id]
            result[human_string] = score

        return result

# Если скрипт запускается напрямую, а не как модуль
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python classify.py <image_path>")
    else:
        image_path = sys.argv[1]
        result = classify_image(image_path)
        for label, score in result.items():
            print(f"{label}: {score:.5f}")