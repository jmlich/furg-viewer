#!/usr/bin/python3

import cv2
import sys
import argparse

def load_anots(filename, frames):

    xml = cv2.FileStorage(filename, cv2.FILE_STORAGE_READ)
    anot_data = {}
    counter = 0;

    xml_frames = xml.getNode("frames");
    for i in range(xml_frames.size()):
        frame = xml_frames.at(i)
        frameNumber = int(frame.getNode("frameNumber").real())
#        print("frameNumber", frameNumber)
        anots = frame.getNode("annotations")
        anot_data[frameNumber] = []

        for j in range (anots.size()):
            anot = anots.at(j)
            if anot.size() == 4:
                rect = (int(anot.at(0).real()), int(anot.at(1).real()), int(anot.at(2).real()), int(anot.at(3).real()))
                anot_data[frameNumber].append(rect)
                counter = counter + 1
#                print(rect)
            else:
                print("size:", anot.size(), anot.type())
    return anot_data, counter

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--video', type=str, default='/var/www/html/fire/data_furg-fire-dataset/hand_held_batteries_night.mp4',
        help='Video file')
    parser.add_argument('--xml', type=str, default='/var/www/html/fire/data_furg-fire-dataset/hand_held_batteries_night.xml',
        help='XML file')

    FLAGS, unparsed = parser.parse_known_args()

    cap = cv2.VideoCapture(FLAGS.video)
    anots, anots_num = load_anots(FLAGS.xml, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    print(anots_num)

    first_run = True

    frame_id = 0
    while(cap.isOpened()):
        ret, frame = cap.read()

        try:
            frame.shape
        except AttributeError:
            break


        rects = anots[frame_id]
        for rect in rects:
#            print(rect)
            frame = cv2.rectangle(frame, (rect[0],rect[1]), (rect[0] + rect[2], rect[1]+rect[3]), (255,0,0), 2)

#        if first_run:
#            first_run = False
#            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#            cvWriter = cv2.VideoWriter(output_video_fn, fourcc, 25.0, (frame.shape[1], frame.shape[0]))

        cv2.imshow('frame',frame)
#        cvWriter.write(frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break
        if key == ord(' ') or key == 27:
            key = cv2.waitKey(1000000) 
        frame_id = frame_id + 1;

    cap.release()
#    cvWriter.release()

#    cv2.destroyAllWindows()