from flas_file_api import request,send_file,app , datetime,Fernet,make_response,jsonify,cors,cross
import gzip
from sqlAlchemyDb import *
import cryptography
import os



def singalFile(decodeToken):

    try:

        data = request.files.items()

        for key, value in data:
            data = request.files[key]
            break

        uniq_name = str(datetime.now().timestamp()).replace(".", "")

        extanceFile = data.filename.split(".")

        data.save(f"uploadFile/{uniq_name}.{extanceFile[-1]}")

        # =======================================file encrypt =============================

        key = Fernet(b'Tvo-DHOLOxFvRpEZwvtu1eUt3L5seBuE6yfapa2W5dA=')

        with open(f"uploadFile/{uniq_name}.{extanceFile[-1]}", 'rb') as fileEncrypt:
            file = fileEncrypt.read()

        encrypt = key.encrypt(file)

        # =====================remove normal file===================

        os.remove(f"uploadFile/{uniq_name}.{extanceFile[-1]}")

        # ===========================encrypt file===========================

        with open(f"uploadFile/{uniq_name}.{extanceFile[-1]}", 'wb') as fileEncrypted:
            fileEncrypted.write(encrypt)

        # =============================compress file using Gzip===================

        with open(f"uploadFile/{uniq_name}.{extanceFile[-1]}", 'rb') as binaryData:
            with gzip.open(f"uploadFile/{uniq_name}.{extanceFile[-1]}.gz", 'wb') as compressFile:
                compressFile.writelines(binaryData)

        # =====================remove encrypt file===================

        os.remove(f"uploadFile/{uniq_name}.{extanceFile[-1]}")

        dbStore = FileOpration(token=uniq_name, fileName=f"{uniq_name}.{extanceFile[-1]}.gz" ,userName = decodeToken['name'] , userEmail = decodeToken['email'] )

        Session.add(dbStore)
        Session.commit()
        Session.close()

        information = ({"fileName" : f"{uniq_name}.{extanceFile[-1]}", "token" : uniq_name , "states" : True})

        return information

    except AttributeError or TypeError:

        return "data not upload"
