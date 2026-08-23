import os
import unittest

import config


class ConfigPathTests(unittest.TestCase):
    def test_map_image_path_is_absolute_and_exists(self):
        self.assertTrue(os.path.isabs(config.MAP_IMAGE_PATH))
        self.assertTrue(os.path.exists(config.MAP_IMAGE_PATH))


if __name__ == "__main__":
    unittest.main()
