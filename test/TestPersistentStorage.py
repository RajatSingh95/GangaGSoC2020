import unittest
import copy
from gangagsoc.Initial_Task.countWord import * 
from gangagsoc.Persistent_Storage_Task.subtask_2 import recreate_job
class TestPersistentStorage(unittest.TestCase):

    def test_recreate_job(self):
        cwd = os.path.abspath(os.getcwd())
        actual_job  = count_word_from_pdf(cwd+"/test/test2.pdf",cwd+'/gangagsoc/Initial_Task/count_word.sh',cwd+'/gangagsoc/Initial_Task/merge_result.py')

        # It includes writing the actual job string to db
        # and reading it back and recreating it.
        read_time,create_time,created_job = recreate_job(actual_job)
        created_job.submit()
        self.assertEqual(len(created_job.subjobs), 2)
        self.assertEqual(len(created_job.inputfiles), 2)

if __name__ == '__main__':
    unittest.main()
