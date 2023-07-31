import argparse
import lane_detection
import matplotlib.pyplot as plt
import cv2


def main(ip_address):
    vcap = cv2.VideoCapture(f"rtsp://{ip_address}:8554/rovcam")

    try:
        while True:
            # Obtain the frame
            ret, frame = vcap.read()

            # Check frame was received successfully
            if ret:
                print(" YOU GOT THIS ")
                # TODO: Do something with the frame here
                frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                lines = lane_detection.detect_lines(frame, 35, 60, 3, 200, 20)
                lines = lane_detection.rmvExcessLines(lines)
                lanes = lane_detection.detect_lanes(lines)
                img = lane_detection.draw_lanes(frame, lanes)
                plt.imshow(img)
                plt.show()
            else:
                pass

    except KeyboardInterrupt:
        # Close the connection
        vcap.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Network Stream Capture")
    parser.add_argument("--ip", type=str, help="IP Address of the Network Stream")
    args = parser.parse_args()

    main(args.ip)
