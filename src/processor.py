import cv2
import numpy as np
import os

def process_stamps(image_path, output_folder, prefix, start_counter, suffix, pad_top=20, pad_bottom=50, pad_left=20, pad_right=20):
    img_array = np.fromfile(image_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    if img is None:
        raise Exception(f"Erro: Não foi possível carregar a imagem: {image_path}")
    
    img_h, img_w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 40, 130)

    # Bloqueio de 5x5 para garantir que os dentes ficam selados
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)
    
    # Procurar contornos
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    detected_stamps = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 60 and h > 60 and w < img_w * 0.95 and h < img_h * 0.95:
            detected_stamps.append((x, y, w, h))
            
    if not detected_stamps:
        raise Exception(f"Nenhum selo foi detetado na imagem {os.path.basename(image_path)}.")

    # ORDENAÇÃO (Esquerda para a Direita, Cima para Baixo)
    avg_height = np.mean([item[3] for item in detected_stamps])
    y_tolerance = avg_height / 2
    
    detected_stamps.sort(key=lambda b: b[1])
    
    rows = []
    current_row = [detected_stamps[0]]
    
    for box in detected_stamps[1:]:
        if box[1] <= current_row[-1][1] + y_tolerance:
            current_row.append(box)
        else:
            rows.append(current_row)
            current_row = [box]
    rows.append(current_row) 
    
    sorted_stamps = []
    for row in rows:
        row.sort(key=lambda b: b[0])
        sorted_stamps.extend(row)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    counter = start_counter
    
    for (x, y, w, h) in sorted_stamps:
        top = max(0, y - pad_top)
        bottom = min(img_h, y + h + pad_bottom)
        left = max(0, x - pad_left)
        right = min(img_w, x + w + pad_right)
        
        stamp_roi = img[top:bottom, left:right]
        
        file_name = f"{prefix}{counter}{suffix}.jpg"
        final_path = os.path.join(output_folder, file_name)
        
        is_success, im_buf_arr = cv2.imencode(".jpg", stamp_roi)
        if is_success:
            im_buf_arr.tofile(final_path)
            
        counter += 1

    return len(sorted_stamps), counter