from flas_file_api import request,Fernet , make_response,cross,cors,send_file
import os
import gzip
from sqlAlchemyDb import *
import shutil
import cryptography


def getSingalFiles(fileData,encryptFileName):

    # ===============================Singal file get=========================================

    # encryptFileName = ".".join(data)
    
    # ==================================decommpose gzip file==================

    with gzip.open(f"uploadFile/{fileData}", 'rb') as decommpostFile:
        with open(f"uploadFile/{encryptFileName}", 'wb') as encryptFile:
            shutil.copyfileobj(decommpostFile, encryptFile)

    # ==========================remove gzip file ===============

    # os.remove(f"uploadFile/{fileData}")

    # ============================decrypt file ================================

    key = Fernet(b'Tvo-DHOLOxFvRpEZwvtu1eUt3L5seBuE6yfapa2W5dA=')

    with open(f"uploadFile/{encryptFileName}", 'rb') as decryptFile:
        data = decryptFile.read()

    decryptedFile = key.decrypt(data)
    # ==========================remove encript file ===============

    # os.remove(f"uploadFile/{encryptFileName}")
    # ===============================orignalFile ========================

    with open(f"uploadFile/{encryptFileName}", 'wb') as finalFile:
        orignalData = finalFile.write(decryptedFile)

    # ---------------------------------------------------------------------------

    # dbStore = Session.query(FileOpration).filter(FileOpration.token == token).delete()
    #
    # Session.commit()
    # Session.close()
    return send_file(f"uploadFile/{encryptFileName}", as_attachment=True)
    # return make_response("send_from_directory(, encryptFileName, as_attachment=True)")

# getSingalFiles()