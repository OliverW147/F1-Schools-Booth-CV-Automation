import cv2
import mediapipe as mp
from statistics import mode
import requests
import time

no_fingers_timer = time.time()

# Replace <YOUR_WEBHOOK_URL> with the URL of your Discord webhook
webhook_url = ''
while True:
    try:
        lastfinger = 0
        mp_hands = mp.solutions.hands

        # For webcam input:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cv2.destroyAllWindows()
        with mp_hands.Hands(
                model_complexity=0,
                min_detection_confidence=0.8,
                min_tracking_confidence=0.5) as hands:

            finger_count_list = []  # initialize list to store finger counts

            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image)

                # Initially set finger count to 0 for each cap
                fingerCount = 0

                if results.multi_hand_landmarks:

                    for hand_landmarks in results.multi_hand_landmarks:
                        # Get hand index to check label (left or right)
                        handIndex = results.multi_hand_landmarks.index(hand_landmarks)
                        handLabel = results.multi_handedness[handIndex].classification[0].label

                        # Set variable to keep landmarks positions (x and y)
                        handLandmarks = []

                        # Fill list with x and y positions of each landmark
                        for landmarks in hand_landmarks.landmark:
                            handLandmarks.append([landmarks.x, landmarks.y])

                        # Test conditions for each finger: Count is increased if finger is
                        #   considered raised.
                        # Thumb: TIP x position must be greater or lower than IP x position,
                        #   depending on hand label.
                        if handLabel == "Left" and handLandmarks[4][0] > handLandmarks[3][0]:
                            fingerCount = fingerCount + 1
                        elif handLabel == "Right" and handLandmarks[4][0] < handLandmarks[3][0]:
                            fingerCount = fingerCount + 1

                        # Other fingers: TIP y position must be lower than PIP y position,
                        #   as image origin is in the upper left corner.
                        if handLandmarks[8][1] < handLandmarks[6][1]:  # Index finger
                            fingerCount = fingerCount + 1
                        if handLandmarks[12][1] < handLandmarks[10][1]:  # Middle finger
                            fingerCount = fingerCount + 1
                        if handLandmarks[16][1] < handLandmarks[14][1]:  # Ring finger
                            fingerCount = fingerCount + 1
                        if handLandmarks[20][1] < handLandmarks[18][1]:  # Pinky
                            fingerCount = fingerCount + 1

                # Add the finger count to the list
                finger_count_list.append(fingerCount)

                # Print the mode of the last ten finger count values
                if len(finger_count_list) == 25:

                    # Remove the oldest finger count from the list
                    finger_count_list.pop(0)

                if cv2.waitKey(5) & 0xFF == 27:
                    break

                if 0 < fingerCount < 4 and lastfinger != fingerCount:
                    lastfinger = fingerCount
                    message = {"content": f"{fingerCount}"}
                    response = requests.post(webhook_url, json=message)
                    lastresponse = fingerCount
                    print(str(fingerCount))

                if fingerCount == 0 and lastfinger != 4:
                    current_time = time.time()
                    time_elapsed = current_time - no_fingers_timer
                    if time_elapsed >= 15:
                        lastfinger = 4
                        message = {"content": f"4"}
                        response = requests.post(webhook_url, json=message)
                        lastresponse = fingerCount
                        print(str(fingerCount))
                else:
                    no_fingers_timer = time.time()


            cap.release()


    except Exception as e:
        print(e)