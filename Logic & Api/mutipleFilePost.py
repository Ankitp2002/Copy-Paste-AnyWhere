from flas_file_api import request,send_file,app ,Fernet,os
import tarfile
import gzip
from sqlAlchemyDb import *


def multipleFilePost(files_list,uniq_name,decodeToken):

    for keys in files_list:
        
        # files = request.files[keys]
        
        keys.save(f"uploadFile/{keys.filename}")

        # ========================================file encrypt===========================

        with open(f"uploadFile/{keys.filename}", 'rb') as file:
            encryptdata = file.read()

        key = Fernet(b'Tvo-DHOLOxFvRpEZwvtu1eUt3L5seBuE6yfapa2W5dA=')

        encrypytFile = key.encrypt(encryptdata)

        # --------------------------------------------------------------------------------------

        # =====================================remove normal file==============================

        os.remove(f"uploadFile/{keys.filename}")

        # ----------------------------------------------------------------------------------------

        # =====================================encrypt file save ================================

        with open(f"uploadFile/{keys.filename}", 'wb') as fileSave:
            fileSave.write(encrypytFile)

        # -----------------------------------------------------------------------------------------

        # =========================================compress file ==================================

        with open(f"uploadFile/{keys.filename}", 'rb') as binaryfile:
            with gzip.open(f"uploadFile/{keys.filename}.gz", 'wb') as compressFile:
                compressFile.writelines(binaryfile)

        # --------------------------------------------------------------------------------------------

        # =====================================encrypt file remove====================================

        os.remove(f"uploadFile/{keys.filename}")

        # -------------------------------------------------------------------------------------------

        # ==================================add file to tar file =====================================

        with tarfile.open(f"uploadFile/{uniq_name}.tar.gz", 'a') as fileAdd:
            fileAdd.add(f"uploadFile/{keys.filename}.gz")

        # --------------------------------------------------------------------------------------------

        # ================================================remove gzip file=============================

        os.remove(f"uploadFile/{keys.filename}.gz")

        # ------------------------------------------------------------------------------------------------

    dbStore = FileOpration(token=uniq_name, fileName=f"{uniq_name}.tar.gz",userName = decodeToken['name'] , userEmail = decodeToken['email'])

    Session.add(dbStore)
    Session.commit()
    Session.close()

    return {"token":uniq_name}
