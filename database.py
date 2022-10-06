import pymongo

#Conexão Banco de dados mongodb
#Conection Database mongodb
class Database():
    def __init__(self):
        #Conexão com o Cluster mongodb
        #Conection Cluster mongodb
        self.cluster = pymongo.MongoClient(
            "mongodb+srv://cluster0.ty1glmi.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority",
            tls = True,
            tlsCertificateKeyFile = 'token/X509-cert-2817312730614208270.pem'
        )
        self.db = self.cluster["Cluster0"]
        #Conexão com o Db users
        #Conection Db users
        self.collection = self.db["users"]

    def isUserNameExists(self, un):
        if self.collection.find_one({"username": un}) != None:
            return True
        return False

    def isAccountExists(self, un, pw):
        try:
            if self.isUserNameExists(un) == True:
                userDetails = self.collection.find({"username": un})
                for detail in userDetails:
                    matchPassword = detail["password"]
                if matchPassword == pw:
                    return True
            else:
                return False
        except Exception as e:
            print(e)

    def createAccount(self, un, pw):
        try:
            if self.isUserNameExists(un) == True:
                return "Username Exists"
            else:
                details = {"username": un, "password": pw}
                self.collection.insert_one(details)
                return "account Created"
        except Exception as e:
            print(e)

    def deleteAccount(self, un, pw):
        self.collection.delete_one({"username": un, "password": pw})
        return "Account Deleted"
