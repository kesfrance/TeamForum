import unittest
import os
import json
from urlparse import urlparse

# Configure app to use the testing databse
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog import models
from blog.database import Base, engine, session


class TestAPI(unittest.TestCase):
    """ Tests for the posts API """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)
   
    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)
    
    def test_get_empty_posts(self):
        """ Getting posts from an empty database """
        response = self.client.get("/post/JSON")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        data = json.loads(response.data)
        self.assertEqual(data, [])
    
    def test_get_posts(self):
        """ Getting posts from a populated database """
        postA = models.Post(title="Example Post A", description = "testingA", content="Just a test")
        postB = models.Post(title="Example Post B", description = "testingB", content="Still a test")

        session.add_all([postA, postB])
        session.commit()

        response = self.client.get("/post/JSON")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        data = json.loads(response.data)
        self.assertEqual(len(data), 2)

        postA = data[0]
        self.assertEqual(postA["title"], "Example Post A")
        self.assertEqual(postA["description"], "testingA")
        self.assertEqual(postA["content"], "Just a test")

        postB = data[1]
        self.assertEqual(postB["title"], "Example Post B")
        self.assertEqual(postB["description"], "testingB")
        self.assertEqual(postB["content"], "Still a test")

    def test_get_post(self):
        """ Getting a single post from a populated database """
        postA = models.Post(title="Example Post A", description = "testA", content="Just a test")
        postB = models.Post(title="Example Post B", description = "testB", content="Still a test")

        session.add_all([postA, postB])
        session.commit()

        response = self.client.get("/post/{}/JSON".format(postB.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        post = json.loads(response.data)
        self.assertEqual(post["title"], "Example Post B")
        self.assertEqual(post["description"], "testB")
        self.assertEqual(post["content"], "Still a test")

    def test_get_non_existent_post(self):
        """ Getting a single post which doesn't exist """
        response = self.client.get("/post/4/JSON")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.mimetype, "application/json")

        data = json.loads(response.data)
        self.assertEqual(data["message"], "Could not find post with id 4")
    


if __name__ == "__main__":
    unittest.main()
