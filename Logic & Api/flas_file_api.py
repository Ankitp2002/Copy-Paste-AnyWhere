import time
from datetime import datetime , timedelta
import jwt
from flask import Flask ,request,send_file , send_from_directory,make_response,jsonify
from flask_restful import Resource ,Api
from sqlAlchemyDb import *
from cryptography.fernet import Fernet
import os
from flask_cors import CORS
import gzip
import shutil


app = Flask(__name__)

CORS(app)

cross = CORS(app , allow_headers="Access-Control-Allow-Origin" )

cors = CORS(app, resources={r"/*": {"Access-Control-Allow-Origin": "*"}})

api = Api(app)

class TokenValidation:

    @staticmethod
    def token(self):

        try:

            token = request.headers['token']
            tokendecode = jwt.decode(token,'SECRET_KEY', algorithms=['HS256'])
            userData = Session.query(Signup).filter(Signup.userEmail == tokendecode['email']).first()

            if userData is not None:

                return tokendecode

            else:

                return "Invalid Token or Token Is not Givern "

        except jwt.exceptions.InvalidTokenError or jwt.exceptions.InvalidSignatureError or TypeError :

            return "Invalid Token or Token Is not Givern "


class SingalfileUpload(Resource):

    def post(self):

        decodeToken = TokenValidation.token(self)
        print(decodeToken)
        if decodeToken == 'Invalid Token or Token Is not Givern ':

            return make_response(jsonify({"responce":"Invalid Token or Token Is not Givern "}))

        else:

            from singalUploadFile import singalFile

            # data =request.files.items()
            # for key, value in data:
            #     data = request.files[key]
            #     break
            #
            # uniq_name = str(datetime.now().timestamp()).replace(".", "")
            #
            # extanceFile = data.filename.split(".")
            #
            # data.save(f"uploadFile/{uniq_name}.{extanceFile[-1]}")
            #
            # # =======================================file encrypt =============================
            #
            # key = Fernet(b'Tvo-DHOLOxFvRpEZwvtu1eUt3L5seBuE6yfapa2W5dA=')
            #
            # with open(f"uploadFile/{uniq_name}.{extanceFile[-1]}", 'rb') as fileEncrypt:
            #     file = fileEncrypt.read()
            #
            # encrypt = key.encrypt(file)
            #
            # # =====================remove normal file===================
            #
            # os.remove(f"uploadFile/{uniq_name}.{extanceFile[-1]}")
            #
            # # ===========================encrypt file===========================
            #
            # with open(f"uploadFile/{uniq_name}.{extanceFile[-1]}", 'wb') as fileEncrypted:
            #     fileEncrypted.write(encrypt)
            #
            # # =============================compress file using Gzip===================
            #
            # with open(f"uploadFile/{uniq_name}.{extanceFile[-1]}", 'rb') as binaryData:
            #     with gzip.open(f"uploadFile/{uniq_name}.{extanceFile[-1]}.gz", 'wb') as compressFile:
            #         compressFile.writelines(binaryData)
            #
            # # =====================remove encrypt file===================
            #
            # os.remove(f"uploadFile/{uniq_name}.{extanceFile[-1]}")
            #
            # dbStore = FileOpration(token=uniq_name, fileName=f"{uniq_name}.{extanceFile[-1]}.gz")
            #
            # Session.add(dbStore)
            # Session.commit()
            # Session.close()
            #
            # information = (f"{uniq_name}.{extanceFile[-1]}", uniq_name)
            #
            # # return information

            return make_response(jsonify(singalFile(decodeToken)))

class fileGet(Resource):

    def get(self,token):

        decodeToken = TokenValidation.token(self)

        time.sleep(1)

        if decodeToken == 'Invalid Token or Token Is not Givern ':

            return make_response(jsonify({"responce":"Invalid Token or Token Is not Givern "}))

        else:
            try:

                getDb = Session.query(FileOpration.fileName).filter(FileOpration.token == token).first()

                if getDb is None:
                    return make_response(jsonify("token is invalide"))
                else:

                    temp=getDb[0].split('.')

                    fielsData = []

                    if temp[1] == "tar" :

                        from multipleFileGet import multipleFileGet

                        responce = make_response("")
                        responce.headers['file'] = multipleFileGet(token,decodeToken)
                        return responce

            # ==================================multiple file get====================================

                        #
                        # data = tarfile.open(f'uploadFile/{token}.tar.gz','r')
                        #
                        # for value in data.getnames():
                        #
                        #     data.extract(path='E:/script_all_dna/Professional_codeing_practice/copyPasteApiFlask/ankit',member=value , numeric_owner=True)
                        #
                        #     temp = value.split('.')
                        #
                        #     encryptFileName = ".".join(temp[:-1])
                        #
                        #     # ====================================unzip file================================
                        #
                        #     with gzip.open(value, 'rb') as decommpostFile:
                        #
                        #         with open(encryptFileName, 'wb') as encryptFile:
                        #
                        #             shutil.copyfileobj(decommpostFile, encryptFile)
                        #
                        #      #==========================remove gz file ==========================
                        #
                        #     os.remove(value)
                        #
                        #     # ----------------------------decription-----------------------------------------
                        #
                        #     key = Fernet(b'Tvo-DHOLOxFvRpEZwvtu1eUt3L5seBuE6yfapa2W5dA=')
                        #
                        #     with open( encryptFileName , 'rb') as decryptFile:
                        #
                        #         decryptdata = decryptFile.read()
                        #
                        #     decryptedFile = key.decrypt(decryptdata)
                        #
                        #     # ==========================remove encript file ===============
                        #
                        #     os.remove(encryptFileName)
                        #
                        #     # ===============================orignalFile ========================
                        #
                        #     with open(encryptFileName, 'wb') as finalFile:
                        #
                        #         orignalData = finalFile.write(decryptedFile)
                        #
                        #     # ---------------------------------------------------------------------------
                        #     temp = encryptFileName.split('/')[1]
                        #
                        #     fielsData.append(temp)
                        #
                        # data.close()
                        #
                        # os.remove(f'uploadFile/{token}.tar.gz')
                        #
                        # dbStore = Session.query(FileOpration).filter(FileOpration.token == token).delete()
                        # Session.commit()
                        # Session.close()
                        #
                        # return fielsData

                    else:

                        from getSingalFile import getSingalFiles

                        fileData = temp[:-1]

                        encryptFileName = ".".join(fileData)

                        data = getDb[0]

                        fileSend = getSingalFiles(data,encryptFileName)

                        headerData = make_response(fileSend)
                        headerData.headers['fileName'] = encryptFileName
                        return headerData

            except :

                return make_response(jsonify("some this is wronge"))

    # ===============================Singal file get=========================================
    #             fileData = temp[:-1]
    #             encryptFileName = ".".join(fileData)
    #
    #         # ==================================decommpose gzip file==================
    #
    #             with gzip.open(f"uploadFile/{getDb[0]}",'rb') as decommpostFile:
    #
    #                  with open(f"uploadFile/{encryptFileName}",'wb') as encryptFile:
    #
    #                      shutil.copyfileobj(decommpostFile,encryptFile)
    #
    #             # ==========================remove gzip file ===============
    #
    #             # os.remove(f"uploadFile/{getDb[0]}")
    #
    #             # ============================decrypt file ================================
    #
    #             key = Fernet(b'Tvo-DHOLOxFvRpEZwvtu1eUt3L5seBuE6yfapa2W5dA=')
    #
    #             with open(f"uploadFile/{encryptFileName}",'rb') as decryptFile:
    #                 data = decryptFile.read()
    #
    #             decryptedFile = key.decrypt(data)
    #             # ==========================remove encript file ===============
    #
    #             os.remove(f"uploadFile/{encryptFileName}")
    #
    #             # ===============================orignalFile ========================
    #
    #             with open(f"uploadFile/{encryptFileName}",'wb') as finalFile:
    #
    #                 orignalData = finalFile.write(decryptedFile)
    #
    #             # ---------------------------------------------------------------------------
    #
    #
    #             # dbStore = Session.query(FileOpration).filter(FileOpration.token == token).delete()
    #             #
    #             # Session.commit()
    #             # Session.close()
    #
    #             # return send_from_directory("uploadFile/",encryptFileName,as_attachment=True)
    #             return send_file(f"uploadFile/{encryptFileName}",as_attachment=True)
    #
    # #
    #         except:
    # 
    #             return "Data Not Found"



class MultiplefileUpload(Resource):

    def post(self):

        decodeToken = TokenValidation.token(self)

        if decodeToken == 'Invalid Token or Token Is not Givern ':

            return make_response(jsonify({"responce":"Invalid Token or Token Is not Givern "}))

        else:
            files = request.files.getlist('file')
            
            uniq_name = str(datetime.now().timestamp()).replace(".", "")
            
            from mutipleFilePost import multipleFilePost

            return make_response(jsonify(multipleFilePost(files,uniq_name,decodeToken)))

            # for keys,value in files:
        # 
        #     files = request.files[keys]
        # 
        #     files.save(f"uploadFile/{files.filename}")
        # 
        #     # ========================================file encrypt===========================
        # 
        #     with open(f"uploadFile/{files.filename}" , 'rb') as file:
        #         encryptdata = file.read()
        # 
        #     key = Fernet(b'Tvo-DHOLOxFvRpEZwvtu1eUt3L5seBuE6yfapa2W5dA=')
        # 
        #     encrypytFile = key.encrypt(encryptdata)
        # 
        #     # --------------------------------------------------------------------------------------
        # 
        #     # =====================================remove normal file==============================
        # 
        #     os.remove(f"uploadFile/{files.filename}")
        # 
        #     # ----------------------------------------------------------------------------------------
        # 
        #     # =====================================encrypt file save ================================
        # 
        #     with open(f"uploadFile/{files.filename}" , 'wb') as fileSave:
        # 
        #         fileSave.write(encrypytFile)
        # 
        #     # -----------------------------------------------------------------------------------------
        # 
        #     # =========================================compress file ==================================
        # 
        #     with open(f"uploadFile/{files.filename}",'rb') as binaryfile:
        # 
        #         with gzip.open(f"uploadFile/{files.filename}.gz",'wb') as compressFile:
        # 
        #             compressFile.writelines(binaryfile)
        # 
        #     # --------------------------------------------------------------------------------------------
        # 
        #     # =====================================encrypt file remove====================================
        # 
        #     os.remove(f"uploadFile/{files.filename}")
        # 
        #     # -------------------------------------------------------------------------------------------
        # 
        #     # ==================================add file to tar file =====================================
        # 
        #     with tarfile.open(f"uploadFile/{uniq_name}.tar.gz",'a') as fileAdd:
        # 
        #         fileAdd.add(f"uploadFile/{files.filename}.gz")
        # 
        #     # --------------------------------------------------------------------------------------------
        # 
        #     # ================================================remove gzip file=============================
        # 
        #     os.remove(f"uploadFile/{files.filename}.gz")
        # 
        #     # ------------------------------------------------------------------------------------------------
        # 
        # dbStore = FileOpration(token=uniq_name, fileName=f"{uniq_name}.tar.gz")
        # 
        # 
        # Session.add(dbStore)
        # Session.commit()
        # Session.close()
        # 
        # return  uniq_name

class home(Resource):

    def get(self):

        return "succesfuly"


class multipleFileGet(Resource):

    def get(self,filename):

        decodeToken = TokenValidation.token(self)

        if decodeToken == 'Invalid Token or Token Is not Givern':

            return make_response(jsonify({"responce":"Invalid Token or Token Is not Givern"}))

        else:
            try:

                responce =  make_response(send_file(f'uploadFile/{filename}', as_attachment = True))

                responce.headers['fileName'] = filename
                # dbStore = Session.query(UserFiles).filter(UserFiles.fileName == filename).delete()
                #
                # Session.commit()
                # Session.close()

                return responce
            except:

                 make_response(jsonify("Data Not Available!"))

@app.route('/filesDelete/<string:fileName>',methods=['GET'])
def delete_file(fileName):

    decodeToken = TokenValidation.token(self)

    if decodeToken == 'Invalid Token or Token Is not Givern':

        return make_response(jsonify({"responce": "Invalid Token or Token Is not Givern"}))

    else:
        os.remove(f'uploadFile/{fileName}')

        return "Delete succesfully"

class SignupUser(Resource):

    def post(self):

        userName = request.json['userName']
        userEmail = request.json['userEmail']
        userPassword = request.json['userPassword']

        data = Signup(userName=userName ,userEmail=userEmail,userPassword=userPassword)

        Session.add(data)
        Session.commit()

        return make_response(jsonify({"responce":"successfully signup","status" : True }))


@app.route('/login',methods=['POST'])
def login():

    userEmail = request.json['userEmail']
    userPassword = request.json['userPassword']

    check = Session.query(Signup).filter(Signup.userEmail == userEmail , Signup.userPassword == userPassword).first()

    if check is None:

        return make_response(jsonify({"Failed":"Check your credetial !!!!","status":False}))


    else:

        exp_time = int((datetime.now() + timedelta(minutes=30)).timestamp())

        payload = {

            "name": check.userName,
            "email": check.userEmail,
            "expTime": exp_time

        }

        token = jwt.encode(payload, 'SECRET_KEY', algorithm="HS256")

        return make_response(jsonify({"token": token, "status": True}))


class Profile(Resource):

    def get(self):

        decodeToken = TokenValidation.token(self)

        return make_response(jsonify({"Name" : decodeToken['name'] , "Email" : decodeToken['email']}))
    
    
class UserFile(Resource):
    
    def get(self):
        
        decodeToken = TokenValidation.token(self)
        
        print(decodeToken)
        userData = Session.query(UserFiles).filter(UserFiles.userEmail == decodeToken['email'])
        
        files = [file.fileName for file in userData]


        return make_response(jsonify({"Name" : decodeToken['name'] , "Email" : decodeToken['email'],"Files" : files }))

    
        

api.add_resource(SingalfileUpload,'/uploadSingleFile')
api.add_resource(MultiplefileUpload,'/uploadMultipleFile')
api.add_resource(fileGet,'/get/<token>')
api.add_resource(multipleFileGet,'/files/<filename>')
api.add_resource(SignupUser,'/signup')
api.add_resource(home,'/')
api.add_resource(Profile,'/profile')
api.add_resource(UserFile,'/UserFile')

if __name__ == '__main__':
    
    # app.run(host='',port='3000',debug=True)
    
    app.run(debug=True  )