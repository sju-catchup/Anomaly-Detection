import os
import sys
import argparse
import shutil

import xml.etree.ElementTree as elemTree
from datetime import datetime, timedelta

def parse_args():
    parser = argparse.ArgumentParser(description="Trim Video.")
    parser.add_argument('-s', '--src_path', required=True, type=str, help="Input your video and XML folder name(path)")
    parser.add_argument('-d', '--dst_path', required=True, type=str, help="Input destination folder paths to save results.")
    args = parser.parse_args()
    return args

def main(args):
    
    if not os.path.exists(args.dst_path):
        os.makedirs(args.dst_path)

    file_list = os.listdir(args.src_path)
    video_list = [file for file in file_list if file.endswith(".mp4")]

    for video in video_list:
        video_path = args.src_path + '/' + video
        xml_path = args.src_path + '/' + video.rstrip('.mp4') + '.xml'

        tree = elemTree.parse(xml_path)
        event = tree.find('./event')
        category = event.find('eventname').text
        start_time = event.find('starttime').text.split('.')[0]
        duration = event.find('duration').text.split('.')[0]
        duration_list = list(map(int, duration.split(':')))
        starttime_list = list(map(int, start_time.split(':')))
        end_time = datetime.strptime(start_time, '%H:%M:%S') + timedelta(hours=duration_list[0], minutes=duration_list[1], seconds=duration_list[2])
        end_time = end_time.strftime('%H:%M:%S')

        output_video_path = args.dst_path + '/' + video
        terminal_command = f"ffmpeg -i {video_path} -ss {start_time} -to {end_time} -vcodec copy -acodec copy {output_video_path}"
        os.system(terminal_command)

        # XML 수정 및 저장
        output_xml = args.dst_path + '/' + video.rstrip('.mp4') + '.xml'
        shutil.copyfile(xml_path, output_xml)

        tree_output = elemTree.parse(output_xml)
        root = tree_output.getroot()
        root.find('./header/duration').text = duration
        fps = int(root.find('./header/fps').text)
        root.find('./header/frames').text = str(fps * ((duration_list[0] * 360) + (duration_list[1] * 60) + duration_list[2]))
        root.find('./event/starttime').text = "00:00:00"

        origin_start_frame = fps * ((starttime_list[0] * 360) + starttime_list[1] * 60 + starttime_list[2])
        for person in root.findall('./object'):
            person.find('position/keyframe').text = str(int(person.find('position/keyframe').text) - origin_start_frame)
            
            for action in person.findall('action'):
                action.find('frame/start').text = str(int(action.find('frame/start').text) - origin_start_frame)
                action.find('frame/end').text = str(int(action.find('frame/end').text) - origin_start_frame)

        tree_output.write(output_xml, encoding='UTF-8', xml_declaration=True)
        

if __name__ == '__main__':
    args = parse_args()
    main(args)