from Moderation import classify
import os

async def Image_Moderation(image_path):
    # Вызов метода классификации
    result = classify.classify_image(image_path)

    # Вывод результата
    for label, score in result.items():
        print(f"{label}: {score:.5f}")

    # Проверка, является ли изображение NSFW
    if 'nsfw' in result and result['nsfw'] > 0.7:
        os.remove(image_path)
        return True
    else:
        return False