# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CreatePostgisSwdeDb
                                 A part of QGIS plugin
 odpowiada za tworzenie nowej postgisowej bazy dla danych z plików SWDE
                              -------------------
        begin                : 2013-06-23
        copyright            : (C) 2013 by Robert Dorna - robbur
        email                : robert.dorna@wp.eu
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from rob_db_connection import RobDBBase
from rob_db_connection import RobDBTable

class CreatePostgisSwdeDb:
 
    def __init__(self, host, db, postgisver,  owner, admin, adminpswd):
        #print "connect w db = " + str(connect)
        self.host = host
        self.db = db
        self.owner = owner
        self.admin = admin
        self.adminpswd = adminpswd
        self.postgisver = postgisver


    def createSwdeTables(self):

        rdbase = RobDBBase(str(self.host), str(self.db), str(self.admin), str(self.adminpswd), 1)

        sqlstr = "CREATE TABLE g5adr(tab_uid character varying(50) NOT NULL, g5tar character(1), g5naz character varying(150), g5krj character varying(100),g5wjd character varying(100),g5pwj character varying(100),g5gmn character varying(100),g5ulc character varying(255),g5nra character varying(50),g5nrl character varying(50), g5msc character varying(100), g5kod character varying(50),g5pcz character varying(100),g5dtw character varying(25),g5dtu character varying(25),id_zd character varying(50) NOT NULL,g5id2 character varying(50),g5id1 character varying(50),CONSTRAINT g5adr_pkey PRIMARY KEY (tab_uid ))WITH (OIDS=FALSE)"
        rdbase.executeSQL(sqlstr)
        sqlstr = "ALTER TABLE g5adr OWNER TO " + self.owner

        rdbase.executeSQL(sqlstr)
        sqlstr = "ALTER TABLE g5adr COMMENT ON TABLE g5adr IS 'Adres obiektu'"
        rdbase.executeSQL(sqlstr)
        sqlstr = "COMMENT ON COLUMN g5adr.tab_uid IS 'Adres obiektu'"
        rdbase.executeSQL(sqlstr)
        sqlstr = "COMMENT ON COLUMN g5adr.g5tar IS 'typ adresu 1 - adres, 2 - nazwa własna'"
        rdbase.executeSQL(sqlstr)
        sqlstr = "COMMENT ON COLUMN g5adr.g5krj IS 'kraj'"
        rdbase.executeSQL(sqlstr)
        sqlstr = "COMMENT ON COLUMN g5adr.g5wjd IS 'województwo'"
        rdbase.executeSQL(sqlstr)
        sqlstr = "COMMENT ON COLUMN g5adr.g5pwj IS 'powiat, miasto'"
        rdbase.executeSQL(sqlstr)
        sqlstr = "COMMENT ON COLUMN g5adr.g5gmn IS 'gmina'"
        rdbase.executeSQL(sqlstr)
        sqlstr = "COMMENT ON COLUMN g5adr.g5ulc IS 'ulica'"
        rdbase.executeSQL(sqlstr)
        sqlstr = "COMMENT ON COLUMN g5adr.g5nra IS 'numer porzadkowy domu - niestety muszę zarezerwować 50 znakow poniewaz zdazylo sie ze to pole było wykorzystywanie jako komentaż'"
        rdbase.executeSQL(sqlstr)
        sqlstr = "COMMENT ON COLUMN g5adr.g5nrl IS 'nr lokalu - uwagi jak do g5nra'"
        rdbase.executeSQL(sqlstr)
        sqlstr = "COMMENT ON COLUMN g5adr.g5msc IS 'Miejscowośc '"
        rdbase.executeSQL(sqlstr)
        sqlstr = "COMMENT ON COLUMN g5adr.g5kod IS 'kod pocztowy - początkowo miałem 7 znaków, ale trafiłem na jakieś długasy - zagraniczne kody"
        rdbase.executeSQL(sqlstr)
        sqlstr = "COMMENT ON COLUMN g5adr.g5pcz IS 'poczta'"
        rdbase.executeSQL(sqlstr)
        sqlstr = "COMMENT ON COLUMN g5adr.g5dtw IS 'Data weryfikacji danych'"
        rdbase.executeSQL(sqlstr)
        sqlstr = "COMMENT ON COLUMN g5adr.g5dtu IS 'Data utworzenia obiektu';"
        rdbase.executeSQL(sqlstr)
        sqlstr = "COMMENT ON COLUMN g5adr.id_zd IS 'Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.'"
        rdbase.executeSQL(sqlstr)
        sqlstr = "COMMENT ON COLUMN g5adr.g5id2 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po id1 i jest ciągiem różnistych znaków. '"
        rdbase.executeSQL(sqlstr)
        sqlstr = "COMMENT ON COLUMN g5adr.g5id1 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, i jest ciągiem różnistych znaków. '"
        rdbase.executeSQL(sqlstr)


    def createSwdeFunc(self):
        pass
