import tempfile
import os
import unittest
import shutil

import gig.project


class TestProject(unittest.TestCase):

    def setUp(self):
        self.path = tempfile.mkdtemp(prefix='gig-tests')
        print self.path
        
    def tearDown(self):
        shutil.rmtree(self.path)

    def test_directory(self):
        name = 'directory-test'
        dir = gig.project.Directory(self.path, name)
        self.assertEqual('%s/%s' % (self.path, name), dir.path)

        # Creating a dir should return a new Directory with a new path
        newdir = dir.mkdir('newdir')
        self.assertEqual('%s/%s/%s' % (self.path, name, 'newdir'), newdir.path)
        
        # Safety check
        self.assertRaises(gig.project.IllegalPathError, dir.mkdir, '../path-outside-dir')

        # Test writing to a file and confirming the write/contents
        testfile = 'test-file.txt'
        testcontents = 'Test file cotents.'
        newdir.mkfile(testfile, testcontents)
        self.assertEqual(
            file('%s/%s' % (newdir.path, testfile)).read(), 
            testcontents
        )


    def test_project(self):
        name = 'project-test'
        script_fname = 'full-template'
        
        # Just build a file:// url for the template.py file in this directory
        script_url = 'file://%s' % os.path.abspath(__file__).replace(os.path.basename(__file__), script_fname)

        # template.py should create a project contaiing only 'foo/bar/test.txt'
        project = gig.project.Project(self.path, 'project-test', script_url)
        
        # A Project should behave like a directory and create the full path in __init__
        self.assertEqual('%s/%s' % (self.path, name), project.path)
        
        # Check that the Template works
        project.setup()
        
        # Tempalte should create 'foo/bar/test.txt'
        self.assertEqual(os.path.exists('%s/foo/bar/test.txt' % project.path), True)
        
        # with contents 'testing'
        self.assertEqual(file('%s/foo/bar/test.txt' % project.path).read(), 'testing')
        
        # check that a requirements file is created
        project.handle_requirements()
        self.assertEqual(file('%s/requirements.txt' % project.path).read(), 'fake-package')
        
        # Check that a package without a requirements listing wont' kill everything
        no_req_script_url = 'file://%s' % os.path.abspath(__file__).replace(os.path.basename(__file__), 'no-requirements-template')
        no_req_project = gig.project.Project(self.path, 'no-req-project', no_req_script_url)
        no_req_project.handle_requirements()
        
        # Tempalte has no requirements, should be no requirements.txt file
        self.assertEqual(os.path.exists('%s/requirements.txt' % no_req_project.path), False)
        
        
if __name__ == '__main__':
    unittest.main()
