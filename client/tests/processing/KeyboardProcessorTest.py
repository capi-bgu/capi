import time
import unittest
from tests.SessionStub import SessionStub
from src.processing.KeyboardProcessor import KeyboardProcessor
from tests.collection.stubs.KeyboardCollectorStub import KeyboardCollectorStub
from tests.database.sqlite_db.stubs.KeyboardDataHandlerStub import KeyboardDataHandlerStub


class KeyboardProcessorTest(unittest.TestCase):
    def test(self):
        keyboard_collector = KeyboardCollectorStub()
        keyboard_collector.start()
        keyboard_collector.join()
        start_time, data = keyboard_collector.stop_collect()

        self.kbpt = KeyboardProcessor()
        session_duration = 5
        session = SessionStub(0, session_duration, start_time)
        self.kbpt.set_arguements(data, session)

        st = time.time()
        self.kbpt.start()
        self.kbpt.join()
        features = self.kbpt.features
        print(time.time() - st)

        self.assertAlmostEqual(features['typing_speed'], 3.8, delta=0.05)
        self.assertAlmostEqual(features['active_typing_speed'], 5.4285, delta=0.05)
        self.assertAlmostEqual(features['average_press_duration'], 0.04, delta=0.05)
        self.assertAlmostEqual(features['average_down_to_down'], 0.08, delta=0.07)
        self.assertEqual(features['regular_press_count'], 16)
        self.assertEqual(features['punctuations_press_count'], 0)
        self.assertEqual(features['space_counter'], 3)
        self.assertEqual(features['error_corrections'], 0)
        self.assertEqual(features['uppercase_counter'], 0)
        self.assertAlmostEqual(features['digraph_duration'], 0, delta=0.05)
        self.assertAlmostEqual(features['trigraph_duration'], 0, delta=0.05)
        self.assertEqual(features['mode_key'], ord('e'.upper()))
        self.assertAlmostEqual(features['idle_time'], 1.5, delta=0.05)
        self.assertEqual(features['unique_events'], 10)

        data_handler = KeyboardDataHandlerStub(name="processed")
        data_handler.save(features)


if __name__ == '__main__':
    unittest.main()
