from flas_file_api import request,send_file,app , datetime,Fernet
import os
import tarfile
import gzip
from sqlAlchemyDb import *
import cryptography
import shutil

def multipleFileGet(token,decodeToken):
    
    data = tarfile.open(f'uploadFile/{token}.tar.gz', 'r')
    fielsData = []

    for value in data.getnames():
        data.extract(path='E:/script_all_dna/Professional_codeing_practice/copyPasteApiFlask/ankit', member=value,
                     numeric_owner=True)

        temp = value.split('.')

        encryptFileName = ".".join(temp[:-1])

        # ====================================unzip file================================

        with gzip.open(value, 'rb') as decommpostFile:
            with open(encryptFileName, 'wb') as encryptFile:
                shutil.copyfileobj(decommpostFile, encryptFile)

        # ==========================remove gz file ==========================

        os.remove(value)

        # ----------------------------decription-----------------------------------------

        key = Fernet(b'Tvo-DHOLOxFvRpEZwvtu1eUt3L5seBuE6yfapa2W5dA=')

        with open(encryptFileName, 'rb') as decryptFile:
            decryptdata = decryptFile.read()

        decryptedFile = key.decrypt(decryptdata)

        # ==========================remove encript file ===============

        os.remove(encryptFileName)

        # ===============================orignalFile ========================

        with open(encryptFileName, 'wb') as finalFile:
            orignalData = finalFile.write(decryptedFile)

        # ---------------------------------------------------------------------------
        temp = encryptFileName.split('/')[1]

        fielsData.append(temp)

        fileStore =UserFiles(fileName=temp ,userName = decodeToken['name'] , userEmail = decodeToken['email'] )

        Session.add(fileStore)
        Session.commit()

    data.close()
    Session.close()

    # os.remove(f'uploadFile/{token}.tar.gz')

    # dbStore = Session.query(FileOpration).filter(FileOpration.token == token).delete()
    # Session.commit()
    # Session.close()

    return fielsData
