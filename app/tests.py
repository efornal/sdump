# -*- encoding: utf-8 -*-
from django.test import TestCase
from .views import describe_file

class ViewsTests(TestCase):

    def test_describe_file1(self):
        filename = "tests/servername.intranet_base-databasename_db_2016-09-06-22_04.sql.gz"
        desc = describe_file( filename )
        print desc
        self.assertEqual( desc['server'], 'servername.intranet' )
        self.assertEqual( desc['time'], '22:04' )
        self.assertEqual( desc['date'], '06-09-2016' )
        self.assertEqual( desc['database'], 'databasename_db' )

    def test_describe_file2(self):
        filename = "tests/servername2015.intranet_base-databasename_db_2016-09-06-22_00.sql.gz"
        desc = describe_file( filename )
        print desc
        self.assertEqual( desc['server'], 'servername2015.intranet' )
        self.assertEqual( desc['time'], '22:00' )
        self.assertEqual( desc['date'], '06-09-2016' )
        self.assertEqual( desc['database'], 'databasename_db' )

    def test_describe_file(self):
        filename = "tests/servername-dev.intranet_base-database_name_db_16-10-2015_05-03.sql.gz"
        desc = describe_file( filename )
        print desc
        self.assertEqual( desc['server'], 'servername-dev.intranet' )
        self.assertEqual( desc['time'], '05:03' )
        self.assertEqual( desc['date'], '16-10-2015' )
        self.assertEqual( desc['database'], 'database_name_db' )
