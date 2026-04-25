import os
import sys
import cv2
import rospy
import rosbag
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

def create_stereo_rosbag(dataset_dir, output_bag):
    left_images_dir = os.path.join(dataset_dir, 'left')
    right_images_dir = os.path.join(dataset_dir, 'right')

    left_image_files = sorted(os.listdir(left_images_dir))
    right_image_files = sorted(os.listdir(right_images_dir))

    if len(left_image_files) != len(right_image_files):
        raise ValueError("The number of left and right images do not match")

    bag = rosbag.Bag(output_bag, 'w')
    bridge = CvBridge()

    first_timestamp = None

    for left_image_file, right_image_file in zip(left_image_files, right_image_files):
        left_timestamp = int(left_image_file.split('.')[0])
        right_timestamp = int(right_image_file.split('.')[0])

        if left_timestamp != right_timestamp:
            raise ValueError(f"Timestamps do not match: {left_image_file}, {right_image_file}")

        if first_timestamp is None:
            first_timestamp = left_timestamp

        # Calculate time since start
        timestamp_sec = (left_timestamp - first_timestamp) // 1000000
        timestamp_nsec = ((left_timestamp - first_timestamp) % 1000000) * 1000

        # Read left image
        left_image_path = os.path.join(left_images_dir, left_image_file)
        left_image = cv2.imread(left_image_path, cv2.IMREAD_GRAYSCALE)
        left_image_msg = bridge.cv2_to_imgmsg(left_image, encoding="mono8")
        left_image_msg.header.stamp.secs = timestamp_sec
        left_image_msg.header.stamp.nsecs = timestamp_nsec
        left_image_msg.header.frame_id = 'left_camera'
        bag.write('/camera/left/image_raw', left_image_msg, left_image_msg.header.stamp)

        # Read right image
        right_image_path = os.path.join(right_images_dir, right_image_file)
        right_image = cv2.imread(right_image_path, cv2.IMREAD_GRAYSCALE)
        right_image_msg = bridge.cv2_to_imgmsg(right_image, encoding="mono8")
        right_image_msg.header.stamp.secs = timestamp_sec
        right_image_msg.header.stamp.nsecs = timestamp_nsec
        right_image_msg.header.frame_id = 'right_camera'
        bag.write('/camera/right/image_raw', right_image_msg, right_image_msg.header.stamp)

    bag.close()
    print(f"Bag file created: {output_bag}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <dataset_directory> <output_bag>")
        sys.exit(1)

    dataset_dir = sys.argv[1]
    output_bag = sys.argv[2]

    create_stereo_rosbag(dataset_dir, output_bag)

