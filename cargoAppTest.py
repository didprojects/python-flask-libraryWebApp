import unittest
from cargoApp import calculateTrolleyNumber, loadDataFromFile

class TestCargoApp(unittest.TestCase):
    def test_calculateTrolleyNumber(self):
        loaded_data1 = {'10221':{"mass":293.0, "volume":[0.2, 1.2, 2.3]},'10222':{'mass':9.2, "volume":[2.0, 2.2, 2.3]}}
        loaded_data2 = {'10223':{"mass":193.0, "volume":[0.2, 1.2, 2.3]},'10224':{'mass':9.2, "volume":[0, 0, 0]}}
        loaded_data3 = {'10224':{'mass':9.2, "volume":[0, 0, 0]},'10225':{"mass":293.0, "volume":[0.2, 1.2, 2.3]}}
        loaded_data4 = {'10223':{"mass":193.0, "volume":[0.2, 1.2, 2.3]},
                        '10224':{'mass':9.2, "volume":[0, 0, 0]},
                        '10226':{"mass":200.0, "volume":[0.2, 1.2, 2.3]},
                        '10227':{"mass":200.0, "volume":[0.2, 1.2, 2.3]},
                        '10228':{"mass":200.0, "volume":[0.2, 1.2, 2.3]},
                        '10229':{"mass":200.0, "volume":[0.2, 1.2, 2.3]},
                        '10230':{"mass":200.0, "volume":[0.2, 1.2, 2.3]},
                        '10231':{"mass":200.0, "volume":[0.2, 1.2, 2.3]},
                        '10232':{"mass":200.0, "volume":[0.2, 1.2, 2.3]},
                        '10233':{"mass":200.0, "volume":[0.2, 1.2, 2.3]},
                        '10234':{"mass":200.0, "volume":[0.2, 1.2, 2.3]},
                        '10235':{"mass":200.0, "volume":[0.2, 1.2, 2.3]},
                        '10236':{"mass":200.0, "volume":[0.2, 1.2, 2.3]},
                        '10237':{"mass":200.0, "volume":[0.2, 1.2, 2.3]},
                        '10238':{"mass":200.0, "volume":[0.2, 1.2, 2.3]},
                        '10239':{"mass":200.0, "volume":[0.2, 1.2, 2.3]},
                        '10240':{"mass":200.0, "volume":[0.2, 1.2, 2.3]},
                        '10241':{"mass":200.0, "volume":[0.2, 1.2, 2.3]}}
        
        self.assertEqual(calculateTrolleyNumber(loaded_data1),0)
        self.assertEqual(calculateTrolleyNumber(loaded_data2),1)
        self.assertEqual(calculateTrolleyNumber(loaded_data3),1)
        self.assertEqual(calculateTrolleyNumber(loaded_data4),2)

    def test_loadDataFromFile(self):
        file1 = "Test.yaml"
        file2 = "cargoData.yaml"
        file3 = "Data.txt"
        self.assertEqual(loadDataFromFile(file1),'')
        self.assertGreater(len(loadDataFromFile(file2)),0)
        self.assertEqual(loadDataFromFile(file3),'')
         

if __name__=='__main__':
	unittest.main()