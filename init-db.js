db =db.getSiblingDB("agencia-turismo")

db.teste.drop()
db.teste.insert({"teste":"teste"})