"""
Simple TensorFlow proctoring test
Detects: multiple persons, mobile phones using webcam
"""

import cv2
import numpy as np
from datetime import datetime

# Check if required packages are installed
try:
    import tensorflow as tf
    print(f"✓ TensorFlow version: {tf.__version__}")
except ImportError:
    print("✗ TensorFlow not installed. Run: pip install tensorflow")
    exit()

try:
    from tensorflow import keras
    print(f"✓ Keras available")
except ImportError:
    print("✗ Keras not available")
    exit()

print("\n" + "="*60)
print("PROCTORING TEST - Press 'q' to quit")
print("="*60)

# Initialize webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("✗ Cannot access webcam!")
    exit()

print("✓ Webcam opened successfully")
print("\nLoading TensorFlow model...")

# Load pre-trained MobileNet SSD model for object detection
# This will download the model first time (~25MB)
try:
    # Using TensorFlow Hub model
    import tensorflow_hub as hub
    
    # Load COCO-SSD model from TensorFlow Hub
    detector = hub.load("https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2")
    print("✓ Model loaded successfully!\n")
    
    # COCO class labels
    PERSON_CLASS = 1
    CELL_PHONE_CLASS = 77
    
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("✗ Failed to grab frame")
            break
        
        frame_count += 1
        
        # Process every 30 frames (about 1 second at 30fps)
        if frame_count % 30 == 0:
            # Prepare image for detection
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            input_tensor = tf.convert_to_tensor(rgb_frame)
            input_tensor = input_tensor[tf.newaxis, ...]
            
            # Run detection
            detections = detector(input_tensor)
            
            # Extract results
            detection_classes = detections['detection_classes'][0].numpy().astype(int)
            detection_scores = detections['detection_scores'][0].numpy()
            
            # Count persons and phones (confidence > 0.5)
            person_count = sum(1 for i, score in enumerate(detection_scores) 
                             if detection_classes[i] == PERSON_CLASS and score > 0.5)
            phone_count = sum(1 for i, score in enumerate(detection_scores) 
                            if detection_classes[i] == CELL_PHONE_CLASS and score > 0.5)
            
            # Check violations
            status = "✓ OK"
            violations = []
            
            if person_count == 0:
                violations.append("NO PERSON DETECTED")
                status = "⚠ WARNING"
            elif person_count > 1:
                violations.append(f"MULTIPLE PERSONS ({person_count})")
                status = "⚠ WARNING"
            
            if phone_count > 0:
                violations.append(f"MOBILE PHONE DETECTED ({phone_count})")
                status = "⚠ WARNING"
            
            # Display results
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"\n[{timestamp}] {status}")
            print(f"  Persons: {person_count} | Phones: {phone_count}")
            if violations:
                print(f"  ⚠ VIOLATIONS: {', '.join(violations)}")
        
        # Display video feed
        cv2.putText(frame, f"Monitoring... (Press 'q' to quit)", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow('Proctoring Test', frame)
        
        # Quit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("\n✓ Test stopped by user")
            break
    
except ImportError:
    print("✗ TensorFlow Hub not installed. Run: pip install tensorflow-hub")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    print("\nTrying alternative approach with OpenCV DNN...")
    
    # Fallback: Use OpenCV's DNN module with pre-trained model
    print("This requires downloading model files separately.")
    print("For simplest approach, install: pip install tensorflow-hub")

# Cleanup
cap.release()
cv2.destroyAllWindows()
print("\n✓ Test complete!")
