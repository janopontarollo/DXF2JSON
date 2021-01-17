#!/usr/bin/python
#-*- coding: utf-8 -*-

# TU CONVETIS DANS LE DXF D'ENTREE
# LES POLYLINGUES, LES NOTES, LES BLOCS
# DANS LE JSON DE SORTIE

# LE FORMAT DU DXF  DOIT ETRE EN ASCII R2000-2002
# AVEC UN SYSTEME DE PROJECTION LB93


# Next Step : suprimer gliches dans les chaines 50%
# Next Step : Ajouter ++++ Couleurs

# Jano Pontarollo
# Call me on intagram @janopontarollo

import math
import pyfiglet

ListeCouleur = [ "ZERO" , "RED", "YELLO" , "GREEN" , "CYAN" , "BLUE" , "WHITE" , "WHITE" , "GRREY" , "GREY" ]


# ENTREES ET SORTIES
fii = "In.dxf"
foo = "Out.json"

i = 0
j = 0

LWPOLYLINE = 0
LINE = 0
CIRCLE = 0
MTEXT = 0
INSERT = 0
POINT = 0

# Tu copie le fichier d'entre dans la chaine LineDXF
DXF = open ( fii, "r")
LineDXF = DXF.readlines()
DXF.close()

# Tu encode toutes les lignes en ANSI (cp1252) vers UTF8
for n in range(0, len(LineDXF)):
	LineDXF[n] = LineDXF[n].decode("cp1252").encode("utf-8")

#Concatenation du JSON, les 5 premiere lignes
LineJSON = "{\n"
LineJSON = LineJSON + "\"type\": \"FeatureCollection\",\n"
LineJSON = LineJSON + "\"name\": \"DXF2JSON\",\n"
LineJSON = LineJSON + "\"crs\": { \"type\": \"name\", \"properties\": { \"name\": \"urn:ogc:def:crs:EPSG::2154\" } },\n"
LineJSON = LineJSON + "\"features\": [\n"


while LineDXF[i] + LineDXF[i+1] != "  0\nEOF\n":

	#SECTION
	if LineDXF[i] + LineDXF[i+1] == "  0\nSECTION\n":
		CadSECTION = LineDXF[i+3].strip()

    #LES POLYLINGUES
	if CadSECTION == "ENTITIES" and LineDXF[i] + LineDXF[i+1] == "  0\nLWPOLYLINE\n":
			
		j=i+2
		ListePointsX = ""
		ListePointsY = ""
		PythonLinePoints = ""
		Handle = ""
		LayerName = ""
		Flag = "0"
		Link = ""
		laCouleur = "BYLAYER"
		LWPOLYLINE = LWPOLYLINE + 1 
			
		while LineDXF[j] != "  0\n":
		
			if LineDXF[j] == "  5\n":										#LePointeur
				Handle = LineDXF[j+1].strip()

			if LineDXF[j] == "  8\n":										#LeCalque
				LayerName = LineDXF[j+1].strip()
				
			if LineDXF[j] == " 70\n":										#LeDrapeau
				# FLAG ( default: 0 , closed polyline: 1 )
				Flag = LineDXF[j+1].strip()
				
			if LineDXF[j] == " 10\n":										#X
				ListePointsX = ListePointsX + LineDXF[j+1].strip() + ";"

			if LineDXF[j] == " 20\n":										#Y
				ListePointsY = ListePointsY + LineDXF[j+1].strip() + ";"
				
			if LineDXF[j] == " 62\n":										#laCouleur
				if int(LineDXF[j+1].strip()) < 10:
					laCouleur = ListeCouleur[int(LineDXF[j+1].strip())]
				else:
					laCouleur = "#" + LineDXF[j+1].strip()

			if LineDXF[j] + LineDXF[j+1] + LineDXF[j+2] == "1001\nPE_URL\n1000\n":	#Link
				Link = "_" + LineDXF[j+3].strip() + "_"
				
			j = j + 2
			#Fin de ceuillette Mtext
			
		#tu split BasePointX
		arrayPointX = ListePointsX.split(";")
		#Tu split BasePointY
		arrayPointY = ListePointsY.split(";")

		#Concatenation du JSON
		LineJSON = LineJSON + "{ \"type\": \"Feature\", \"properties\": { \"ENTITIES\": \"LWPOLYLINE\", \"LayerName\": \"" + LayerName + "\", \"Handle\": \"" + Handle + "\", \"laCouleur\": \"" + laCouleur + "\", \"Link\": \"" + Link + "\" },\n"

		if Flag == "1":

				
			LineJSON = LineJSON + "     \"geometry\": { \"type\": \"Polygon\","
			LineJSON = LineJSON + "\"coordinates\": [[\n"
			
			for n in range(0, len(arrayPointX)-1):
				LineJSON = LineJSON + "     [" +arrayPointX[n]
				LineJSON = LineJSON +  "," + arrayPointY[n] + "],\n"

			LineJSON = LineJSON + "     [" +arrayPointX[0]
			LineJSON = LineJSON + "," + arrayPointY[0] + "],\n"
			LineJSON = LineJSON[0:len(PythonLinePoints)-2]
			LineJSON = LineJSON + "]]\n"
			LineJSON = LineJSON + "} },\n"

		elif Flag == "0":

			LineJSON = LineJSON + "     \"geometry\": { \"type\": \"LineString\","
			LineJSON = LineJSON + "\"coordinates\": [\n"
			
			for n in range(0, len(arrayPointX)-1):
				LineJSON = LineJSON + "     [" +arrayPointX[n] + ","
				LineJSON = LineJSON + arrayPointY[n] + "],\n"

			LineJSON = LineJSON[0:len(PythonLinePoints)-2]
			LineJSON = LineJSON + "]\n"
			LineJSON = LineJSON + "} },\n"
		#Fin de Concatenation du JSON
		
	#LES LIGNES
	if CadSECTION == "ENTITIES" and LineDXF[i] + LineDXF[i+1] == "  0\nLINE\n":
			
		j=i+2
		ListePointsX = ""
		ListePointsY = ""
		PythonLinePoints = ""
		Handle = ""
		LayerName = ""
		Flag = "0"
		Link = ""
		laCouleur = "BYLAYER"
		LINE = LINE + 1
			
		while LineDXF[j] != "  0\n":
		
			if LineDXF[j] == "  5\n":										#LePointeur
				Handle = LineDXF[j+1].strip()

			if LineDXF[j] == "  8\n":										#LeCalque
				LayerName = LineDXF[j+1].strip()
				
			if LineDXF[j] == " 70\n":										#LeDrapeau
				# FLAG ( default: 0 , closed polyline: 1 )
				Flag = LineDXF[j+1].strip()
				
			if LineDXF[j] == " 10\n":										#X1
				ListePointsX = ListePointsX + LineDXF[j+1].strip() + ";"

			if LineDXF[j] == " 20\n":										#Y1
				ListePointsY = ListePointsY + LineDXF[j+1].strip() + ";"
				
			if LineDXF[j] == " 11\n":										#X2
				ListePointsX = ListePointsX + LineDXF[j+1].strip() + ";"

			if LineDXF[j] == " 21\n":										#Y2
				ListePointsY = ListePointsY + LineDXF[j+1].strip() + ";"
				
			if LineDXF[j] == " 62\n":										#laCouleur
				if int(LineDXF[j+1].strip()) < 10:
					laCouleur = ListeCouleur[int(LineDXF[j+1].strip())]
				else:
					laCouleur = "#" + LineDXF[j+1].strip()

			if LineDXF[j] + LineDXF[j+1] + LineDXF[j+2] == "1001\nPE_URL\n1000\n":	#Link
				Link = "_" + LineDXF[j+3].strip() + "_"
				
			j = j + 2
			#Fin de ceuillette Mtext
			
		#tu split BasePointX
		arrayPointX = ListePointsX.split(";")
		#Tu split BasePointY
		arrayPointY = ListePointsY.split(";")

		#Concatenation du JSON
		LineJSON = LineJSON + "{ \"type\": \"Feature\", \"properties\": { \"ENTITIES\": \"LINE\", \"LayerName\": \"" + LayerName + "\", \"Handle\": \"" + Handle + "\", \"laCouleur\": \"" + laCouleur + "\", \"Link\": \"" + Link + "\" },\n"

		LineJSON = LineJSON + "     \"geometry\": { \"type\": \"LineString\","
		LineJSON = LineJSON + "\"coordinates\": [\n"
		
		for n in range(0, len(arrayPointX)-1):
			LineJSON = LineJSON + "     [" +arrayPointX[n] + ","
			LineJSON = LineJSON + arrayPointY[n] + "],\n"

		LineJSON = LineJSON[0:len(PythonLinePoints)-2]
		LineJSON = LineJSON + "]\n"
		LineJSON = LineJSON + "} },\n"
		#Fin de Concatenation du JSON
		
	#LES CERCLES
	if CadSECTION == "ENTITIES" and LineDXF[i] + LineDXF[i+1] == "  0\nCIRCLE\n":
			
		j=i+2
		PointsX = ""
		PointsY = ""
		ListePointsX = ""
		ListePointsY = ""
		PythonLinePoints = ""
		Handle = ""
		LayerName = ""
		Flag = "0"
		Link = ""
		laCouleur = "BYLAYER"
		RADIUS = ""
		CIRCLE = CIRCLE + 1
			
		while LineDXF[j] != "  0\n":
		
			if LineDXF[j] == "  5\n":										#LePointeur
				Handle = LineDXF[j+1].strip()

			if LineDXF[j] == "  8\n":										#LeCalque
				LayerName = LineDXF[j+1].strip()
				
			if LineDXF[j] == " 70\n":										#LeDrapeau
				# FLAG ( default: 0 , closed polyline: 1 )
				Flag = LineDXF[j+1].strip()
				
			if LineDXF[j] == " 10\n":										#X
				PointsX = LineDXF[j+1].strip()

			if LineDXF[j] == " 20\n":										#Y
				PointsY = LineDXF[j+1].strip()
				
			if LineDXF[j] == " 40\n":										#RADIUS
				RADIUS = LineDXF[j+1].strip()
				
			if LineDXF[j] == " 62\n":										#laCouleur
				if int(LineDXF[j+1].strip()) < 10:
					laCouleur = ListeCouleur[int(LineDXF[j+1].strip())]
				else:
					laCouleur = "#" + LineDXF[j+1].strip()

			if LineDXF[j] + LineDXF[j+1] + LineDXF[j+2] == "1001\nPE_URL\n1000\n":	#Link
				Link = "_" + LineDXF[j+3].strip() + "_"
				
			j = j + 2
			#Fin de ceuillette Mtext
			
		for alfa in range (0,360,10):
			
			#Tu calcules trigonometriquement tout les points du cercle
			ListePointsX = ListePointsX + str(math.cos(math.radians(alfa+1))*float(RADIUS)+float(PointsX)) + ";"
			ListePointsY = ListePointsY + str(math.sin(math.radians(alfa+1))*float(RADIUS)+float(PointsY)) + ";"
			
		#tu split BasePointX
		arrayPointX = ListePointsX.split(";")
		#Tu split BasePointY
		arrayPointY = ListePointsY.split(";")

		#Concatenation du JSON
		LineJSON = LineJSON + "{ \"type\": \"Feature\", \"properties\": { \"ENTITIES\": \"CIRCLE\", \"LayerName\": \"" + LayerName + "\", \"Handle\": \"" + Handle + "\", \"laCouleur\": \"" + laCouleur + "\", \"Link\": \"" + Link + "\" },\n"
			
		LineJSON = LineJSON + "     \"geometry\": { \"type\": \"Polygon\","
		LineJSON = LineJSON + "\"coordinates\": [[\n"
			
		for n in range(0, len(arrayPointX)-1):
			LineJSON = LineJSON + "     [" +arrayPointX[n]
			LineJSON = LineJSON +  "," + arrayPointY[n] + "],\n"
			
		LineJSON = LineJSON + "     [" +arrayPointX[0]
		LineJSON = LineJSON + "," + arrayPointY[0] + "],\n"
		LineJSON = LineJSON[0:len(PythonLinePoints)-2]
		LineJSON = LineJSON + "]]\n"
		LineJSON = LineJSON + "} },\n"

		#Fin de Concatenation du JSON

	# LES NOTES        
	if CadSECTION == "ENTITIES" and LineDXF[i] + LineDXF[i+1] == "  0\nMTEXT\n":

		PointsX = ""
		PointsY = ""
		LaNote = ""
		Handle = ""
		LayerName = ""
		Link = ""
		laCouleur = "BYLAYER"
		MTEXT = MTEXT + 1
		
		j=i+2
		
		# Ici commence la ceuillette des Notes, toutes les info
		# Sont receuilli dans des variables corespondantes
		while LineDXF[j] != "  0\n":

			if LineDXF[j] == "  5\n":										#LePointeur
				Handle = LineDXF[j+1].strip()
				
			if LineDXF[j] == "  8\n":										#LeCalque
				LayerName = LineDXF[j+1].strip()
				
			if LineDXF[j] == " 10\n":										#X
				PointsX = LineDXF[j+1].strip()
				
			if LineDXF[j] == " 20\n":										#Y
				PointsY = LineDXF[j+1].strip()
				
			if LineDXF[j] == "  1\n":										#LaNote
				LaNote = LineDXF[j+1].strip()
				
				LaNote = LaNote.replace("\P", " - ")
				LaNote = LaNote.replace("{", "")
				LaNote = LaNote.replace("}", "")
				LaNote = LaNote.replace("\"", "")
				
			if LineDXF[j] == " 62\n":										#laCouleur
				if int(LineDXF[j+1].strip()) < 10:
					laCouleur = ListeCouleur[int(LineDXF[j+1].strip())]
				else:
					laCouleur = "#" + LineDXF[j+1].strip()
				
			if LineDXF[j] + LineDXF[j+1] + LineDXF[j+2] == "1001\nPE_URL\n1000\n":	#Link
				Link = "_" + LineDXF[j+3].strip() + "_"
				
			j = j + 2
		#Fin de ceuillette Mtext
		
		#Concatenation du JSON
		LineJSON = LineJSON + "{ \"type\": \"Feature\", \"properties\": { \"ENTITIES\": \"MTEXT\", \"LayerName\": \"" + LayerName + "\", \"Handle\": \"" + Handle + "\", \"laCouleur\": \"" + laCouleur + "\", \"Link\": \"" + Link + "\", \"LaNote\": \"" + LaNote + "\"  },\n"
		LineJSON = LineJSON + "     \"geometry\": { \"type\": \"Point\", \"coordinates\": [" + PointsX + "," + PointsY + "] }},\n"
		#Fin de Concatenation du JSON
		
	# LES POINTS        
	if CadSECTION == "ENTITIES" and LineDXF[i] + LineDXF[i+1] == "  0\nPOINT\n":

		PointsX = ""
		PointsY = ""
		Handle = ""
		LayerName = ""
		Link = ""
		laCouleur = "BYLAYER"
		POINT = POINT + 1
		
		j=i+2
		
		# Ici commence la ceuillette des Notes, toutes les info
		# Sont receuilli dans des variables corespondantes
		while LineDXF[j] != "  0\n":

			if LineDXF[j] == "  5\n":										#LePointeur
				Handle = LineDXF[j+1].strip()
				
			if LineDXF[j] == "  8\n":										#LeCalque
				LayerName = LineDXF[j+1].strip()
				
			if LineDXF[j] == " 10\n":										#X
				PointsX = LineDXF[j+1].strip()
				
			if LineDXF[j] == " 20\n":										#Y
				PointsY = LineDXF[j+1].strip()
				
			if LineDXF[j] == " 62\n":										#laCouleur
				if int(LineDXF[j+1].strip()) < 10:
					laCouleur = ListeCouleur[int(LineDXF[j+1].strip())]
				else:
					laCouleur = "#" + LineDXF[j+1].strip()
				
			if LineDXF[j] + LineDXF[j+1] + LineDXF[j+2] == "1001\nPE_URL\n1000\n":	#Link
				Link = "_" + LineDXF[j+3].strip() + "_"
				
			j = j + 2
		#Fin de ceuillette Mtext
		
		#Concatenation du JSON
		LineJSON = LineJSON + "{ \"type\": \"Feature\", \"properties\": { \"ENTITIES\": \"POINT\", \"LayerName\": \"" + LayerName + "\", \"Handle\": \"" + Handle + "\", \"laCouleur\": \"" + laCouleur + "\", \"Link\": \"" + Link + "\"  },\n"
		LineJSON = LineJSON + "     \"geometry\": { \"type\": \"Point\", \"coordinates\": [" + PointsX + "," + PointsY + "] }},\n"
		#Fin de Concatenation du JSON
		
	# LES BLOCS
	if CadSECTION == "ENTITIES" and LineDXF[i] + LineDXF[i+1] == "  0\nINSERT\n":

		PointsX = ""
		PointsY = ""
		leBloc = ""
		Handle = ""
		LayerName = ""
		ATTRIB = 0
		ListeValue = ""
		ListeAttribute = ""
		Link = ""
		laCouleur = "BYLAYER"
		INSERT = INSERT + 1
		
		j=i+2
		
		# Ici commence la ceuillette du Bloc, toutes les info
		# Sont receuilli dans des variables corespondantes
		while LineDXF[j] != "  0\n":
		

			
			# pour que la bouble Wile ne s'arrete pas aux ligne "  0\nATTRIB\n"
			# On prend un tour d'avance sur la lecture de LineDXF
			# Et on change le lingne "  0\n" en "  A\n"
			# La variable ATTRIB passe a 1, Signifi qu'i y a des attribues dans le bloc
			if LineDXF[j+2]+LineDXF[j+3] == "  0\nATTRIB\n": 
				LineDXF[j+2] = "  A\n"
				ATTRIB = 1
				
			if LineDXF[j] == "  2\n" and ATTRIB == 0:						#leBloc
				leBloc = LineDXF[j+1].strip()
				
			if LineDXF[j] == "  8\n":										#LeCalque
				LayerName = LineDXF[j+1].strip()
				
			if LineDXF[j] == "  5\n":										#LePointeur
				Handle = LineDXF[j+1].strip()
				
			if LineDXF[j] == " 10\n":								#X
				PointsX = LineDXF[j+1].strip()
				
			if LineDXF[j] == " 20\n":								#Y
				PointsY = LineDXF[j+1].strip()
				
			if LineDXF[j] == " 62\n":										#laCouleur
				if int(LineDXF[j+1].strip()) < 10:
					laCouleur = ListeCouleur[int(LineDXF[j+1].strip())]
				else:
					laCouleur = "#" + LineDXF[j+1].strip()

			if LineDXF[j] + LineDXF[j+1] + LineDXF[j+2] == "1001\nPE_URL\n1000\n":	#Link
				Link = "_" + LineDXF[j+3].strip() + "_"
				
			if LineDXF[j] == "  1\n" and ATTRIB == 1:		#Valeur d'attribue
				ListeValue = ListeValue + LineDXF[j+1].strip() + ";"
				
			if LineDXF[j] == "  2\n" and ATTRIB == 1:		#Nom d'attribue
				ListeAttribute = ListeAttribute + LineDXF[j+1].strip() + ";"
				
			j = j + 2
		#Fin de ceuillette des INSERT, la suite dans ATTRIB
		
		#tu split ListeValue
		arrayValue = ListeValue.split(";")
		#Tu split ListeAttribute
		arrayAttribute = ListeAttribute.split(";")
		
		#Concatenation du JSON
		LineJSON = LineJSON + "{ \"type\": \"Feature\", \"properties\": { \"ENTITIES\": \"INSERT\", \"LayerName\": \"" + LayerName + "\", \"Handle\": \"" + Handle + "\", \"laCouleur\": \"" + laCouleur + "\", \"Link\": \"" + Link + "\", \"leBloc\": \"" + leBloc + "\""
		
		if ATTRIB == 1:
			
			for n in range(0, len(arrayAttribute)-1):
				LineJSON = LineJSON + ", \"" + arrayAttribute[n] + "\": \"" + arrayValue[n] + "\""
				
			#LineJSON = LineJSON[0:len(PythonLinePoints)-2]
			
		LineJSON = LineJSON +   "},\n" # attribute...
		LineJSON = LineJSON + "     \"geometry\": { \"type\": \"Point\", \"coordinates\": [" + PointsX + "," + PointsY + "] }},\n"
		# Fin de Concatenation du JSON
		
	# Incrementation de lecture
	i = i +2
	
	

LineJSON = LineJSON[0:len(PythonLinePoints)-2] + "]\n}"

JSON = open( foo, "w")
JSON.write(LineJSON)
JSON.close()





BigPrint = pyfiglet.figlet_format(" DXF  2  JSON ") 
print(BigPrint)

print "###############################################################"
print "LIST OF EXTRACTIONS"
print "LWPOLYLINE : " , LWPOLYLINE
print "LINE : " , LINE
print "CIRCLE : " , CIRCLE
print "MTEXT : " , MTEXT
print "POINT : " , POINT
print "INSERT : " , INSERT
print "Total Entities : " , LWPOLYLINE + LINE + CIRCLE + MTEXT + POINT + INSERT
print "###############################################################"
print "                                           YOUR JSON IS DONE !!"