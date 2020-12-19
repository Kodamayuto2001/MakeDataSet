import os 


class DataCrean:
    def __init__(self):
        pass 
    def __del__(self):
        pass 

    def setDir(self,rootDir):
        self.rootDir    =   rootDir

    def test(self):
        nameList    =   os.listdir(self.rootDir)
        for name in nameList:
            self.__dataCrean(name) 

    def __dataCrean(self,name):
        mDir    =   self.rootDir    +name   +"/"
        tmpDir  =   mDir    +"tmp/"
        try:
            os.makedirs(tmpDir)
        except FileExistsError:
            pass 

        #   画像を読み込んで格納
        filelist    =   []
        for f in os.listdir(mDir):
            if os.path.isfile(os.path.join(mDir,f)):
                filelist.append(mDir+f)

        cnt = 0

        # tmpフォルダに保存
        for path in filelist:
            os.rename(path,mDir+"tmp/"+str(cnt)+".jpg")
            cnt += 1

        # 元のフォルダに移動
        cnt = 0
        for f in os.listdir(mDir+"tmp/"):
            os.rename(mDir+"tmp/"+f,mDir+str(cnt)+".jpg")
            cnt += 1

        # tmpフォルダの削除
        os.rmdir(mDir+"tmp/")

        print(mDir+"に保存されているファイル名を揃えました。")
        pass 

    



if __name__ == "__main__":
    d   =   DataCrean()
    d.setDir(rootDir="dataset_class_1/")
    d.test()
