import shutil
import os 

class DataTo30Classes:
    NAME    =   [
        "ando",
        "uemura",
        "enomaru",
        "ooshima",
        "mizuki",
        "okamura",
        "kataoka",
        "kodama",
        "shinohara",
        "suetomo",
        "takemoto",
        "tamejima",
        "nagao",
        "hamada",
        "masuda",
        "matuzaki",
        "miyatake",
        "soushi",
        "ryuuga",
        "yamaji",
        "yamashita",
        "wada",
        "watanabe",
        "teppei",
        "kawano",
        "higashi",
        "tutiyama",
        "toriyabe",
        "matui",
        "ishino",
    ]
    CLASSES =   [
        [] for i in NAME
    ]

    def __init__(self,rootDir,saveDir):
        self.__classification(rootDir=rootDir)
        self.__save(rootDir,saveDir)


    def __classification(self,rootDir):
        name_list   =   os.listdir(rootDir)
        
        for i,classes in enumerate(self.NAME):
            tmp_list    =   []
            for n in name_list:
                try:
                    if classes[0]+classes[1]+classes[2]+classes[3]+classes[4]+classes[5] == n[0]+n[1]+n[2]+n[3]+n[4]+n[5]:
                        tmp_list.append(n)
                except IndexError:
                    if classes[0]+classes[1]+classes[2]+classes[3] == n[0]+n[1]+n[2]+n[3]:
                        tmp_list.append(n)
            self.CLASSES[i] =   tmp_list
        
        # for c in self.CLASSES:
        #     print(c)

    def __save(self,rootDir,saveDir):
        #####   -----   親ディレクトリ作成    -----   #####
        try:
            os.makedirs(saveDir)
        except FileExistsError:
            pass 
        for i,c in enumerate(self.NAME):
            #####   -----   子ディレクトリ作成    -----   #####
            try:
                os.makedirs(saveDir+c+"/")
            except FileExistsError:
                pass 
            # print(self.CLASSES[i])
            # print(len(self.CLASSES[i]))
            # print(saveDir+c+"/")

            cnt     =   0

            for subDirName in self.CLASSES[i]:
                # print(subDirName)
                # print(rootDir+subDirName+"/")
                for f in os.listdir(rootDir+subDirName+"/"):
                    path = rootDir+subDirName+"/"+f
                    # print(path)
                    # print(saveDir+c+"/"+f)
                    # print(cnt)
                    shutil.copyfile(path,saveDir+c+"/"+str(cnt)+".jpg")
                    cnt += 1
                pass 
        
            



if __name__ == "__main__":
    # d   =   DataTo30Classes(rootDir="dataset_class_1/",saveDir="dataset/")
    e   =   DataTo30Classes(rootDir="dataset/",saveDir="test/")