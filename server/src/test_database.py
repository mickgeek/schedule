# -*- coding: utf-8 -*-

import unittest
import datetime
from database import UserGateway, TaskStatus, TaskGateway

class UserGatewayTestCase(unittest.TestCase):
    def test_find(self):
        row = UserGateway().find()
        self.assertEqual(row[0].name, 'michael')
        self.assertEqual(row[1].name, 'emily')

    def test_find_by_id(self):
        row = UserGateway().find_by_id(1)
        self.assertEqual(row.name, 'michael')

    def test_find_by_name(self):
        row = UserGateway().find_by_name('michael')
        self.assertEqual(row.id, 1)

class TaskGatewayTestCase(unittest.TestCase):
    def test_find_by_date(self):
        row = TaskGateway().find_by_date('2022-05-15', 1)
        self.assertEqual(row[0].description, 'Edit the book of a jungle.')

    def test_create(self):
        row = TaskGateway().create('Read the code book.', TaskStatus.OPENED.value, '2022-05-15', 1)
        self.assertEqual(row, 4)

    def test_update(self):
        updated_at = datetime.datetime.now().isoformat(' ', 'seconds')
        row = TaskGateway().update('Read three pages.', TaskStatus.CLOSED.value, updated_at, 4, 1)
        self.assertEqual(row, 0)

    def test_delete(self):
        row = TaskGateway().delete(4, 1)
        self.assertEqual(row, 0)
