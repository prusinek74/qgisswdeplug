qgisswdeplug
============

swde import plugins for quantum gis 

Zestaw wtyczek do Quantum Gis, tworzących środowisko do pracy z danymi zaimportowanymi z plików swde (pliki z powiatowych ośrodków Ewidencji Gruntów i Budynków) do bazy postgis
Aktualnie wtyczki mają status experymentalny. Zestaw obecnie składa się z:
  1. swdeImport - podstawowa wtyczka, umożliwia import/aktualizację danych z plików swde do bazy postgis
  2. swdeDzeInfo - pozwala uzyskać podstawowe informację o wybranej działce ewidencyjnej - odpowiednik wypisu z rejestru gruntów
  3. swdeDzeSearch - wyszukiwarka działek ewidencyjnych. Proste szukanie działek - po numerze, obrębie, jednostce ewidencyjnej. Wybrane w wyniku wyszukiwania działki tworzą nową warstwę w formacie ESRI shapefile.
  
Ponadto repozytorium zawiera również plik sql - tworzący pustą strukturę bazy postgis.
  
Aktualnie wersja rozwojowa, w fazie testowania pod linuksem oraz windows.
