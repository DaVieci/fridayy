import unittest
from Database.sqliteAPI import Datenbank
from Direction.DirectionsAPI import DirectionsApi

class DirectionsAPI_test(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(DirectionsAPI_test, self).__init__(*args, **kwargs)
        self.myDB = Datenbank()
        keys = self.myDB.getKeys()
        self.__directions_key = keys[0]['directions_key']
        self.test_lat = 48.2752
        self.test_lon = 8.8546
        self.dest_lat = 49.2752
        self.dest_lon = 8.8746
        self.myDirections = DirectionsApi(self.__directions_key)

    def test_say_direction_info_wrong_key(self):
        self.myDirections.set_current_position(self.test_lat,self.test_lon)
        myDirections_invalid = DirectionsApi("wrongKey")
        directions = myDirections_invalid.say_direction_info("driving")
        self.assertEqual(directions, "Invalide Adresse!")

    def test_say_direction_info_wrong_travelmode(self):
        self.myDirections.set_current_position(self.test_lat,self.test_lon)
        directions = self.myDirections.say_direction_info("hopp")
        self.assertEqual(directions, "Invalide Adresse!")

    def test_translate_travelmode_auto(self):
        travelmode = self.myDirections.translate_travelmode('auto')
        self.assertEqual(travelmode, 'driving')

    def test_translate_travelmode_laufen(self):
        travelmode = self.myDirections.translate_travelmode('laufen')
        self.assertEqual(travelmode, 'walking')

    def test_translate_travelmode_zug(self):
        travelmode = self.myDirections.translate_travelmode('zug')
        self.assertEqual(travelmode, 'transit')

    def test_translate_travelmode_fahrrad(self):
        travelmode = self.myDirections.translate_travelmode('fahrrad')
        self.assertEqual(travelmode, 'bicycling')

    def test_route_to_destination(self):
        self.myDirections.set_current_position(self.test_lat,self.test_lon)
        self.myDirections.set_destination_position_lat_lon(self.dest_lat,self.dest_lon)
        self.assertEqual(None, self.myDirections.route_to_destination('driving'))

    def test_say_direction_info(self):
        self.myDirections.set_current_position(self.test_lat,self.test_lon)
        self.myDirections.set_destination_position_lat_lon(self.dest_lat,self.dest_lon)
        self.assertEqual('Dein Ziel ist 1 hour 59 mins und 169 km entfernt.', self.myDirections.say_direction_info('driving'))

    #def test_set_destination_position_adress(self):
    #    self.myDirections.set_destination_position_adress('Herrengaerten 17 Lenningen')
    #    self.assertEqual(None, self.myDirections.__dest_lat)

    

if __name__ == "__main__":
    unittest.main(module="DirectionsAPI_test")