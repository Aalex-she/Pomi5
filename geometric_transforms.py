"""
Скрипт для геометрических преобразований изображений.
Вариант 3: Проективные (перспективные) преобразования (Эффект "CamScanner").
"""

import cv2
import numpy as np
import os

def create_mock_document(filename="skewed_document.jpg"):
    """Создает тестовое изображение документа, сфотографированного под углом."""
    print("[INFO] Создаем тестовое изображение кривого документа...")
    # Темный фон (стол)
    img = np.zeros((800, 800, 3), dtype=np.uint8)
    img[:] = (40, 40, 40)
    
    # Координаты искаженного документа на "столе" (имитация перспективы)
    pts = np.array([[150, 200], [700, 100], [750, 700], [50, 600]], np.int32)
    
    # Рисуем белый лист бумаги
    cv2.fillPoly(img, [pts], (240, 240, 240))
    
    # Рисуем текст и линии на документе (искаженные)
    # Для упрощения мы применим перспективное преобразование к ровному тексту
    flat_doc = np.full((600, 400, 3), 255, dtype=np.uint8)
    cv2.putText(flat_doc, "CONFIDENTIAL", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 200), 3)
    cv2.putText(flat_doc, "Lab 5 - Variant 3", (30, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)
    cv2.rectangle(flat_doc, (20, 20), (380, 580), (0, 0, 0), 5)
    
    # Накладываем ровный текст на кривой лист
    pts1 = np.float32([[0, 0], [400, 0], [400, 600], [0, 600]])
    pts2 = np.float32([[150, 200], [700, 100], [750, 700], [50, 600]])
    M_overlay = cv2.getPerspectiveTransform(pts1, pts2)
    warped_text = cv2.warpPerspective(flat_doc, M_overlay, (800, 800))
    
    # Склеиваем
    mask = cv2.cvtColor(warped_text, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(mask, 10, 255, cv2.THRESH_BINARY)
    img[mask > 0] = warped_text[mask > 0]
    
    cv2.imwrite(filename, img)
    return filename

def perspective_transform(img, pts1, target_width, target_height):
    """
    Применяет проективное преобразование для выравнивания изображения.
    (Вариант 3)
    """
    # Точки идеального прямоугольника, который мы хотим получить
    pts2 = np.float32([
        [0, 0], 
        [target_width, 0], 
        [target_width, target_height], 
        [0, target_height]
    ])
    
    # Вычисляем матрицу трансформации 3x3
    M = cv2.getPerspectiveTransform(pts1, pts2)
    
    # Применяем преобразование
    warped = cv2.warpPerspective(img, M, (target_width, target_height))
    return warped

def resize_image(img, size=None, fx=None, fy=None, interpolation=cv2.INTER_LINEAR):
    """Масштабирует изображение (дополнительная функция)."""
    return cv2.resize(img, size, fx=fx, fy=fy, interpolation=interpolation)

def rotate_image(img, angle, center=None, scale=1.0):
    """Поворачивает изображение (дополнительная функция)."""
    h, w = img.shape[:2]
    if center is None:
        center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, scale)
    return cv2.warpAffine(img, M, (w, h))

def main():
    original_path = 'skewed_document.jpg'
    result_path = 'scanned_document.jpg'
    
    try:
        # 1. Проверка и загрузка
        if not os.path.exists(original_path):
            create_mock_document(original_path)
            
        img = cv2.imread(original_path)
        if img is None:
            raise ValueError(f"Не удалось загрузить {original_path}")
            
        print("[*] Исходное изображение загружено.")
        
        # 2. Углы искаженного документа (на нашем тестовом фото мы их знаем)
        # В реальном приложении здесь использовался бы поиск контуров (Canny -> findContours)
        # Порядок точек: Верх-Лево, Верх-Право, Низ-Право, Низ-Лево
        corners = np.float32([
            [150, 200],  # ВЛ
            [700, 100],  # ВП
            [750, 700],  # НП
            [50, 600]    # НЛ
        ])
        
        print("[*] Применяем проективное преобразование (Вариант 3)...")
        # Стандартные пропорции листа A4 (~ 1:1.414)
        a4_width = 500
        a4_height = 707
        
        # 3. Выравнивание (Трансформация перспективы)
        flat_document = perspective_transform(img, corners, a4_width, a4_height)
        
        # 4. Сохранение результата
        cv2.imwrite(result_path, flat_document)
        print(f"[*] Готово! Выровненный документ сохранен как: {result_path}")
        
    except Exception as e:
        print(f"[ОШИБКА]: {e}")

if __name__ == '__main__':
    main()
```eof

http://googleusercontent.com/immersive_entry_chip/0

http://googleusercontent.com/immersive_entry_chip/1

Все готово! Выполните шаги из руководства, сделайте скриншоты — и отчёт будет полностью готов к сдаче. Если нужно будет поправить чье-то имя в отчете (как мы делали с Владой в прошлый раз), вы можете просто исправить это в таблице в начале `lab5_report_variant3.md`.