#!/usr/bin/python3

import datetime
from email import utils

import xml.etree.cElementTree as ET

class fireXMLStore():
    curFrame = 0
    data = {}
    sourceFileName = ""
    sourceFrameRate = 25
    sourceFrameWidth = 320
    sourceFrameHeight = 200

    def setFrame(self, f):
        self.curFrame = f
        self.data[f] = []

    def addBBox(self, x,y,w,h):
        self.data[self.curFrame].append((x,y,w,h))


    def save(self, filename):

        nowdt = datetime.datetime.now()
        rfcdate = utils.format_datetime(nowdt)

        root = ET.Element("opencv_storage")
        ET.SubElement(root, "fileName").text = self.sourceFileName
        ET.SubElement(root, "frameRate").text = str(self.sourceFrameRate)
        ET.SubElement(root, "shapeType").text = 'r'
        ET.SubElement(root, "frameWidth").text = str(self.sourceFrameWidth)
        ET.SubElement(root, "frameHeight").text = str(self.sourceFrameHeight)
        ET.SubElement(root, "dataSetDate").text = str(rfcdate)

        frames_el = ET.SubElement(root, "frames")

        for frameNum, anots in self.data.items():
            f_el = ET.SubElement(frames_el, "_")
            ET.SubElement(f_el, "frameNumber").text = str(frameNum)
            annots_el = ET.SubElement(f_el, "annotations")
            for anot in anots:
                ET.SubElement(annots_el,"_").text = str(anot[0]) + " " + str(anot[1]) + " " + str(anot[2]) + " " + str(anot[3])

        tree = ET.ElementTree(root)
        tree.write(filename)

    def load(self, filename):

        counter = 0
        tree = ET.parse(filename)
        root = tree.getroot()

        for child in root:
            if child.tag == "fileName":
                self.sourceFileName = child.text
            elif child.tag == "frameRate":
                self.sourceFrameRate = child.text
            #elif child.tag == "shapeType":
            elif child.tag == "frameWidth":
                self.sourceFrameWidth = child.text
            elif child.tag == "frameHeight":
                self.sourceFrameHeight = child.text
            # elif child.tag == "dataSetDate":
            elif child.tag == "frames":
                for frame in list(child):
                    frameNumber = None
                    annotations = []
                    for frameElement in frame:
                        if frameElement.tag == "frameNumber":
                            frameNumber = int(frameElement.text)
                        elif frameElement.tag == "annotations":
                            for anotSet in list(frameElement):
                                bbstr = anotSet.text.split()
                                bb = []
                                for n in bbstr:
                                    bb.append(int(n))
                                annotations.append(bb)
                                counter = counter + 1

                    self.data[frameNumber] = annotations

        return self.data, counter
