"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app

# we need to import the file that contains the status codes
from src import status


class CounterTest(TestCase):
    """Counter tests"""

    def setUp(self):
        self.client = app.test_client()

    def test_create_a_counter(self):
        """It should create a counter"""
        result = self.client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """It should update a counter by +1"""
        post = self.client.post('/counters/coo')
        self.assertEqual(post.status_code, status.HTTP_201_CREATED)
        put = self.client.put('/counters/coo')
        self.assertEqual(put.status_code, status.HTTP_200_OK)
        self.assertEqual(put.json["coo"], post.json["coo"] + 1)

    def test_read_a_counter(self):
        post = self.client.post('/counters/dar')
        self.assertEqual(post.status_code, status.HTTP_201_CREATED)

        res = self.client.get('/counters/read/dar')
        self.assertEqual(res.json["message"], "Counter: dar reads at: 0")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.client.put('/counters/dar')
        res = self.client.get('/counters/read/dar')
        self.assertEqual(res.json["message"], "Counter: dar reads at: 1")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_a_counter(self):
        post = self.client.post('/counters/eor')
        self.assertEqual(post.status_code, status.HTTP_201_CREATED)

        res = self.client.delete('/counters/eor')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        res = self.client.get('/counters/read/eor')
        self.assertEqual(res.json["message"], "Counter eor does not exist")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
