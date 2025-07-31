def fingers_state(lms):
    fingers = []

    fingers.append(lms[4].x < lms[3].x)  # left hand mirrored
    fingers.append(lms[8].y < lms[6].y)  # Index
    fingers.append(lms[12].y < lms[10].y)  # Middle
    fingers.append(lms[16].y < lms[14].y)  # Ring
    fingers.append(lms[20].y < lms[18].y)  # Pinky
    return fingers
