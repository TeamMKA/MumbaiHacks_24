import cv2
import numpy as np
import tensorflow as tf


model = tf.keras.models.load_model("model_checkpoint_mobilenetv2.keras")


def preprocess_frames(frames, target_size=(224, 224)):
    processed_frames = []
    for frame in frames:

        frame = cv2.resize(frame, target_size)
        frame = frame / 255.0
        processed_frames.append(frame)
    return np.expand_dims(np.array(processed_frames), axis=0)


def annotate_frame(frame, prediction, threshold=0.5):

    label = "Unsafe" if prediction > threshold else "Safe"
    # label = str(prediction)

    color = (0, 0, 255) if prediction > threshold else (0, 255, 0)

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2.5
    font_thickness = 4

    text_size, _ = cv2.getTextSize(label, font, font_scale, font_thickness)
    text_x, text_y = (
        10,
        80,
    )

    cv2.putText(
        frame,
        label,
        (text_x, text_y),
        font,
        font_scale,
        (255, 255, 255),
        font_thickness + 3,
        cv2.LINE_AA,
    )

    cv2.putText(
        frame,
        label,
        (text_x, text_y),
        font,
        font_scale,
        color,
        font_thickness,
        cv2.LINE_AA,
    )

    return frame


def process_video(input_video_path, output_video_path, num_frames=15):
    cap = cv2.VideoCapture(input_video_path)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = cap.get(cv2.CAP_PROP_FPS)
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    )
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

        if len(frames) == num_frames:

            processed_frames = preprocess_frames(frames)
            prediction = model.predict(processed_frames)[0][0]

            for i in range(num_frames):
                frames[i] = annotate_frame(frames[i], prediction)

            for annotated_frame in frames:
                out.write(annotated_frame)

            frames = []

    cap.release()
    out.release()
    print(f"Annotated video saved to {output_video_path}")


process_video("V_10.mp4", "V_10_output.mp4")
