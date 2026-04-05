import cv2
import numpy as np

try:
    import mediapipe as mp

    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    MEDIAPIPE_AVAILABLE = True
except:
    MEDIAPIPE_AVAILABLE = False
    mp_pose = None
    mp_drawing = None


class WorkoutDetector:
    def __init__(self):
        self.pose = None
        if MEDIAPIPE_AVAILABLE:
            self.pose = mp_pose.Pose(
                static_image_mode=False,
                model_complexity=0,
                enable_segmentation=False,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5,
            )
        self.rep_count = 0
        self.exercise = "head_rotation"
        self.base_values = {}
        self.form_feedback = ["Stand in frame"]
        self.calories_burned = 0
        self.state = "start"

    def set_exercise(self, exercise):
        self.exercise = exercise
        self.rep_count = 0
        self.base_values = {}
        self.form_feedback = ["Stand in frame"]
        self.calories_burned = 0
        self.state = "start"

    def detect_exercise(self, landmarks):
        if self.exercise == "head_rotation":
            return self.detect_head_rotation(landmarks)
        elif self.exercise == "shoulder_shrug":
            return self.detect_shoulder_shrug(landmarks)
        elif self.exercise == "arm_raise":
            return self.detect_arm_raise(landmarks)
        elif self.exercise == "side_bend":
            return self.detect_side_bend(landmarks)
        elif self.exercise == "neck_tilt":
            return self.detect_neck_tilt(landmarks)
        elif self.exercise == "neck_rotation":
            return self.detect_neck_rotation(landmarks)
        elif self.exercise == "squat":
            return self.detect_squat(landmarks)
        elif self.exercise == "pushup":
            return self.detect_pushup(landmarks)
        elif self.exercise == "jumping_jack":
            return self.detect_jumping_jack(landmarks)
        return ["Unknown exercise"]

    def detect_head_rotation(self, landmarks):
        nose = landmarks[mp_pose.PoseLandmark.NOSE]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2

        feedback = []

        if "center_x" not in self.base_values:
            self.base_values["center_x"] = shoulder_center_x
            feedback.append("Calibrated! Look left")
            return feedback

        offset = nose.x - self.base_values["center_x"]

        if offset < -0.08:
            if self.state == "start":
                self.state = "left"
                feedback.append("Good! Now look right")
            else:
                feedback.append("Now look right")
        elif offset > 0.08 and self.state == "left":
            self.rep_count += 1
            self.calories_burned += 0.2
            self.state = "start"
            self.base_values["center_x"] = shoulder_center_x
            feedback.append(f"Rep {self.rep_count}! Look left")
        elif offset > 0.08:
            feedback.append("Look left first")
        else:
            feedback.append("Look left or right")

        return feedback

    def detect_shoulder_shrug(self, landmarks):
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        current_y = (left_shoulder.y + right_shoulder.y) / 2

        feedback = []

        if "base_y" not in self.base_values:
            self.base_values["base_y"] = current_y
            feedback.append("Calibrated! Shrug up")
            return feedback

        delta = self.base_values["base_y"] - current_y

        if delta > 0.02:
            if self.state == "start":
                self.state = "up"
                feedback.append("Good! Lower down")
            else:
                feedback.append("Now lower down")
        elif delta < -0.01 and self.state == "up":
            self.rep_count += 1
            self.calories_burned += 0.3
            self.state = "start"
            self.base_values["base_y"] = current_y
            feedback.append(f"Rep {self.rep_count}! Shrug up")
        elif self.state == "up":
            feedback.append("Lower shoulders")
        else:
            feedback.append("Raise shoulders up")

        return feedback

    def detect_arm_raise(self, landmarks):
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]

        avg_shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
        avg_wrist_y = (left_wrist.y + right_wrist.y) / 2

        feedback = []

        if "base_y" not in self.base_values:
            self.base_values["base_y"] = avg_wrist_y
            feedback.append("Calibrated! Raise arms")
            return feedback

        if avg_wrist_y < avg_shoulder_y - 0.15:
            if self.state == "start":
                self.state = "up"
                feedback.append("Great! Lower down")
            else:
                feedback.append("Now lower down")
        elif avg_wrist_y > avg_shoulder_y + 0.1 and self.state == "up":
            self.rep_count += 1
            self.calories_burned += 0.4
            self.state = "start"
            self.base_values["base_y"] = avg_wrist_y
            feedback.append(f"Rep {self.rep_count}! Raise arms")
        elif self.state == "up":
            feedback.append("Lower arms slowly")
        else:
            feedback.append("Raise both arms up")

        return feedback

    def detect_wave_hand(self, landmarks):
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]

        feedback = []

        if "base_x" not in self.base_values:
            self.base_values["base_x"] = (left_wrist.x + right_wrist.x) / 2
            self.base_values["left_y"] = left_shoulder.y
            feedback.append("Calibrated! Wave one hand")
            return feedback

        left_wave = abs(left_wrist.x - self.base_values["base_x"])
        right_wave = abs(right_wrist.x - self.base_values["base_x"])

        if left_wave > 0.15 or right_wave > 0.15:
            if self.state == "start":
                self.state = "wave"
                self.base_values["wave_start"] = (
                    left_wrist.x if left_wave > right_wave else right_wrist.x
                )
                feedback.append("Good! Keep waving")
            elif self.state == "wave":
                self.base_values["wave_count"] = (
                    self.base_values.get("wave_count", 0) + 1
                )
                if self.base_values.get("wave_count", 0) >= 3:
                    self.rep_count += 1
                    self.calories_burned += 0.3
                    self.state = "start"
                    self.base_values = {
                        "base_x": (left_wrist.x + right_wrist.x) / 2,
                        "left_y": left_shoulder.y,
                    }
                    feedback.append(f"Rep {self.rep_count}! Wave again")
                else:
                    feedback.append(
                        f"Keep waving ({self.base_values.get('wave_count', 0)}/3)"
                    )
        else:
            if self.state == "wave" and self.base_values.get("wave_count", 0) < 3:
                self.base_values["wave_count"] = (
                    self.base_values.get("wave_count", 0) + 1
                )
                if self.base_values["wave_count"] >= 3:
                    self.rep_count += 1
                    self.calories_burned += 0.3
                    self.state = "start"
                    self.base_values = {
                        "base_x": (left_wrist.x + right_wrist.x) / 2,
                        "left_y": left_shoulder.y,
                    }
                    feedback.append(f"Rep {self.rep_count}! Wave again")
                else:
                    feedback.append(
                        f"Continue waving ({self.base_values['wave_count']}/3)"
                    )
            elif self.state == "start":
                feedback.append("Wave your hand!")
            else:
                feedback.append("Wave side to side")

        return feedback

    def detect_side_bend(self, landmarks):
        nose = landmarks[mp_pose.PoseLandmark.NOSE]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2

        feedback = []

        if "center_x" not in self.base_values:
            self.base_values["center_x"] = shoulder_center_x
            self.base_values["base_nose_x"] = nose.x
            feedback.append("Calibrated! Bend left")
            return feedback

        offset = nose.x - self.base_values["center_x"]

        if offset < -0.1:
            if self.state == "start":
                self.state = "left"
                feedback.append("Good! Now bend right")
            else:
                feedback.append("Now bend right")
        elif offset > 0.1 and self.state == "left":
            self.rep_count += 1
            self.calories_burned += 0.3
            self.state = "start"
            self.base_values["center_x"] = shoulder_center_x
            self.base_values["base_nose_x"] = nose.x
            feedback.append(f"Rep {self.rep_count}! Bend left")
        elif offset > 0.1:
            feedback.append("Bend left first")
        else:
            feedback.append("Bend to the sides")

        return feedback

    def detect_neck_tilt(self, landmarks):
        nose = landmarks[mp_pose.PoseLandmark.NOSE]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2

        feedback = []

        if "center_x" not in self.base_values:
            self.base_values["center_x"] = shoulder_center_x
            feedback.append("Calibrated! Tilt head left")
            return feedback

        offset = nose.x - self.base_values["center_x"]

        if offset < -0.06:
            if self.state == "start":
                self.state = "left"
                feedback.append("Good! Tilt right")
            else:
                feedback.append("Now tilt right")
        elif offset > 0.06 and self.state == "left":
            self.rep_count += 1
            self.calories_burned += 0.15
            self.state = "start"
            self.base_values["center_x"] = shoulder_center_x
            feedback.append(f"Rep {self.rep_count}! Tilt left")
        elif offset > 0.06:
            feedback.append("Tilt left first")
        else:
            feedback.append("Tilt head side to side")

        return feedback

    def detect_jaw_open(self, landmarks):
        nose = landmarks[mp_pose.PoseLandmark.NOSE]
        mouth_left = landmarks[mp_pose.PoseLandmark.MOUTH_LEFT]
        mouth_right = landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT]

        mouth_width = abs(mouth_right.x - mouth_left.x)

        feedback = []

        if "mouth_width" not in self.base_values:
            self.base_values["mouth_width"] = mouth_width
            feedback.append("Calibrated! Open mouth wide")
            return feedback

        delta = mouth_width - self.base_values["mouth_width"]

        if delta > 0.02:
            if self.state == "start":
                self.state = "open"
                feedback.append("Good! Close mouth")
            else:
                feedback.append("Now close")
        elif delta < -0.01 and self.state == "open":
            self.rep_count += 1
            self.calories_burned += 0.1
            self.state = "start"
            self.base_values["mouth_width"] = mouth_width
            feedback.append(f"Rep {self.rep_count}! Open mouth")
        elif self.state == "open":
            feedback.append("Close mouth")
        else:
            feedback.append("Open mouth wide")

        return feedback

    def detect_eye_movement(self, landmarks):
        nose = landmarks[mp_pose.PoseLandmark.NOSE]
        left_eye = landmarks[mp_pose.PoseLandmark.LEFT_EYE]
        right_eye = landmarks[mp_pose.PoseLandmark.RIGHT_EYE]

        eye_center_x = (left_eye.x + right_eye.x) / 2

        feedback = []

        if "eye_center" not in self.base_values:
            self.base_values["eye_center"] = eye_center_x
            feedback.append("Calibrated! Look left")
            return feedback

        offset = nose.x - self.base_values["eye_center"]

        if offset < -0.05:
            if self.state == "start":
                self.state = "left"
                feedback.append("Good! Look right")
            else:
                feedback.append("Now look right")
        elif offset > 0.05 and self.state == "left":
            self.rep_count += 1
            self.calories_burned += 0.1
            self.state = "start"
            self.base_values["eye_center"] = eye_center_x
            feedback.append(f"Rep {self.rep_count}! Look left")
        elif offset > 0.05:
            feedback.append("Look left first")
        else:
            feedback.append("Move eyes side to side")

        return feedback

    def detect_hand_clap(self, landmarks):
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]

        distance = abs(left_wrist.x - right_wrist.x)

        feedback = []

        if "clap_dist" not in self.base_values:
            self.base_values["clap_dist"] = distance
            feedback.append("Calibrated! Clap hands")
            return feedback

        if distance < 0.08:
            if self.state == "start":
                self.state = "clap"
                self.base_values["clap_count"] = 1
                feedback.append("Clap!")
            else:
                self.base_values["clap_count"] = (
                    self.base_values.get("clap_count", 0) + 1
                )
                if self.base_values["clap_count"] >= 3:
                    self.rep_count += 1
                    self.calories_burned += 0.3
                    self.state = "start"
                    self.base_values["clap_dist"] = distance
                    feedback.append(f"Rep {self.rep_count}! Clap again")
                else:
                    feedback.append(
                        f"Keep clapping ({self.base_values['clap_count']}/3)"
                    )
        else:
            if self.state == "clap" and self.base_values.get("clap_count", 0) < 3:
                self.base_values["clap_count"] = (
                    self.base_values.get("clap_count", 0) + 1
                )
                if self.base_values["clap_count"] >= 3:
                    self.rep_count += 1
                    self.calories_burned += 0.3
                    self.state = "start"
                    self.base_values["clap_dist"] = distance
                    feedback.append(f"Rep {self.rep_count}! Clap again")
                else:
                    feedback.append(f"Continue ({self.base_values['clap_count']}/3)")
            elif self.state == "start":
                feedback.append("Bring hands together!")
            else:
                feedback.append("Clap hands")

        return feedback

    def detect_finger_touch(self, landmarks):
        left_index = landmarks[mp_pose.PoseLandmark.LEFT_INDEX]
        right_index = landmarks[mp_pose.PoseLandmark.RIGHT_INDEX]
        nose = landmarks[mp_pose.PoseLandmark.NOSE]

        left_touching = (
            abs(left_index.x - nose.x) < 0.08 and abs(left_index.y - nose.y) < 0.08
        )
        right_touching = (
            abs(right_index.x - nose.x) < 0.08 and abs(right_index.y - nose.y) < 0.08
        )

        feedback = []

        if "nose_pos" not in self.base_values:
            self.base_values["nose_pos"] = (nose.x, nose.y)
            feedback.append("Calibrated! Touch nose with finger")
            return feedback

        if left_touching or right_touching:
            if self.state == "start":
                self.state = "touch"
                feedback.append("Good! Remove finger")
            else:
                feedback.append("Remove finger")
        elif self.state == "touch" and not left_touching and not right_touching:
            self.rep_count += 1
            self.calories_burned += 0.2
            self.state = "start"
            self.base_values["nose_pos"] = (nose.x, nose.y)
            feedback.append(f"Rep {self.rep_count}! Touch again")
        elif self.state == "touch":
            feedback.append("Remove finger from nose")
        else:
            feedback.append("Touch nose with finger")

        return feedback

    def detect_neck_rotation(self, landmarks):
        nose = landmarks[mp_pose.PoseLandmark.NOSE]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2

        feedback = []

        if "center_x" not in self.base_values:
            self.base_values["center_x"] = shoulder_center_x
            feedback.append("Calibrated! Rotate neck left")
            return feedback

        offset = nose.x - self.base_values["center_x"]

        if offset < -0.1:
            if self.state == "start":
                self.state = "left"
                feedback.append("Good! Rotate right")
            else:
                feedback.append("Now rotate right")
        elif offset > 0.1 and self.state == "left":
            self.rep_count += 1
            self.calories_burned += 0.2
            self.state = "start"
            self.base_values["center_x"] = shoulder_center_x
            feedback.append(f"Rep {self.rep_count}! Rotate left")
        elif offset > 0.1:
            feedback.append("Rotate left first")
        else:
            feedback.append("Rotate neck in circles")

        return feedback

    def detect_squat(self, landmarks):
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]

        def calculate_angle(a, b, c):
            import numpy as np

            a = np.array([a.x, a.y])
            b = np.array([b.x, b.y])
            c = np.array([c.x, c.y])
            radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
                a[1] - b[1], a[0] - b[0]
            )
            angle = np.abs(np.degrees(radians))
            if angle > 180:
                angle = 360 - angle
            return angle

        angle = calculate_angle(left_hip, left_knee, left_ankle)

        feedback = []

        if "squat_angle" not in self.base_values:
            self.base_values["squat_angle"] = 170
            feedback.append("Calibrated! Start squat")
            return feedback

        if angle < 100:
            if self.state == "start":
                self.state = "down"
                feedback.append("Good! Stand up")
            else:
                feedback.append("Now stand up")
        elif angle > 160 and self.state == "down":
            self.rep_count += 1
            self.calories_burned += 0.5
            self.state = "start"
            feedback.append(f"Rep {self.rep_count}! Squat again")
        elif self.state == "down":
            feedback.append("Stand up completely")
        else:
            feedback.append("Squat down")

        return feedback

    def detect_pushup(self, landmarks):
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]

        def calculate_angle(a, b, c):
            import numpy as np

            a = np.array([a.x, a.y])
            b = np.array([b.x, b.y])
            c = np.array([c.x, c.y])
            radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
                a[1] - b[1], a[0] - b[0]
            )
            angle = np.abs(np.degrees(radians))
            if angle > 180:
                angle = 360 - angle
            return angle

        angle = calculate_angle(left_shoulder, left_elbow, left_wrist)

        feedback = []

        if "pushup_angle" not in self.base_values:
            self.base_values["pushup_angle"] = 170
            feedback.append("Calibrated! Start pushup")
            return feedback

        if angle < 80:
            if self.state == "start":
                self.state = "down"
                feedback.append("Good! Push up")
            else:
                feedback.append("Now push up")
        elif angle > 160 and self.state == "down":
            self.rep_count += 1
            self.calories_burned += 0.6
            self.state = "start"
            feedback.append(f"Rep {self.rep_count}! Do another")
        elif self.state == "down":
            feedback.append("Push up completely")
        else:
            feedback.append("Lower down")

        return feedback

    def detect_jumping_jack(self, landmarks):
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
        right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]

        wrist_distance = abs(right_wrist.x - left_wrist.x)
        ankle_distance = abs(right_ankle.x - left_ankle.x)

        feedback = []

        if "jj_base" not in self.base_values:
            self.base_values["jj_base"] = {"wrist": 0.2, "ankle": 0.15}
            feedback.append("Calibrated! Start jumping jack")
            return feedback

        if wrist_distance > 0.5 and ankle_distance > 0.3:
            if self.state == "start":
                self.state = "up"
                feedback.append("Great! Return to start")
            else:
                feedback.append("Return to start")
        elif wrist_distance < 0.2 and ankle_distance < 0.15 and self.state == "up":
            self.rep_count += 1
            self.calories_burned += 0.4
            self.state = "start"
            feedback.append(f"Rep {self.rep_count}! Jump again")
        elif self.state == "up":
            feedback.append("Stand with arms down")
        else:
            feedback.append("Jump and spread arms!")

        return feedback

    def process_frame(self, frame):
        if not MEDIAPIPE_AVAILABLE or self.pose is None:
            cv2.putText(
                frame,
                "MediaPipe not available",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
            )
            return frame

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)

        self.form_feedback = []

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2),
            )
            landmarks = results.pose_landmarks.landmark
            self.form_feedback = self.detect_exercise(landmarks)
        else:
            self.form_feedback = ["No person detected!"]

        cv2.putText(
            frame,
            f"Reps: {self.rep_count}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )
        cv2.putText(
            frame,
            self.exercise.replace("_", " ").title(),
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )
        cv2.putText(
            frame,
            f"Cal: {self.calories_burned:.1f}",
            (10, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2,
        )

        return frame

    def reset(self):
        self.rep_count = 0
        self.base_values = {}
        self.calories_burned = 0
        self.state = "start"
        self.form_feedback = ["Reset! Stand in frame"]

    def get_stats(self):
        return {
            "rep_count": self.rep_count,
            "exercise": self.exercise,
            "calories_burned": round(self.calories_burned, 1),
            "form_feedback": self.form_feedback
            if self.form_feedback
            else ["Stand in frame"],
        }


detector = WorkoutDetector()
