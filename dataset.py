import cv2 
import os 

class MakeDataset:
    CAP_CHANNEL         =   0
    WINDOW_WIDTH        =   1920
    WINDOW_HEIGHT       =   1080
    IMSHOW_WINDOW_W     =   720
    IMSHOW_WINDOW_H     =   480
    FRAME_WIDTH         =   600
    FRAME_HEIGHT        =   600

    CASCADEPATH         =   "haarcascades/haarcascade_frontalface_default.xml"

    ROOT_DIR            =   "dataset_class/"

    DATA_MAX            =   200
    CLASSES             =   5
    COLOR               =   (255,0,255)
    FILE_CNT_MAX        =   200
    MOJI_OOKISA         =   1.0
    PROGRESS_BAR_LEN    =   200

    def __init__(self):
        #   カメラの初期化
        self.cap        =   cv2.VideoCapture(self.CAP_CHANNEL)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,   self.WINDOW_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,  self.WINDOW_HEIGHT)

        #   haar-likeカスケード特徴分類器
        self.cascade    =   cv2.CascadeClassifier(self.CASCADEPATH)
        
        self.__askClasses()
        self.__askName()

        pass 

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
        print("Thank you!")

    def __makeDir(self,path):
        #   個別データセットPATH
        try:
            os.makedirs(path)
        except FileExistsError:
            pass 

    def __askName(self):
        for i in range(0,int(self.CLASSES)):
            print("name :",end="")
            name    =   input()

            path    =   self.ROOT_DIR+str(name)+"/"
            #   ディレクトリを作る
            self.__makeDir(path)

            #   データセットを作る
            self.__make_dataset(name,path)
        pass 

    def __askClasses(self):
        print("Classes  :",end="")
        self.CLASSES    =   input()

    def __make_dataset(self,name,path):
        cnt     =   0
        isEnd   =   0

        while True:
            success,img =   self.cap.read()
            try:
                imgGray     =   cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            except cv2.error:
                self.CAP_CHANNEL    ^=  1
                self.cap    =   cv2.VideoCapture(self.CAP_CHANNEL)
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,   self.WINDOW_WIDTH)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,  self.WINDOW_HEIGHT)
                success,img =   self.cap.read()
                imgGray     = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            
            
            imgResult   =   img.copy()
            facerect    = self.cascade.detectMultiScale(imgGray,scaleFactor=1.1,minNeighbors=2,minSize=(200,200))
            H,W,C = img.shape
            self.x = int((W - self.FRAME_WIDTH)/2)
            self.y = int((H - self.FRAME_HEIGHT)/2)


            if len(facerect) > 0:
                for (x,y,w,h) in facerect:

                    imgTrim =   img[y:y+h,x:x+w]
                    cv2.imwrite(path+str(cnt)+".jpg",imgTrim)

                    cv2.rectangle(imgResult,(x,y),(x+w,y+h),self.COLOR,thickness=2)

                    cv2.rectangle(imgResult,(self.x,self.y),(self.x+self.FRAME_WIDTH,self.y+self.FRAME_HEIGHT),self.COLOR,thickness=10)
                    cv2.putText(imgResult,"Please wait.",(self.x+self.FRAME_WIDTH+40,int((self.y+self.FRAME_HEIGHT)/2)+40),cv2.FONT_HERSHEY_SIMPLEX,self.MOJI_OOKISA,self.COLOR,thickness=2)
                    cv2.putText(
                        imgResult,
                        str(int(self.PROGRESS_BAR_LEN/self.FILE_CNT_MAX*cnt/(self.FILE_CNT_MAX)*100))+"%",
                        (self.x+self.FRAME_WIDTH+40*2,int((self.y+self.FRAME_HEIGHT)/2)+40*2),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        self.MOJI_OOKISA,
                        self.COLOR,
                        thickness=2
                    )
                    cv2.line(
                        imgResult,
                        (self.x+self.FRAME_WIDTH+50,                        int((self.y+self.FRAME_HEIGHT)/2)+40*3),
                        (self.x+self.FRAME_WIDTH+50+self.PROGRESS_BAR_LEN,  int((self.y+self.FRAME_HEIGHT)/2)+40*3),
                        (204,204,204),
                        15
                    )
                    cv2.line(
                        imgResult,
                        (self.x+self.FRAME_WIDTH+50,                                                    int((self.y+self.FRAME_HEIGHT)/2)+40*3),
                        (self.x+self.FRAME_WIDTH+50+(int(self.PROGRESS_BAR_LEN/self.FILE_CNT_MAX))*cnt, int((self.y+self.FRAME_HEIGHT)/2)+40*3),
                        self.COLOR,
                        15
                    )
                    cv2.imshow("Image result",imgResult)
                    cv2.waitKey(1)

                    if cnt < self.FILE_CNT_MAX-1:
                        cnt += 1
                    else:
                        isEnd   =   1
            else:
                cv2.rectangle(imgResult,(self.x,self.y),(self.x+self.FRAME_WIDTH,self.y+self.FRAME_HEIGHT),self.COLOR,thickness=10)
                cv2.putText(imgResult, "Set Face", (40*2, 40*2), cv2.FONT_HERSHEY_SIMPLEX,self.MOJI_OOKISA*2,self.COLOR,thickness=4)
                cv2.imshow("Image result",imgResult)
                cv2.waitKey(1)
            
            #   終了
            if isEnd == 1:
                # cv2.destroyAllWindows()
                imgResult   =   img.copy()
                cv2.rectangle(imgResult,(self.x,self.y),(self.x+self.FRAME_WIDTH,self.y+self.FRAME_HEIGHT),self.COLOR,thickness=10)
                cv2.putText(imgResult,str(name)+" is complete.",(self.x+self.FRAME_WIDTH+40,int((self.y+self.FRAME_HEIGHT)/2)+40),cv2.FONT_HERSHEY_SIMPLEX,self.MOJI_OOKISA,self.COLOR,thickness=2)
                cv2.putText(
                    imgResult,
                    "100%",
                    (self.x+self.FRAME_WIDTH+40*2,int((self.y+self.FRAME_HEIGHT)/2)+40*2),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    self.MOJI_OOKISA,
                    self.COLOR,
                    thickness=2
                )
                cv2.line(
                    imgResult,
                    (self.x+self.FRAME_WIDTH+50,                        int((self.y+self.FRAME_HEIGHT)/2)+40*3),
                    (self.x+self.FRAME_WIDTH+50+self.PROGRESS_BAR_LEN,  int((self.y+self.FRAME_HEIGHT)/2)+40*3),
                    (204,204,204),
                    15
                )
                cv2.line(
                    imgResult,
                    (self.x+self.FRAME_WIDTH+50,                                                    int((self.y+self.FRAME_HEIGHT)/2)+40*3),
                    (self.x+self.FRAME_WIDTH+50+(int(self.PROGRESS_BAR_LEN/self.FILE_CNT_MAX))*cnt, int((self.y+self.FRAME_HEIGHT)/2)+40*3),
                    self.COLOR,
                    15
                )
                cv2.imshow("Image result",imgResult)
                cv2.waitKey(1)
                break


                    

    

if __name__ == "__main__":
    m   =   MakeDataset()