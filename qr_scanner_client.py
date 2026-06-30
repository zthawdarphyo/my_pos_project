import cv2
import numpy as np
import requests

API_URL = "http://127.0.0.1:8000/api/scan-product/" 

# OpenCV ရဲ့ အဆင့်မြင့် QR Code Detector ကို သုံးထားပါတယ်
qr_detector = cv2.QRCodeDetector()

cap = cv2.VideoCapture(0)

# Laptop ကင်မရာကို ပုံရိပ်အပြတ်သားဆုံးရအောင် ညှိပါတယ်
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print("--- အဆင့်မြင့် QR Code Scanner စတင်နေပါပြီ (ပိတ်ရန် 'q' ကို နှိပ်ပါ) ---")

while True:
    success, frame = cap.read()
    if not success: break

    # --- IMAGE ENHANCEMENT (QR ဖတ်ရလွယ်အောင် ပုံရိပ်ကို အပြင်းအထန် ပြင်ဆင်ခြင်း) ---
    # ၁။ ပုံကို Grayscale ပြောင်းတယ်
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # ၂။ အလင်းပြန်တာတွေကို သက်သာအောင်နဲ့ QR အကွက်တွေကို ထင်ရှားအောင် Contrast မြှင့်တင်ခြင်း
    gray = cv2.equalizeHist(gray)
    
    # ၃။ ပုံကို မှုန်ဝါးမနေအောင် Sharp ဖြစ်အောင် လုပ်ခြင်း
    gaussian_blur = cv2.GaussianBlur(gray, (0, 0), 3)
    sharpened = cv2.addWeighted(gray, 1.5, gaussian_blur, -0.5, 0)

    # QR Code ကို Detector နဲ့ ရှာဖွေဖတ်ရှုခြင်း
    # (မူရင်း frame ရော၊ ပြင်ဆင်ထားတဲ့ sharpened ပုံရော နှစ်ခုလုံးမှာ လိုက်ရှာခိုင်းထားပါတယ်)
    detected_data, bbox, _ = qr_detector.detectAndDecode(sharpened)
    
    if not detected_data:
        detected_data, bbox, _ = qr_detector.detectAndDecode(frame)

    # QR Code တစ်ခုခု မိပြီဆိုရင်
    if detected_data:
        print(f"[QR တွေ့ရှိ] ကုဒ်နံပါတ် -> {detected_data}")

        # QR Code ဘေးပတ်လည်မှာ လေးထောင့်စိမ်းကွက် ပြသရန်
        if bbox is not None and len(bbox) > 0:
            for i in range(len(bbox)):
                pt1 = tuple(map(int, bbox[i][0]))
                pt2 = tuple(map(int, bbox[(i+1) % len(bbox)][0]))
                cv2.line(frame, pt1, pt2, (0, 255, 0), 3)

        # Django Server ဆီ သို့ Data ပို့ခြင်း
        try:
            response = requests.post(API_URL, data={'product_code': detected_data}, timeout=2)
            if response.status_code == 200:
                print("Server သို့ ပို့ဆောင်မှု အောင်မြင်သည်။")
        except requests.exceptions.RequestException:
            print("Server ချိတ်ဆက်မှု မရရှိပါ။")

    # Screen ပြသခြင်း
    cv2.imshow('POS Classic QR Scanner (Advanced Mode)', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()