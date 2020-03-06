#!/bin/bash

DIR=/var/www/html/fire/data_furg-fire-dataset

# ./show_furg.py --video $DIR/case2_car.mp4 --xml $DIR/case2_car.xml

./show_furg.py --video $DIR/hand_held_camera_wildfire.mp4 --xml $DIR/hand_held_camera_wildfire.xml
#./show_furg.py --video $DIR/hand_held_camera_wildfire.mp4 --xml ./filename.xml

cat filename.xml | xmllint --format - > filename2.xml

# case2_car.mp4-bbox.avi

