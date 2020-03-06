#!/usr/bin/python3

import cv2
import argparse
from fireXMLStore import fireXMLStore

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--video', type=str, required=True, help='Video file')
    parser.add_argument('--xml', type=str, required=True, help='XML file')

    FLAGS, unparsed = parser.parse_known_args()

    cap = cv2.VideoCapture(FLAGS.video)

    xmlFIRE = fireXMLStore()
    anots, anots_num = xmlFIRE.load(FLAGS.xml)
    print(anots_num)

    # xmlwriter.sourceFileName = FLAGS.video

    first_run: bool = True

    frame_id = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        #xmlFIRE.setFrame(frame_id)

        if first_run:
            first_run = False
            # xmlwriter.sourceFrameRate = cap.get(cv2.CAP_PROP_FPS)
            # xmlwriter.sourceFrameWidth = frame.shape[1]
            # xmlwriter.sourceFrameHeight = frame.shape[0]

            # fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            # cvWriter = cv2.VideoWriter(output_video_fn, fourcc, 25.0, (frame.shape[1], frame.shape[0]))

        try:
            frame.shape
        except AttributeError:
            break

        rects = anots[frame_id]
        for rect in rects:
            # print(rect)
            frame = cv2.rectangle(frame, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (255, 0, 0), 2)
            #xmlFIRE.addBBox(rect[0], rect[1], rect[2], rect[3])

        cv2.imshow('frame', frame)
        # cvWriter.write(frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break
        if key == ord(' ') or key == 27:
            key = cv2.waitKey(1000000)
        frame_id = frame_id + 1

    cap.release()
    #xmlFIRE.save("filename.xml")
    # cvWriter.release()

    # cv2.destroyAllWindows()
