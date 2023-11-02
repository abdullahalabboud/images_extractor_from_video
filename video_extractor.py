# extract images from included video on the python runner command

import cv2
import os
import sys
import pathlib
import logging


class VideoImagesExtractor:
    # constractor
    def __init__(self) -> None:
        self.current_path = os.getcwd()
        self.video_path: str
        self.video_name: str
        self.folder_name: str
        self.video_images_path = ""

        # Must be created video folder with name (videos) to work with multi videos
        self.multi_vidoes_folder_path = self.current_path + "/videos"

        # start program information
        print(
            "Program Started With Main Path".title() + f" {self.current_path}",
        )

    # check if folder video or not :
    def isVideo(self, video_path):
        import magic

        mime = magic.Magic(mime=True)
        filename = mime.from_file(video_path)
        # if file type is video
        if filename.find("video") != -1:
            print("it's a video")
            return True

        # esle not
        else:
            logging.error(f"your file is not video file type is : {filename}".title())
            return False

    # get video name from path
    def get_video_name(self):
        path, ext = os.path.splitext(self.video_path)
        self.video_name = pathlib.PurePath(path).name
        self.folder_name = self.video_name
        logging.info("vidoe name is : ".title() + f"({self.video_name})")

    # check if folder name is valid to create it or create another folder with valid name .
    def set_valid_foldername(self, folder_name: str):
        if folder_name + "_images" in os.listdir(self.current_path):
            folder_name = folder_name + "_"
            logging.error("You already have folder here .".title())

            # recursive
            self.set_valid_foldername(folder_name)
        else:
            self.folder_name = folder_name + "_images"

    # create new vidoe for video images with video name
    def open_new_folder(self):
        # check if folder name is valiabel or not :
        self.set_valid_foldername(self.folder_name)

        # create new folder
        os.mkdir(self.folder_name)
        logging.info(f"New Folder With Name :({self.folder_name}) Created .".title())

        # set video images path
        # Not : if not os.path.exists(folder_name):
        self.video_images_path = self.current_path + "/" + self.folder_name + "/"

    # ex
    def extraction_second(self, sec: int = 1, frame: int = 30) -> int:
        # by default extract every 1 seconds in 30 frame
        result = sec * frame
        if result != 0:
            return result
        else:
            return 1

    # extract video images method
    def extract_images(self, video_path: str):
        print(f"extrcted images in folder {self.video_images_path}")
        success = True
        count = 0
        image_counter = 0

        # set extraction seconds
        extraction_seconds = self.extraction_second(5)

        # print
        print(f"will extract video images every ({extraction_seconds})frame.".title())
        cap = cv2.VideoCapture(video_path)
        while success:
            success, image = cap.read()
            if (count % extraction_seconds) == 0:
                image_counter += 1
                image_name = f"{self.video_name}{image_counter}"
                cv2.imwrite(f"{self.video_images_path}{image_name}.jpg", image)

                # print
                print(f"wrote new image ({image_name})")

            count += 1

        # print
        print(f"extracted images count is : {image_counter}".title())
        print("extaction finished".title())
        image_counter = 0

    # run method
    def run(self, video_path: str):
        self.video_path = video_path  # used video path .

        # check if file is video to continue to extraction
        if self.isVideo(self.video_path):
            self.get_video_name()  # get video name
            self.open_new_folder()  # check folder name of video images folder and create valid vidoe images folder  .
            self.extract_images(video_path)  # extract images from video

    def check_video_folder(self, folder_path) -> str:
        if folder_path == None:
            return self.multi_vidoes_folder_path
        else:
            return folder_path

    # auto extraction for multi videos
    def run_multi(self, video_folder_path=None):
        # check video folder from where will be read or as auto will be work from (videos) folder in the main program path .
        folder_path = self.check_video_folder(video_folder_path)
        video_list = os.listdir(folder_path)
        for video in video_list:
            video_name = os.path.basename(video)
            print(
                f"\nwill start extract images from video ({folder_path}/{video_name})\n".title()
            )
            self.run(f"{folder_path}/{video_name}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.exception("Enter Video Path !".title())
    else:
        video_extractor = VideoImagesExtractor()
        # video_extractor.run(sys.argv[1]) # for one video
        # video_extractor.run_multi(sys.argv[1]) # for check videos folder from other folders
        video_extractor.run_multi()  # for check videos folder from same folder (videos) in our current path
        # logging.info(
        #     f"video images path now is : ${video_extractor.video_images_path}".title(),
        # )
